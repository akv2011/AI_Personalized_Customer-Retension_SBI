# Implementation Plan: FAISS Integration, PDF Support, and OpenAI Embeddings

This document outlines the steps required to replace the Pinecone vector database with FAISS, add support for processing PDF documents, and use OpenAI for generating embeddings in the backend.

## Phase 1: FAISS Integration & OpenAI Embeddings

1.  **Install Dependencies:**
    *   Add `faiss-cpu` (or `faiss-gpu` if CUDA is available) to `backend/requirements.txt`.
    *   Add `openai` to `backend/requirements.txt`.
    *   Add a PDF parsing library (e.g., `pypdf2` or `pymupdf`) to `backend/requirements.txt`.
    *   Remove `pinecone-client` (if present) from `backend/requirements.txt`.
    *   Run `pip install -r backend/requirements.txt` (or equivalent for your environment).

2.  **Update Configuration (`backend/src/config/config.py`):**
    *   Remove Pinecone API key and environment variables.
    *   Add OpenAI API key configuration.
    *   Add configuration for the FAISS index file path (for persistence).

3.  **Update Embedding Service (`backend/src/embedding_service/embedding_generator.py`):**
    *   Initialize the OpenAI client using the API key from the configuration.
    *   Implement a function to generate embeddings using the OpenAI API (e.g., `text-embedding-ada-002` model).
    *   Modify existing embedding generation logic to use this new function.

4.  **Update Vector Database Client (`backend/src/vector_database/vector_db_client.py`):**
    *   Remove Pinecone initialization logic.
    *   Implement FAISS index initialization (e.g., `faiss.IndexFlatL2`). Determine the dimensionality based on the OpenAI embedding model (e.g., 1536 for `text-embedding-ada-002`).
    *   Implement index persistence: logic to save the FAISS index to the configured file path and load it if it exists.
    *   Replace Pinecone `upsert` logic with FAISS `add` logic. Ensure vectors are added with the correct IDs.
    *   Replace Pinecone `query` logic with FAISS `search` logic.

## Phase 2: PDF Support Integration

1.  **Implement PDF Text Extraction:**
    *   Create a new utility function or modify `backend/src/embedding_service/embedding_generator.py`.
    *   This function should take a PDF file path or file stream as input.
    *   Use the chosen PDF library (`pypdf2`, `pymupdf`) to open the PDF and extract text content.
    *   Consider text cleaning and chunking strategies for large PDFs.
    *   Return the extracted text chunks.

2.  **Integrate PDF Processing into Embedding Workflow:**
    *   Modify the part of the code responsible for generating and storing embeddings (likely triggered from `app.py` and implemented in `embedding_generator.py` and `vector_db_client.py`).
    *   Add logic to handle PDF file uploads (e.g., in an API endpoint in `app.py`).
    *   If the input is a PDF, call the text extraction function.
    *   Generate embeddings for the extracted text chunks using the OpenAI embedding function.
    *   Store these embeddings in the FAISS index using the updated `vector_db_client.py`.

## Phase 3: API and Application Updates

1.  **Update API (`backend/src/api/app.py`):**
    *   Modify or add API endpoints to handle PDF uploads.
    *   Update any existing endpoints that interact with the vector database to use the new FAISS client methods.
    *   Ensure API responses are adjusted based on the FAISS search results.

## Phase 4: Testing

1.  **Unit Tests:** Update existing or create new unit tests for the modified components (`vector_db_client.py`, `embedding_generator.py`, PDF processing utility).
2.  **Integration Tests:** Test the end-to-end flow:
    *   Uploading/processing PDF documents.
    *   Generating embeddings via OpenAI.
    *   Storing embeddings in FAISS.
    *   Querying the FAISS index via the API.
    *   Verify index persistence (saving/loading).

## Phase 5: Personalized Customer Response & Memory

1. **Personalized Chat Memory:**
    * Store and retrieve past customer interactions (chat history) for each user.
    * Use this memory to tailor responses, suggest next steps, and provide continuity in conversations.
    * Example: If a customer previously asked about term insurance, prioritize related information in future responses.

2. **Optimal Purchase Path Recommendation:**
    * Analyze past chat histories (across users) where insurance purchases were successful.
    * Identify common conversational paths and decision points that led to a purchase.
    * When a new user interacts, guide them along these optimal paths, adapting based on their responses and history.
    * Use the document: `cotext/Smart Swadhan Supreme Brochure/SBI Life-Smart Swadhan Supreme Brochure_V02.pdf` as a knowledge base for product details.
    * Example interaction (for demo/selling):
        - User: "Tell me about Smart Swadhan Supreme."
        - Bot: "Based on your interest and what other customers found helpful, would you like to know about benefits, eligibility, or premium options?"
        - User: "Benefits."
        - Bot: "Smart Swadhan Supreme offers... [summary from PDF]. Many customers who purchased this plan also asked about premium flexibility. Would you like details?"
        - [Continue guiding based on successful paths.]

3. **System Prompt Enhancements:**
    * Detect the user's language and respond in the same language.
    * Analyze sentiment of the user's message and adjust the tone (empathetic, enthusiastic, neutral, etc.) accordingly.
    * Return both the answer and the detected sentiment in the response payload (for frontend use).
