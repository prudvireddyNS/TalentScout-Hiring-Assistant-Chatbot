import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration settings for the TalentScout chatbot."""
    
    # API settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-3.5-turbo")
    
    # Application settings
    APP_NAME = "TalentScout Hiring Assistant"
    APP_DESCRIPTION = "AI-powered recruitment assistant for technical screening"
    
    # Data settings
    DATA_DIR = os.getenv("DATA_DIR", "data")
    
    # Conversation settings
    MAX_HISTORY_LENGTH = 20  # Maximum number of messages to keep in history
    DEFAULT_TEMPERATURE = 0.7  # Temperature for LLM responses
    
    # Technical question settings
    QUESTIONS_PER_TECH = 3  # Number of questions to generate per technology
    
    # Privacy settings
    PRIVACY_DISCLAIMER = (
        "Your information will be processed in accordance with our privacy policy. "
        "We collect only the information necessary for the recruitment process."
    )
    
    # Fallback messages
    FALLBACK_MESSAGE = (
        "I'm sorry, I didn't quite understand that. Could you please rephrase or provide more details? "
        "I'm here to help with your technical screening process."
    )
    
    # End conversation keywords
    END_CONVERSATION_KEYWORDS = [
        "exit", "quit", "bye", "goodbye", "end", "stop"
    ]
    
    @staticmethod
    def validate_config():
        """Validate that all required configuration settings are present.
        
        Returns:
            tuple: (is_valid, error_message)
        """
        if not Config.OPENAI_API_KEY:
            return False, "OPENAI_API_KEY is not set. Please add it to your .env file."
        
        return True, "Configuration is valid."