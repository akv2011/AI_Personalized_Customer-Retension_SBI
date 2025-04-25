import os
import sys

# Add the 'src' directory to the Python path
# This allows absolute imports from 'src' (e.g., from src.api.app import app)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# --- PDF Processing Imports ---
from utils.pdf_processor import extract_text_from_pdf # Assuming this function exists
from embedding_service.embedding_generator import EmbeddingGenerator
from vector_database.vector_db_client import VectorDBClient
# --- End PDF Processing Imports ---

from api.app import app

# --- Function to process PDF on startup ---
def process_pdf_on_startup(pdf_path):
    """Extracts text, generates embeddings, and stores them in FAISS."""
    print(f"--- Processing initial PDF: {pdf_path} ---")
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}")
        return

    try:
        print("Initializing components...")
        vector_db = VectorDBClient()
        embed_gen = EmbeddingGenerator()

        print("Extracting text from PDF...")
        # Assuming extract_text_from_pdf returns a list of text chunks
        text_chunks = extract_text_from_pdf(pdf_path)
        if not text_chunks:
            print("No text extracted from PDF.")
            return

        print(f"Extracted {len(text_chunks)} text chunks. Generating and storing embeddings...")
        processed_chunks = 0
        for i, chunk in enumerate(text_chunks):
            if not chunk.strip(): # Skip empty chunks
                continue

            try:
                # Generate a unique ID for the chunk (e.g., filename + chunk index)
                vector_id = f"{os.path.basename(pdf_path)}_chunk_{i}"
                print(f"  Processing chunk {i+1}/{len(text_chunks)} (ID: {vector_id})...")

                # Check if already processed (simple check based on metadata)
                if vector_id in vector_db.id_to_metadata:
                     print(f"    Skipping chunk {i+1}: Already found in vector store.")
                     processed_chunks += 1
                     continue

                embedding = embed_gen.get_embedding(chunk)
                if embedding:
                    # Store the FULL chunk text instead of just a preview
                    metadata = {"source": os.path.basename(pdf_path), "chunk": i, "text": chunk} # Changed 'text_preview' to 'text' and removed slicing
                    success = vector_db.upsert_embedding(vector_id, embedding, metadata)
                    if success:
                        print(f"    Chunk {i+1} stored successfully.")
                        processed_chunks += 1
                    else:
                        print(f"    Failed to store chunk {i+1}.")
                else:
                    print(f"    Failed to generate embedding for chunk {i+1}.")
            except Exception as chunk_error:
                print(f"    Error processing chunk {i+1}: {chunk_error}")

        print(f"--- PDF Processing Finished: {processed_chunks}/{len(text_chunks)} chunks processed and stored. ---")

    except ImportError as ie:
         print(f"Import Error during PDF processing setup: {ie}. Make sure all dependencies are installed and paths are correct.")
    except Exception as e:
        print(f"An error occurred during PDF processing: {e}")
        import traceback
        traceback.print_exc()
# --- End Function ---

if __name__ == '__main__':
    # --- Process the specific PDF before starting the app ---
    # Get the directory containing run.py (backend)
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    # Get the project root directory (one level up from backend)
    project_root = os.path.dirname(backend_dir)
    # Construct the correct path to the PDF relative to the project root
    pdf_to_process = os.path.join(project_root, 'cotext', 'Smart Swadhan Supreme Brochure', 'SBI Life-Smart Swadhan Supreme Brochure_V02.pdf')
    process_pdf_on_startup(pdf_to_process)
    # --- End PDF Processing Call ---

    # Run the Flask app
    print("Starting Flask application...")
    # Make sure host='0.0.0.0' if you need to access it from other devices on your network
    app.run(debug=True, host='127.0.0.1', port=5000)