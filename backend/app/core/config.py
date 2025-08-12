import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Google Gemini Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyCDU4XLGIx8EM7Jxy0RHcoovmV9e1Wat2c")
    
    # ChromaDB Configuration
    CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_data")
    CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "debugger_errors")
    
    # Reddit Configuration
    REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
    REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
    REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "agent-debugger-ai")
    
    # Application Configuration
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
      # Vector Database Configuration
    VECTOR_DB_DIMENSION = int(os.getenv("VECTOR_DB_DIMENSION", "768"))  # for Gemini embeddings
      # Search Configuration
    MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "10"))
    MAX_VECTOR_RESULTS = int(os.getenv("MAX_VECTOR_RESULTS", "5"))
    
    def validate(self):
        """Validate that required environment variables are set"""
        required_vars = [
            ("GEMINI_API_KEY", self.GEMINI_API_KEY),
        ]
        
        optional_vars = [
            ("REDDIT_CLIENT_ID", self.REDDIT_CLIENT_ID),
            ("REDDIT_CLIENT_SECRET", self.REDDIT_CLIENT_SECRET),
        ]
        
        missing_required = [var_name for var_name, var_value in required_vars if not var_value]
        missing_optional = [var_name for var_name, var_value in optional_vars if not var_value]
        
        if missing_required:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_required)}")
        
        if missing_optional:
            print(f"Warning: Missing optional environment variables: {', '.join(missing_optional)}")
            print("Some features may not work without these variables.")
        
        # Ensure ChromaDB directory exists
        try:
            os.makedirs(self.CHROMA_DB_PATH, exist_ok=True)
        except Exception as e:
            print(f"Warning: Could not create ChromaDB directory {self.CHROMA_DB_PATH}: {e}")

settings = Settings()

# Validate configuration on import
try:
    settings.validate()
except ValueError as e:
    print(f"Configuration error: {e}")
    print("Please check your .env file and ensure all required variables are set.")