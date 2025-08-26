import re
from utils.llm_utils import get_llm_response
from config.config import Config

class ConversationManager:
    """Manages the conversation flow and context for the TalentScout chatbot."""
    
    def __init__(self):
        """Initialize the conversation manager with conversation history."""
        self.conversation_history = []
        self.end_conversation_keywords = Config.END_CONVERSATION_KEYWORDS
    
    def add_to_history(self, role, content):
        """Add a message to the conversation history.
        
        Args:
            role (str): The role of the message sender ("user" or "assistant")
            content (str): The content of the message
        """
        self.conversation_history.append({"role": role, "content": content})
    
    def get_greeting(self):
        """Generate the initial greeting message.
        
        Returns:
            str: The greeting message
        """
        greeting = (
            "👋 Hello! I'm the TalentScout Hiring Assistant. I'm here to help with your initial screening for tech positions. "
            "I'll ask you a few questions about your background and technical skills, then provide some technical questions "
            "based on your expertise. Let's get started!"
        )
        self.add_to_history("assistant", greeting)
        return greeting
    
    def get_name_prompt(self):
        """Generate the prompt to ask for the candidate's name.
        
        Returns:
            str: The name prompt message
        """
        prompt = "First, could you please tell me your full name?"
        self.add_to_history("assistant", prompt)
        return prompt
    
    def get_email_prompt(self):
        """Generate the prompt to ask for the candidate's email.
        
        Returns:
            str: The email prompt message
        """
        prompt = "Great! Now, could you please provide your email address where we can contact you?"
        self.add_to_history("assistant", prompt)
        return prompt
    
    def get_phone_prompt(self):
        """Generate the prompt to ask for the candidate's phone number.
        
        Returns:
            str: The phone prompt message
        """
        prompt = "Thank you. Could you please share your phone number?"
        self.add_to_history("assistant", prompt)
        return prompt
    
    def get_experience_prompt(self):
        """Generate the prompt to ask for the candidate's years of experience.
        
        Returns:
            str: The experience prompt message
        """
        prompt = "How many years of professional experience do you have in the tech industry?"
        self.add_to_history("assistant", prompt)
        return prompt
    
    def get_position_prompt(self):
        """Generate the prompt to ask for the candidate's desired position.
        
        Returns:
            str: The position prompt message
        """
        prompt = "What position(s) are you interested in applying for at TalentScout?"
        self.add_to_history("assistant", prompt)
        return prompt
    
    def get_location_prompt(self):
        """Generate the prompt to ask for the candidate's current location.
        
        Returns:
            str: The location prompt message
        """
        prompt = "What is your current location? (City and Country)"
        self.add_to_history("assistant", prompt)
        return prompt
    
    def get_tech_stack_prompt(self):
        """Generate the prompt to ask for the candidate's tech stack.
        
        Returns:
            str: The tech stack prompt message
        """
        prompt = (
            "Please list your tech stack, including programming languages, frameworks, databases, and tools you are proficient in. "
            "For example: 'Python, Django, React, PostgreSQL, Docker'"
        )
        self.add_to_history("assistant", prompt)
        return prompt
    
    def format_questions(self, questions):
        """Format the generated technical questions for display.
        
        Args:
            questions (dict): Dictionary of technology-question pairs
            
        Returns:
            str: Formatted questions message
        """
        message = "Based on your tech stack, I'd like to ask you a few technical questions:\n\n"
        
        for tech, tech_questions in questions.items():
            message += f"**{tech}**:\n"
            for i, question in enumerate(tech_questions, 1):
                message += f"{i}. {question}\n"
            message += "\n"
        
        message += "Please feel free to answer these questions. Take your time and provide as much detail as you'd like."
        
        self.add_to_history("assistant", message)
        return message
    
    def is_conversation_ending(self, user_input):
        """Check if the user input contains conversation ending keywords.
        
        Args:
            user_input (str): The user's input message
            
        Returns:
            bool: True if the conversation should end, False otherwise
        """
        user_input_lower = user_input.lower()
        
        # Check if any ending keyword is in the user input
        for keyword in self.end_conversation_keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', user_input_lower):
                return True
        
        return False
    
    def get_end_conversation_message(self):
        """Generate the end conversation message.
        
        Returns:
            str: The end conversation message
        """
        message = (
            "Thank you for taking the time to chat with me today! Your information has been recorded. "
            "A recruiter will review your responses and get back to you soon if there's a potential match. "
            "If you have any questions in the meantime, please feel free to reach out. "
            "Have a great day!"
        )
        self.add_to_history("assistant", message)
        return message
    
    def create_follow_up_prompt(self, user_input, candidate_info, tech_stack):
        """Create a prompt for the LLM to generate a follow-up response.
        
        Args:
            user_input (str): The user's input message
            candidate_info (dict): The candidate's information
            tech_stack (list): The candidate's tech stack
            
        Returns:
            str: The prompt for the LLM
        """
        # Add the user input to history
        self.add_to_history("user", user_input)
        
        # Create a system prompt that includes context about the conversation
        system_prompt = f"""
        You are the {Config.APP_NAME}, an AI chatbot helping with technical recruitment screening.
        
        Candidate Information:
        - Name: {candidate_info.get('name', 'Unknown')}
        - Position: {candidate_info.get('position', 'Unknown')}
        - Experience: {candidate_info.get('experience', 'Unknown')}
        - Tech Stack: {', '.join(tech_stack)}
        
        The candidate has answered some technical questions. Provide a thoughtful, professional response that:
        1. Acknowledges their answer
        2. Provides additional insights or follow-up questions related to their response
        3. Stays focused on technical assessment
        4. Maintains a friendly, conversational tone
        
        Do not introduce new topics unrelated to the technical assessment or the candidate's background.
        If the candidate asks about next steps or the hiring process, provide general information about TalentScout's process.
        """
        
        # Create a prompt that includes the conversation history
        prompt = system_prompt + "\n\nConversation History:\n"
        
        # Add the last few exchanges from conversation history
        max_messages = Config.MAX_HISTORY_LENGTH * 2  # Each exchange has 2 messages (user and assistant)
        for message in self.conversation_history[-max_messages:]:
            prompt += f"\n{message['role'].upper()}: {message['content']}"
        
        # Add the current user input
        prompt += f"\n\nUser's latest response: {user_input}\n\nYour response:"
        
        return prompt