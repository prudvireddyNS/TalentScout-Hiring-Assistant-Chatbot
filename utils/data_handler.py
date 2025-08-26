import os
import json
import pandas as pd
from datetime import datetime
from config.config import Config

class DataHandler:
    """Handles data processing and storage for the TalentScout chatbot."""
    
    def __init__(self, data_dir=None):
        """Initialize the data handler.
        
        Args:
            data_dir (str, optional): Directory to store data files. Defaults to Config.DATA_DIR.
        """
        self.data_dir = data_dir if data_dir else Config.DATA_DIR
        
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
    
    def save_candidate_data(self, candidate_info, tech_stack, conversation_history):
        """Save candidate data to a JSON file.
        
        Args:
            candidate_info (dict): The candidate's information
            tech_stack (list): The candidate's tech stack
            conversation_history (list): The conversation history
            
        Returns:
            str: Path to the saved file
        """
        # Create a unique filename based on candidate name and timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name_slug = candidate_info.get("name", "anonymous").lower().replace(" ", "_")
        filename = f"{name_slug}_{timestamp}.json"
        file_path = os.path.join(self.data_dir, filename)
        
        # Prepare data for saving
        data = {
            "candidate_info": candidate_info,
            "tech_stack": tech_stack,
            "conversation_history": conversation_history,
            "timestamp": timestamp
        }
        
        # Save to JSON file
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
        
        return file_path
    
    def load_candidate_data(self, file_path):
        """Load candidate data from a JSON file.
        
        Args:
            file_path (str): Path to the JSON file
            
        Returns:
            dict: The loaded data
        """
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"Error loading candidate data: {e}")
            return None
    
    def get_all_candidates(self):
        """Get a list of all saved candidates.
        
        Returns:
            list: List of candidate data dictionaries
        """
        candidates = []
        
        # Check if data directory exists
        if not os.path.exists(self.data_dir):
            return candidates
        
        # Load all JSON files in the data directory
        for filename in os.listdir(self.data_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(self.data_dir, filename)
                data = self.load_candidate_data(file_path)
                if data:
                    candidates.append(data)
        
        return candidates
    
    def export_to_csv(self, output_path="candidates.csv"):
        """Export all candidate data to a CSV file.
        
        Args:
            output_path (str): Path to save the CSV file
            
        Returns:
            bool: True if export was successful, False otherwise
        """
        try:
            candidates = self.get_all_candidates()
            
            if not candidates:
                return False
            
            # Extract relevant information for CSV
            csv_data = []
            for candidate in candidates:
                info = candidate.get("candidate_info", {})
                tech = ", ".join(candidate.get("tech_stack", []))
                timestamp = candidate.get("timestamp", "")
                
                row = {
                    "Name": info.get("name", ""),
                    "Email": info.get("email", ""),
                    "Phone": info.get("phone", ""),
                    "Experience": info.get("experience", ""),
                    "Position": info.get("position", ""),
                    "Location": info.get("location", ""),
                    "Tech Stack": tech,
                    "Timestamp": timestamp
                }
                
                csv_data.append(row)
            
            # Create DataFrame and save to CSV
            df = pd.DataFrame(csv_data)
            df.to_csv(output_path, index=False)
            
            return True
        
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False
    
    def anonymize_data(self, data):
        """Anonymize sensitive candidate data for privacy.
        
        Args:
            data (dict): The candidate data to anonymize
            
        Returns:
            dict: Anonymized data
        """
        # Create a copy to avoid modifying the original
        anonymized = data.copy()
        
        # Anonymize sensitive fields in candidate_info
        if "candidate_info" in anonymized:
            info = anonymized["candidate_info"]
            
            if "name" in info:
                # Replace name with initials
                name_parts = info["name"].split()
                initials = "".join([part[0] for part in name_parts if part])
                info["name"] = f"{initials}****"
            
            if "email" in info:
                # Replace email with partial masking
                email_parts = info["email"].split("@")
                if len(email_parts) == 2:
                    username = email_parts[0]
                    domain = email_parts[1]
                    masked_username = username[0] + "*" * (len(username) - 2) + username[-1] if len(username) > 2 else username
                    info["email"] = f"{masked_username}@{domain}"
            
            if "phone" in info:
                # Mask phone number
                phone = info["phone"]
                if len(phone) > 4:
                    info["phone"] = "*" * (len(phone) - 4) + phone[-4:]
        
        return anonymized