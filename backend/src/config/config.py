import os
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = "sbi-life-conversations-index"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


print(f"Config: PINECONE_API_KEY is set to: {PINECONE_API_KEY is not None}") 
if PINECONE_API_KEY:
    print(f"Config: PINECONE_API_KEY (first 8 chars): {PINECONE_API_KEY[:8]}...") 
else:
    print("Config: PINECONE_API_KEY is EMPTY")

print(f"Config: PINECONE_ENVIRONMENT is set to: {PINECONE_ENVIRONMENT is not None}") 
if PINECONE_ENVIRONMENT:
    print(f"Config: PINECONE_ENVIRONMENT: {PINECONE_ENVIRONMENT}") 
else:
    print("Config: PINECONE_ENVIRONMENT is EMPTY")

print(f"Config: PINECONE_INDEX_NAME: {PINECONE_INDEX_NAME}") 

if not OPENAI_API_KEY:
    print("Warning: OPENAI_API_KEY is not set in environment variables. OpenAI functionality will be limited.") 