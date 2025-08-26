import streamlit as st
import os
import time
from modules.conversation import ConversationManager
from modules.candidate_info import CandidateInfoCollector
from modules.tech_questions import TechQuestionGenerator
from utils.llm_utils import get_llm_response
from config.config import Config

# Page configuration
st.set_page_config(
    page_title=Config.APP_NAME,
    page_icon="👨‍💼",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #1E88E5;
    text-align: center;
    margin-bottom: 1rem;
}
.sub-header {
    font-size: 1.5rem;
    color: #424242;
    text-align: center;
    margin-bottom: 2rem;
}
.chat-message {
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    gap: 0.75rem;
}
.assistant {
    background-color: #F3F4F6;
}
.human {
    background-color: #E3F2FD;
}
.avatar {
    width: 2.5rem;
    height: 2.5rem;
    border-radius: 0.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
}
.assistant .avatar {
    background-color: #1E88E5;
    color: white;
}
.human .avatar {
    background-color: #78909C;
    color: white;
}
.message-content {
    flex: 1;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state variables if they don't exist
def initialize_session_state():
    if 'conversation_manager' not in st.session_state:
        st.session_state.conversation_manager = ConversationManager()
    
    if 'candidate_collector' not in st.session_state:
        st.session_state.candidate_collector = CandidateInfoCollector()
    
    if 'question_generator' not in st.session_state:
        st.session_state.question_generator = TechQuestionGenerator()
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'current_stage' not in st.session_state:
        st.session_state.current_stage = "greeting"
    
    if 'candidate_info' not in st.session_state:
        st.session_state.candidate_info = {}
    
    if 'tech_stack' not in st.session_state:
        st.session_state.tech_stack = []
    
    if 'questions_generated' not in st.session_state:
        st.session_state.questions_generated = False

# Function to display chat messages
def display_messages():
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        
        if role == "assistant":
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(content)
        else:  # human
            with st.chat_message("user", avatar="👤"):
                st.markdown(content)

# Function to add a message to the chat history
def add_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})

# Function to handle the conversation flow
def handle_conversation(user_input):
    # Add user message to chat
    add_message("human", user_input)
    
    # Get current conversation stage
    stage = st.session_state.current_stage
    
    # Process based on current stage
    if stage == "greeting":
        # Move to information gathering stage
        st.session_state.current_stage = "collect_name"
        response = st.session_state.conversation_manager.get_name_prompt()
    
    elif stage == "collect_name":
        # Store name and move to email collection
        st.session_state.candidate_info["name"] = user_input
        st.session_state.current_stage = "collect_email"
        response = st.session_state.conversation_manager.get_email_prompt()
    
    elif stage == "collect_email":
        # Validate email before storing
        if st.session_state.candidate_collector.validate_email(user_input):
            # Store email and move to phone collection
            st.session_state.candidate_info["email"] = user_input
            st.session_state.current_stage = "collect_phone"
            response = st.session_state.conversation_manager.get_phone_prompt()
        else:
            # Email validation failed, ask again
            response = "That doesn't appear to be a valid email address. Please provide a valid email in the format: example@domain.com"
    
    elif stage == "collect_phone":
        # Validate phone before storing
        if st.session_state.candidate_collector.validate_phone(user_input):
            # Store phone and move to experience collection
            st.session_state.candidate_info["phone"] = user_input
            st.session_state.current_stage = "collect_experience"
            response = st.session_state.conversation_manager.get_experience_prompt()
        else:
            # Phone validation failed, ask again
            response = "That doesn't appear to be a valid phone number. Please provide a valid phone number (10-15 digits, can include country code)."
    
    elif stage == "collect_experience":
        # Store experience and move to position collection
        st.session_state.candidate_info["experience"] = user_input
        st.session_state.current_stage = "collect_position"
        response = st.session_state.conversation_manager.get_position_prompt()
    
    elif stage == "collect_position":
        # Store position and move to location collection
        st.session_state.candidate_info["position"] = user_input
        st.session_state.current_stage = "collect_location"
        response = st.session_state.conversation_manager.get_location_prompt()
    
    elif stage == "collect_location":
        # Store location and move to tech stack collection
        st.session_state.candidate_info["location"] = user_input
        st.session_state.current_stage = "collect_tech_stack"
        response = st.session_state.conversation_manager.get_tech_stack_prompt()
    
    elif stage == "collect_tech_stack":
        # Store tech stack and move to question generation
        st.session_state.tech_stack = st.session_state.candidate_collector.parse_tech_stack(user_input)
        st.session_state.current_stage = "generate_questions"
        
        # Store candidate information in database (currently simulated)
        storage_success = st.session_state.candidate_collector.store_candidate_info(
            st.session_state.candidate_info, 
            st.session_state.tech_stack
        )
        
        # Generate questions based on tech stack
        questions = st.session_state.question_generator.generate_questions(st.session_state.tech_stack)
        st.session_state.questions_generated = True
        
        # Format the questions for display
        response = st.session_state.conversation_manager.format_questions(questions)
    
    elif stage == "generate_questions":
        # Check for conversation ending keywords
        if st.session_state.conversation_manager.is_conversation_ending(user_input):
            st.session_state.current_stage = "end_conversation"
            response = st.session_state.conversation_manager.get_end_conversation_message()
        else:
            # Continue the conversation with follow-up based on the user's response to questions
            prompt = st.session_state.conversation_manager.create_follow_up_prompt(
                user_input, 
                st.session_state.candidate_info, 
                st.session_state.tech_stack
            )
            response = get_llm_response(prompt)
    
    elif stage == "end_conversation":
        # If user continues after end message, provide a final goodbye
        response = Config.FALLBACK_MESSAGE
    
    # Add assistant response to chat
    add_message("assistant", response)

# Main function
def main():
    # Initialize session state
    initialize_session_state()
    
    # Display header
    st.markdown(f'<h1 class="main-header">{Config.APP_NAME}</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Your AI-powered recruitment companion</p>', unsafe_allow_html=True)
    
    # Display chat messages
    display_messages()
    
    # If this is the first interaction, send greeting
    if len(st.session_state.messages) == 0:
        greeting = st.session_state.conversation_manager.get_greeting()
        add_message("assistant", greeting)
        st.rerun()
    
    # Get user input
    user_input = st.chat_input("Type your message here...")
    
    # Process user input
    if user_input:
        handle_conversation(user_input)
        st.rerun()

# Run the app
if __name__ == "__main__":
    main()