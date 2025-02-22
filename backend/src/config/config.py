import os
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = "sbi-life-conversations-index"

print(f"Config: PINECONE_API_KEY is set to: {PINECONE_API_KEY is not None}") # Check if API_KEY is None or not
if PINECONE_API_KEY:
    print(f"Config: PINECONE_API_KEY (first 8 chars): {PINECONE_API_KEY[:8]}...") # Print first 8 chars if it's set
else:
    print("Config: PINECONE_API_KEY is EMPTY")

print(f"Config: PINECONE_ENVIRONMENT is set to: {PINECONE_ENVIRONMENT is not None}") # Check if ENVIRONMENT is None or not
if PINECONE_ENVIRONMENT:
    print(f"Config: PINECONE_ENVIRONMENT: {PINECONE_ENVIRONMENT}") # Print Environment if it's set
else:
    print("Config: PINECONE_ENVIRONMENT is EMPTY")

print(f"Config: PINECONE_INDEX_NAME: {PINECONE_INDEX_NAME}") # Print Index Name