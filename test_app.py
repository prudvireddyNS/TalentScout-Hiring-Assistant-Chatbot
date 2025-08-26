import unittest
from modules.conversation import ConversationManager
from modules.candidate_info import CandidateInfoCollector
from modules.tech_questions import TechQuestionGenerator
from modules.prompt_engineering import PromptEngineering
from utils.data_handler import DataHandler
from config.config import Config

class TestTalentScoutApp(unittest.TestCase):
    """Test cases for the TalentScout Hiring Assistant application."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.conversation_manager = ConversationManager()
        self.candidate_collector = CandidateInfoCollector()
        self.question_generator = TechQuestionGenerator()
        self.prompt_engineering = PromptEngineering()
        self.data_handler = DataHandler(data_dir="test_data")
    
    def test_conversation_manager(self):
        """Test the ConversationManager class."""
        # Test greeting
        greeting = self.conversation_manager.get_greeting()
        self.assertIsInstance(greeting, str)
        self.assertGreater(len(greeting), 0)
        
        # Test prompts
        name_prompt = self.conversation_manager.get_name_prompt()
        self.assertIsInstance(name_prompt, str)
        self.assertGreater(len(name_prompt), 0)
        
        # Test conversation ending detection
        self.assertTrue(self.conversation_manager.is_conversation_ending("goodbye"))
        self.assertTrue(self.conversation_manager.is_conversation_ending("Thank you for your time"))
        self.assertFalse(self.conversation_manager.is_conversation_ending("I have 5 years of experience"))
    
    def test_candidate_info_collector(self):
        """Test the CandidateInfoCollector class."""
        # Test email validation
        self.assertTrue(self.candidate_collector.validate_email("test@example.com"))
        self.assertFalse(self.candidate_collector.validate_email("invalid-email"))
        
        # Test phone validation
        self.assertTrue(self.candidate_collector.validate_phone("+1234567890"))
        self.assertTrue(self.candidate_collector.validate_phone("123-456-7890"))
        self.assertFalse(self.candidate_collector.validate_phone("123"))
        
        # Test tech stack parsing
        tech_stack = self.candidate_collector.parse_tech_stack("Python, JavaScript, React, and MongoDB")
        self.assertEqual(len(tech_stack), 4)
        self.assertIn("Python", tech_stack)
        self.assertIn("JavaScript", tech_stack)
        self.assertIn("React", tech_stack)
        self.assertIn("MongoDB", tech_stack)
    
    def test_tech_question_generator(self):
        """Test the TechQuestionGenerator class."""
        # Test question generation from templates
        tech_stack = ["Python", "JavaScript", "React"]
        questions = self.question_generator.generate_questions_from_templates(tech_stack, 2)
        
        self.assertEqual(len(questions), 3)  # One entry per technology
        self.assertEqual(len(questions["Python"]), 2)  # Two questions per technology
        self.assertEqual(len(questions["JavaScript"]), 2)
        self.assertEqual(len(questions["React"]), 2)
        
        # Test technology name normalization
        self.assertEqual(self.question_generator.normalize_tech_name("js"), "javascript")
        self.assertEqual(self.question_generator.normalize_tech_name("reactjs"), "react")
        self.assertEqual(self.question_generator.normalize_tech_name("unknown_tech"), "unknown_tech")
    
    def test_prompt_engineering(self):
        """Test the PromptEngineering class."""
        # Test prompt creation
        greeting_prompt = self.prompt_engineering.create_greeting_prompt()
        self.assertIsInstance(greeting_prompt, str)
        self.assertGreater(len(greeting_prompt), 0)
        
        # Test info gathering prompt
        info_prompt = self.prompt_engineering.create_information_gathering_prompt("email")
        self.assertIsInstance(info_prompt, str)
        self.assertGreater(len(info_prompt), 0)
        
        # Test with previous info
        previous_info = {"name": "John Doe", "phone": "123-456-7890"}
        info_prompt_with_context = self.prompt_engineering.create_information_gathering_prompt("email", previous_info)
        self.assertIsInstance(info_prompt_with_context, str)
        self.assertGreater(len(info_prompt_with_context), 0)
        
    def test_config(self):
        """Test the Config class."""
        # Test config validation
        is_valid, _ = Config.validate_config()
        # Note: This might fail if OPENAI_API_KEY is not set in the environment
        # self.assertTrue(is_valid)
        
        # Test config values
        self.assertEqual(Config.APP_NAME, "TalentScout Hiring Assistant")
        self.assertEqual(Config.QUESTIONS_PER_TECH, 3)
        self.assertIsInstance(Config.END_CONVERSATION_KEYWORDS, list)
        self.assertGreater(len(Config.END_CONVERSATION_KEYWORDS), 0)

if __name__ == "__main__":
    unittest.main()
