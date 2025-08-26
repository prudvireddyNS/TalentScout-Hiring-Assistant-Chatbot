from config.config import Config

class PromptEngineering:
    """Handles the creation and management of prompts for the LLM."""
    
    def __init__(self):
        """Initialize the prompt engineering module."""
        # System prompt that defines the chatbot's identity and behavior
        self.system_prompt = f"""
        You are the {Config.APP_NAME}, an AI chatbot designed to help with the initial screening of candidates 
        for technical positions. Your goal is to gather essential information from candidates and assess their technical 
        proficiency through relevant questions.
        
        Guidelines for your behavior:
        1. Be professional, friendly, and conversational
        2. Stay focused on the recruitment process
        3. Ask clear, concise questions
        4. Provide helpful responses to candidate questions
        5. Maintain context throughout the conversation
        6. If you don't understand a response, ask for clarification
        7. Do not ask for sensitive personal information beyond basic contact details
        8. Be respectful of the candidate's time and experience
        
        {Config.PRIVACY_DISCLAIMER}
        """
    
    def create_greeting_prompt(self):
        """Create a prompt for the initial greeting.
        
        Returns:
            str: The greeting prompt
        """
        prompt = f"{self.system_prompt}\n\nCreate a friendly greeting for a candidate who has just started interacting with the TalentScout Hiring Assistant. Introduce yourself and explain your purpose."
        return prompt
    
    def create_information_gathering_prompt(self, info_type, previous_info=None):
        """Create a prompt for gathering specific candidate information.
        
        Args:
            info_type (str): The type of information to gather (e.g., 'name', 'email')
            previous_info (dict, optional): Previously gathered information
            
        Returns:
            str: The information gathering prompt
        """
        context = ""
        if previous_info:
            context = "The candidate has already provided the following information:\n"
            for key, value in previous_info.items():
                if key != info_type and value:  # Don't include the current info type
                    context += f"- {key.capitalize()}: {value}\n"
        
        prompt = f"{self.system_prompt}\n\n{context}\n\nCreate a polite question to ask the candidate for their {info_type}."
        return prompt
    
    def create_tech_stack_prompt(self, candidate_info):
        """Create a prompt for asking about the candidate's tech stack.
        
        Args:
            candidate_info (dict): Previously gathered candidate information
            
        Returns:
            str: The tech stack prompt
        """
        context = "The candidate has provided the following information:\n"
        for key, value in candidate_info.items():
            context += f"- {key.capitalize()}: {value}\n"
        
        prompt = f"{self.system_prompt}\n\n{context}\n\nCreate a question asking the candidate to specify their tech stack, including programming languages, frameworks, databases, and tools they are proficient in."
        return prompt
    
    def create_technical_questions_prompt(self, tech_stack):
        """Create a prompt for generating technical questions based on the tech stack.
        
        Args:
            tech_stack (list): The candidate's tech stack
            
        Returns:
            str: The technical questions prompt
        """
        tech_list = ", ".join(tech_stack)
        
        prompt = f"{self.system_prompt}\n\nThe candidate has specified proficiency in the following technologies: {tech_list}.\n\nGenerate 3-5 technical questions for each technology that would help assess the candidate's proficiency. The questions should be challenging but appropriate for an initial screening."
        return prompt
    
    def create_follow_up_prompt(self, conversation_history, candidate_info, tech_stack, user_input):
        """Create a prompt for generating a follow-up response.
        
        Args:
            conversation_history (list): The conversation history
            candidate_info (dict): The candidate's information
            tech_stack (list): The candidate's tech stack
            user_input (str): The user's latest input
            
        Returns:
            str: The follow-up prompt
        """
        # Create context from candidate info
        context = "Candidate Information:\n"
        for key, value in candidate_info.items():
            context += f"- {key.capitalize()}: {value}\n"
        
        context += f"\nTech Stack: {', '.join(tech_stack)}\n\n"
        
        # Add recent conversation history (last 3 exchanges)
        context += "Recent Conversation:\n"
        recent_history = conversation_history[-6:] if len(conversation_history) > 6 else conversation_history
        for message in recent_history:
            role = "Assistant" if message["role"] == "assistant" else "Candidate"
            context += f"{role}: {message['content']}\n"
        
        # Add the current user input
        context += f"\nCandidate's latest response: {user_input}\n"
        
        prompt = f"{self.system_prompt}\n\n{context}\n\nGenerate a thoughtful, professional response that continues the technical assessment conversation. Your response should acknowledge the candidate's answer, provide relevant insights or follow-up questions, and maintain a friendly tone."
        return prompt
    
    def create_conversation_ending_prompt(self, candidate_info):
        """Create a prompt for generating a conversation ending message.
        
        Args:
            candidate_info (dict): The candidate's information
            
        Returns:
            str: The conversation ending prompt
        """
        context = "The candidate has provided the following information:\n"
        for key, value in candidate_info.items():
            context += f"- {key.capitalize()}: {value}\n"
        
        prompt = f"{self.system_prompt}\n\n{context}\n\nThe conversation with the candidate is ending. Generate a polite message thanking them for their time, informing them about next steps in the recruitment process, and concluding the conversation professionally."
        return prompt
    
    def create_fallback_prompt(self, conversation_history, user_input):
        """Create a prompt for generating a fallback response when the input is unexpected.
        
        Args:
            conversation_history (list): The conversation history
            user_input (str): The user's latest input
            
        Returns:
            str: The fallback prompt
        """
        # Add recent conversation history (last 3 exchanges)
        context = "Recent Conversation:\n"
        recent_history = conversation_history[-6:] if len(conversation_history) > 6 else conversation_history
        for message in recent_history:
            role = "Assistant" if message["role"] == "assistant" else "Candidate"
            context += f"{role}: {message['content']}\n"
        
        # Add the current user input
        context += f"\nCandidate's latest response: {user_input}\n"
        
        prompt = f"{self.system_prompt}\n\n{context}\n\nThe candidate's response is unexpected or unclear. Generate a polite response that acknowledges their message, asks for clarification if needed, and gently guides the conversation back to the recruitment screening process."
        return prompt