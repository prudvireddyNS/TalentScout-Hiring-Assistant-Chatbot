import streamlit as st
import os
import time
import json
from datetime import datetime
from typing import Dict, List, Optional
import re
import pandas as pd

# Import classes from their respective files
from modules.conversation import ConversationManager
from modules.candidate_info import CandidateInfoCollector
from modules.tech_questions import TechQuestionGenerator
from config.config import Config # Assuming a config.py file exists with a Config class

# Page configuration
st.set_page_config(
    page_title=f"{Config.APP_NAME}",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
with open("static/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session state
def initialize_session_state():
    defaults = {
        'conversation_manager': ConversationManager(),
        'candidate_collector': CandidateInfoCollector(),
        'question_generator': TechQuestionGenerator(),
        'messages': [],
        'current_stage': "greeting",
        'candidate_info': {},
        'tech_stack': [],
        'questions_generated': False,
        'session_start_time': datetime.now(),
        'current_questions': [],
        'interview_complete': False
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def get_progress_percentage():
    stages = {
        "greeting": 10, "collect_name": 20, "collect_email": 30,
        "collect_phone": 40, "collect_experience": 50, "collect_position": 60,
        "collect_location": 70, "collect_tech_stack": 80, "generate_questions": 90,
        "interview_complete": 100
    }
    return stages.get(st.session_state.current_stage, 0)

def get_status_info():
    stage = st.session_state.current_stage
    if stage in ["greeting", "collect_name", "collect_email", "collect_phone", 
                "collect_experience", "collect_position", "collect_location"]:
        return ("📝 Collecting Information", "status-collecting")
    elif stage == "collect_tech_stack":
        return ("💻 Tech Stack Analysis", "status-collecting")
    elif stage == "generate_questions":
        return ("🎯 Interview Ready", "status-ready")
    elif stage == "interview_complete":
        return ("✅ Complete", "status-complete")
    return ("", "")

def add_message(role: str, content: str):
    st.session_state.messages.append({
        "role": role, 
        "content": content,
        "timestamp": datetime.now().strftime("%H:%M")
    })

def display_chat():
    """Display chat messages with better formatting"""
    for message in st.session_state.messages:
        if message["role"] == "assistant":
            st.markdown(f"""
            <div class="assistant-message">
                🤖 <strong>TalentScout</strong> <small>({message['timestamp']})</small><br>
                {message['content']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="user-message">
                👤 <strong>You</strong> <small>({message['timestamp']})</small><br>
                {message['content']}
            </div>
            """, unsafe_allow_html=True)

    # Add a scroll anchor at the bottom of the chat
    st.markdown('<div id="chat-anchor"></div>', unsafe_allow_html=True)

# In app.py
def handle_user_input(user_input: str):
    """Handle user input based on current stage"""
    add_message("user", user_input)
    stage = st.session_state.current_stage
    manager = st.session_state.conversation_manager
    collector = st.session_state.candidate_collector
    
    if stage == "greeting":
        st.session_state.candidate_info["name"] = user_input.strip()
        st.session_state.current_stage = "collect_email"
        response = manager.get_name_prompt()
    
    elif stage == "collect_email":
        if collector.validate_email(user_input):
            st.session_state.candidate_info["email"] = user_input.strip()
            st.session_state.current_stage = "collect_phone"
            response = manager.get_phone_prompt()
        else:
            response = "⚠️ Please provide a valid email address (e.g., john@example.com)"
    
    elif stage == "collect_phone":
        if collector.validate_phone(user_input):
            st.session_state.candidate_info["phone"] = user_input.strip()
            st.session_state.current_stage = "collect_experience"
            response = manager.get_experience_prompt()
        else:
            response = "⚠️ Please provide a valid phone number (10-15 digits)"
    
    elif stage == "collect_experience":
        st.session_state.candidate_info["experience"] = user_input.strip()
        st.session_state.current_stage = "collect_position"
        response = manager.get_position_prompt()
    
    elif stage == "collect_position":
        st.session_state.candidate_info["position"] = user_input.strip()
        st.session_state.current_stage = "collect_location"
        response = manager.get_location_prompt()
    
    elif stage == "collect_location":
        st.session_state.candidate_info["location"] = user_input.strip()
        st.session_state.current_stage = "collect_tech_stack"
        response = manager.get_tech_stack_prompt()
    
    elif stage == "collect_tech_stack":
        st.session_state.tech_stack = collector.parse_tech_stack(user_input)
        st.session_state.current_stage = "generate_questions"
        
        # Generate questions
        questions_dict = st.session_state.question_generator.generate_questions(
            st.session_state.tech_stack, Config.QUESTIONS_PER_TECH
        )
        st.session_state.current_questions = questions_dict
        
        response = manager.format_questions(questions_dict)
    
    elif stage == "generate_questions":
        user_lower = user_input.lower().strip()
        
        if manager.is_conversation_ending(user_input):
            st.session_state.current_stage = "interview_complete"
            response = manager.get_end_conversation_message()
        
        elif user_lower in ["summary", "profile", "info"]:
            profile_data = st.session_state.candidate_info.copy()
            profile_data["tech_stack"] = ", ".join(st.session_state.tech_stack)
            
            summary_text = "\n".join([f"**{k.title()}:** {v}" for k, v in profile_data.items()])
            duration = datetime.now() - st.session_state.session_start_time
            duration_str = f"{int(duration.total_seconds() / 60)} minutes"
            
            response = f"""
            📊 **Your Complete Profile:**
            
            {summary_text}
            
            **Generated Questions:** {len(st.session_state.current_questions.get('python', []))}
            **Session Duration:** {duration_str}
            
            Would you like to download your profile or generate more questions?
            """
        
        elif user_lower in ["next", "more", "continue"]:
            response = "I can't generate more questions at this moment. You can provide your answers to the current questions or type 'done' to finish."
        
        else:
            # Step 1: Create the prompt for the LLM using the manager
            llm_prompt = manager.create_follow_up_prompt(user_input, st.session_state.candidate_info, st.session_state.tech_stack)
            
            # Step 2: Use the LLM utility to get a clean response
            from utils.llm_utils import get_llm_response
            
            try:
                response = get_llm_response(llm_prompt)
            except Exception as e:
                print(f"Error during LLM call: {e}")
                response = "I'm having trouble generating a response right now. Please try again or type 'done' to finish the interview."
            
            # Step 3: The manager already adds the user input to history, so we just need to add the assistant's response.
            # This is handled by the final line of this function, so no need to call manager.add_to_history here.
            
    else:
        response = manager.get_end_conversation_message()
    
    add_message("assistant", response)

def export_profile():
    """Export candidate profile as JSON"""
    profile = {
        "candidate_info": st.session_state.candidate_info,
        "tech_stack": st.session_state.tech_stack,
        "questions": st.session_state.current_questions,
        "session_date": datetime.now().isoformat(),
        "duration": str(datetime.now() - st.session_state.session_start_time)
    }
    return json.dumps(profile, indent=2)

def main():
    initialize_session_state()
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"### {Config.APP_NAME}")
        
        # Progress
        progress = get_progress_percentage()
        st.progress(progress / 100)
        st.write(f"Progress: {progress}%")
        
        # Status
        status_text, status_class = get_status_info()
        if status_text:
            st.markdown(f'<div class="status-badge {status_class}">{status_text}</div>', 
                       unsafe_allow_html=True)
        
        st.divider()
        
        # Candidate Info Summary
        if st.session_state.candidate_info:
            st.markdown("**👤 Candidate Info:**")
            for key, value in st.session_state.candidate_info.items():
                st.write(f"**{key.title()}:** {value}")
        
        if st.session_state.tech_stack:
            st.markdown("**💻 Tech Stack:**")
            st.write(", ".join(st.session_state.tech_stack))
        
        st.divider()
        
        # Export functionality
        if st.session_state.current_stage in ["generate_questions", "interview_complete"]:
            if st.button("📥 Export Profile", use_container_width=True):
                profile_data = export_profile()
                st.download_button(
                    label="💾 Download JSON",
                    data=profile_data,
                    file_name=f"candidate_profile_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
        
        # Reset functionality
        if st.button("🔄 Start Over", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Main content
    col1, col2, col3 = st.columns([1, 8, 1])
    
    with col2:
        # Header
        st.markdown(f'<h1 class="main-header">{Config.APP_NAME}</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">🚀 AI-powered recruitment made simple and effective</p>', unsafe_allow_html=True)
        
        # Progress bar
        progress = get_progress_percentage()
        st.markdown(f"""
        <div class="progress-container">
            <div class="progress-bar" style="width: {progress}%"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Chat interface
        if not st.session_state.messages:
            greeting = st.session_state.conversation_manager.get_greeting()
            add_message("assistant", greeting)
        
        # Display chat
        chat_container = st.container(height=400)
        with chat_container:
            display_chat()

        # Add a JavaScript snippet to scroll to the anchor
        st.markdown("""
        <script>
            var chatAnchor = window.parent.document.getElementById("chat-anchor");
            if (chatAnchor) {
                chatAnchor.scrollIntoView({behavior: "smooth", block: "end"});
            }
        </script>
        """, unsafe_allow_html=True)
        
        # Input
        if st.session_state.current_stage != "interview_complete":
            # Use st.form to handle both Enter key and Send button submission
            with st.form("chat_form", clear_on_submit=True):
                user_input = st.text_input(
                    "Your response:", 
                    key="user_input",
                    placeholder="Type your message here...",
                    label_visibility="collapsed"
                )
                col_input1, col_input2 = st.columns([6, 1])
                with col_input2:
                    submitted = st.form_submit_button("Send 📤", use_container_width=True)
                
                # Handle input if form is submitted
                if submitted and user_input.strip():
                    handle_user_input(user_input)
                    st.rerun()
        else:
            st.success("🎉 Interview session completed successfully!")
            
            # Final actions
            col_final1, col_final2 = st.columns(2)
            with col_final1:
                if st.button("📊 View Summary", use_container_width=True):
                    st.session_state.current_stage = "generate_questions"
                    handle_user_input("summary")
                    st.rerun()
            
            with col_final2:
                if st.button("🔄 New Session", use_container_width=True):
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.rerun()
        
        # Quick actions
        if st.session_state.current_stage == "generate_questions":
            st.markdown("**Quick Actions:**")
            col_q1, col_q2, col_q3 = st.columns(3)
            
            with col_q1:
                if st.button("📋 Summary", use_container_width=True):
                    handle_user_input("summary")
                    st.rerun()
            
            with col_q2:
                if st.button("➕ More Questions", use_container_width=True):
                    handle_user_input("next")
                    st.rerun()
            
            with col_q3:
                if st.button("✅ Finish", use_container_width=True):
                    handle_user_input("done")
                    st.rerun()

if __name__ == "__main__":
    main()