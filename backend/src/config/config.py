import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# --- API Keys ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") # Add Google API Key

# --- FAISS Configuration ---
# Define the path for the FAISS index file relative to the backend directory
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Points to the 'src' directory's parent
FAISS_INDEX_PATH = os.path.join(BACKEND_DIR, "faiss_index.idx")
SYSTEM_PROMPT_PATH = os.path.join(os.path.dirname(__file__), "system_prompt.txt") # Path to the system prompt file

# --- Other Configurations (if any) ---
# Example: Default language
DEFAULT_LANGUAGE = "en"

# --- Validation (Optional but recommended) ---
# You might want to add checks here to ensure necessary keys are set
# if not GOOGLE_API_KEY:
#     print("Warning: GOOGLE_API_KEY environment variable not set.")
# if not OPENAI_API_KEY:
#     print("Warning: OPENAI_API_KEY environment variable not set.")