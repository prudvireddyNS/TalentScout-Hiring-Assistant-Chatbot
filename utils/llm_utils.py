import json
from openai import OpenAI
from config.config import Config

# Set up OpenAI API key
client = OpenAI(api_key=Config.OPENAI_API_KEY)

def get_llm_response(prompt, model=Config.DEFAULT_MODEL, temperature=Config.DEFAULT_TEMPERATURE, max_tokens=1000, response_format=None):
    """Get a response from the language model.
    
    Args:
        prompt (str): The prompt to send to the model
        model (str): The model to use
        temperature (float): The temperature parameter for generation
        max_tokens (int): The maximum number of tokens to generate
        response_format (str, optional): The format of the response (e.g., "json")
        
    Returns:
        str or dict: The model's response, either as a string or parsed JSON
    """
    try:
        params = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        if response_format == "json":
            params["response_format"] = {"type": "json_object"}   

        response = client.chat.completions.create(**params)

        content = response.choices[0].message.content

        if response_format == "json":
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                print("Warning: Response was not valid JSON. Returning raw content.")
                return content

        return content

    except Exception as e:
        print(f"Error getting LLM response: {e}")
        return {} if response_format == "json" else Config.FALLBACK_MESSAGE

def create_chat_completion(messages, model=Config.DEFAULT_MODEL, temperature=Config.DEFAULT_TEMPERATURE, max_tokens=1000):
    """Create a chat completion with a series of messages.
    
    Args:
        messages (list): List of message dictionaries with 'role' and 'content'
        model (str): The model to use
        temperature (float): The temperature parameter for generation
        max_tokens (int): The maximum number of tokens to generate
        
    Returns:
        str: The model's response
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error creating chat completion: {e}")
        return Config.FALLBACK_MESSAGE