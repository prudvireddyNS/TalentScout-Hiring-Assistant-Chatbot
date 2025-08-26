import re

class CandidateInfoCollector:
    """Handles the collection and validation of candidate information."""
    
    def __init__(self):
        """Initialize the candidate information collector."""
        pass
    
    def validate_email(self, email):
        """Validate an email address format.
        
        Args:
            email (str): The email address to validate
            
        Returns:
            bool: True if the email is valid, False otherwise
        """
        # Basic email validation pattern
        pattern = r'^[\w\.-]+@([\w\-]+\.)+[A-Za-z]{2,}$'
        return bool(re.match(pattern, email))
    
    def validate_phone(self, phone):
        """Validate a phone number format.
        
        Args:
            phone (str): The phone number to validate
            
        Returns:
            bool: True if the phone number is valid, False otherwise
        """
        # Remove common separators and spaces
        cleaned_phone = re.sub(r'[\s\-\(\)\.]', '', phone)
        
        # Check if it's a valid phone number (basic check for length and digits)
        return bool(re.match(r'^\+?\d{10,15}$', cleaned_phone))
    
    def parse_tech_stack(self, tech_stack_input):
        """Parse the tech stack input into a list of technologies.
        
        Args:
            tech_stack_input (str): The raw tech stack input from the user
            
        Returns:
            list: A list of individual technologies
        """
        # Split by commas, semicolons, or 'and'
        separators = r'[,;]|\sand\s'
        technologies = re.split(separators, tech_stack_input)
        
        # Clean up each technology name
        cleaned_technologies = [tech.strip() for tech in technologies if tech.strip()]
        
        return cleaned_technologies
    
    def format_candidate_info(self, candidate_info):
        """Format the candidate information for display or storage.
        
        Args:
            candidate_info (dict): The candidate's information
            
        Returns:
            str: Formatted candidate information
        """
        formatted_info = "**Candidate Information**\n\n"
        
        if 'name' in candidate_info:
            formatted_info += f"**Name:** {candidate_info['name']}\n"
        
        if 'email' in candidate_info:
            formatted_info += f"**Email:** {candidate_info['email']}\n"
        
        if 'phone' in candidate_info:
            formatted_info += f"**Phone:** {candidate_info['phone']}\n"
        
        if 'experience' in candidate_info:
            formatted_info += f"**Experience:** {candidate_info['experience']}\n"
        
        if 'position' in candidate_info:
            formatted_info += f"**Desired Position:** {candidate_info['position']}\n"
        
        if 'location' in candidate_info:
            formatted_info += f"**Location:** {candidate_info['location']}\n"
        
        return formatted_info
    
    def store_candidate_info(self, candidate_info, tech_stack):
        """Store the candidate information (simulated).
        
        In a real application, this would store the data in a database or file.
        For this demo, we'll just return a success message.
        
        Args:
            candidate_info (dict): The candidate's information
            tech_stack (list): The candidate's tech stack
            
        Returns:
            bool: True if storage was successful
        """
        # In a real application, you would store this information securely
        # For this demo, we'll just return True to simulate successful storage
        return True