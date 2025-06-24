import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Google Gemini Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyCDU4XLGIx8EM7Jxy0RHcoovmV9e1Wat2c")
    
    # Pinecone Configuration
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENV = os.getenv("PINECONE_ENV", "us-west1-gcp")
    
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
            ("PINECONE_API_KEY", self.PINECONE_API_KEY),
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

settings = Settings()

# Validate configuration on import
try:
    settings.validate()
except ValueError as e:
    print(f"Configuration error: {e}")
    print("Please check your .env file and ensure all required variables are set.")