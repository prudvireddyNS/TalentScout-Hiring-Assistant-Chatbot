# TalentScout Hiring Assistant Chatbot

## Project Overview
TalentScout Hiring Assistant is an intelligent chatbot designed for a fictional recruitment agency specializing in technology placements. The chatbot assists in the initial screening of candidates by gathering essential information and posing relevant technical questions based on the candidate's declared tech stack.

## Features
- **Interactive UI**: Clean and intuitive interface built with Streamlit
- **Candidate Information Collection**: Gathers essential details like name, contact information, experience, etc.
- **Tech Stack Assessment**: Prompts candidates to specify their technical proficiencies
- **Dynamic Question Generation**: Creates tailored technical questions based on the candidate's tech stack
- **Context-Aware Conversations**: Maintains conversation flow and context for a seamless experience
- **Fallback Mechanisms**: Provides meaningful responses for unexpected inputs

## Technical Details

### Libraries and Tools Used
- **Python**: Core programming language
- **Streamlit**: Frontend interface development
- **OpenAI API**: For accessing GPT models for intelligent responses
- **dotenv**: For environment variable management
- **pandas**: For data handling (optional)

### Architecture
- **app.py**: Main application entry point
- **modules/**
  - **conversation.py**: Handles conversation flow and context management
  - **candidate_info.py**: Manages candidate information collection and validation
  - **tech_questions.py**: Generates technical questions based on tech stack
- **utils/**
  - **llm_utils.py**: Utilities for interacting with the language model
  - **data_handler.py**: Functions for data processing and storage
- **config/**
  - **config.py**: Configuration settings
  - **.env**: Environment variables (API keys, etc.)
- **static/**
  - CSS and other static assets

## Installation Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Steps
1. Clone the repository or extract the zip file
   ```
   git clone <repository-url>
   cd task
   ```

2. Create and activate a virtual environment (optional but recommended)
   ```
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install required packages
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your OpenAI API key
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

5. Run the application
   ```
   streamlit run app.py
   ```

6. Access the application in your web browser at `http://localhost:8501`

## Usage Guide
1. When the application starts, the chatbot will greet the candidate and explain its purpose
2. The chatbot will guide the candidate through providing their information:
   - Full Name
   - Email Address
   - Phone Number
   - Years of Experience
   - Desired Position(s)
   - Current Location
   - Tech Stack
3. Based on the provided tech stack, the chatbot will generate relevant technical questions
4. The candidate can respond to these questions or ask follow-up questions
5. The conversation will continue until the candidate indicates they want to end it
6. The chatbot will thank the candidate and inform them about next steps

## Prompt Design
The prompts for the chatbot are designed to:
1. **Be Clear and Concise**: Ensure candidates understand what information is being requested
2. **Guide the LLM**: Structure prompts to generate appropriate responses and questions
3. **Maintain Context**: Include relevant context from previous interactions
4. **Handle Edge Cases**: Provide fallback mechanisms for unexpected inputs

The system prompt establishes the chatbot's identity and purpose, while user-facing prompts are conversational and friendly.

## Challenges & Solutions
- **Context Management**: Implemented a conversation history tracker to maintain context across interactions
- **Dynamic Question Generation**: Created a knowledge base of technical concepts to generate relevant questions
- **Data Privacy**: Implemented secure handling of candidate information with appropriate disclaimers
- **Conversation Flow**: Designed state management to guide the conversation while allowing natural interactions

## Future Enhancements
- Sentiment analysis to gauge candidate emotions
- Multilingual support
- Personalized responses based on user history
- Enhanced UI with custom styling
- Cloud deployment for wider accessibility

## License
This project is licensed under the MIT License - see the LICENSE file for details.