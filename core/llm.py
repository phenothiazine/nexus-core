
import google.generativeai as genai
from typing import Optional, List, Dict, Any
from core.config import Config

class GeminiClient:
    """
    Wrapper for Google Gemini API.
    """
    def __init__(self, model_name: str = "gemini-3-flash-preview"):
        """
        Initialize the Gemini Client.
        
        Args:
            model_name (str): The model to use (default: "gemini-3-flash-preview").
        """
        try:
            Config.validate()
            genai.configure(api_key=Config.GOOGLE_API_KEY)
            self.model = genai.GenerativeModel(model_name)
        except Exception as e:
            print(f"Error initializing Gemini Client: {e}")
            raise e

    def generate(self, prompt: str) -> str:
        """
        Generate content from Gemini based on a prompt.
        
        Args:
            prompt (str): The input prompt.
            
        Returns:
            str: The generated text response.
        """
        try:
            response = self.model.generate_content(prompt)
            # Safely extract text from response
            if response and response.candidates and len(response.candidates) > 0:
                candidate = response.candidates[0]
                if candidate.content and candidate.content.parts and len(candidate.content.parts) > 0:
                    return candidate.content.parts[0].text
            return "I couldn't generate a response. Please try again."
        except Exception as e:
            print(f"Error generating content: {e}")
            return f"Error: {str(e)}"

    def generate_chat(self, parsed_history: List[Dict[str, str]], user_message: str) -> str:
         """
         Generate a response in a chat context. 
         (Note: Implementation can be expanded for full chat history support if needed, 
         but 'generate' is sufficient for the Orchestrator's single-turn logic most times.
         This is a placeholder for more advanced chat flows.)
         """
         # Simplified for this architecture where Orchestrator manages context
         return self.generate(user_message)
