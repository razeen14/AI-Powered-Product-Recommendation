# backend/config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration settings
class Config:
    """Config class for the application"""

    # 'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
    # 'MODEL_NAME': os.getenv('MODEL_NAME', 'gpt-3.5-turbo'),
    # 'MAX_TOKENS': int(os.getenv('MAX_TOKENS', 1000)),
    # 'TEMPERATURE': float(os.getenv('TEMPERATURE', 0.7)),
    # 'DATA_PATH': os.getenv('DATA_PATH', 'data/products.json')

    # OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    # MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME", "gemma2-9b-it")
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1000"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

    DATA_PATH = os.getenv("DATA_PATH", "data/products.json")

    API_PREFIX = "/api"

    @classmethod
    def validate(cls):
        """Validate that all req config is present"""

        if not cls.GROQ_API_KEY:
            raise ValueError("GROQ API KEY is req in .env file")
        
        if not os.path.exists(cls.DATA_PATH):
            raise ValueError(f"Product data file not found at {cls.DATA_PATH}")
        
config = Config()