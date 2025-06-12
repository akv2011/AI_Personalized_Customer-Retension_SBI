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

# --- PostgreSQL MCP Configuration ---
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://sbi_user:sbi_password@localhost:5432/sbi_personalization")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "sbi_personalization")
POSTGRES_USER = os.getenv("POSTGRES_USER", "sbi_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "sbi_password")

# --- MCP Server Configuration ---
MCP_SERVER_NAME = os.getenv("MCP_SERVER_NAME", "sbi-postgres-mcp")
MCP_SERVER_COMMAND = "mcp-server-postgres"
MCP_SERVER_ARGS = [DATABASE_URL]

# --- Other Configurations (if any) ---
# Example: Default language
DEFAULT_LANGUAGE = "en"

# --- Validation (Optional but recommended) ---
# You might want to add checks here to ensure necessary keys are set
# if not GOOGLE_API_KEY:
#     print("Warning: GOOGLE_API_KEY environment variable not set.")
# if not OPENAI_API_KEY:
#     print("Warning: OPENAI_API_KEY environment variable not set.")