
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Configuration class to manage environment variables and settings.
    """
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # ChromaDB Persist Directory
    CHROMA_PERSIST_DIRECTORY = os.path.join(os.getcwd(), "chroma_db")

    @staticmethod
    def validate():
        """
        Validates that critical environment variables are set.
        Raises ValueError if keys are missing.
        """
        if not Config.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is missing. Please add it to the .env file.")
