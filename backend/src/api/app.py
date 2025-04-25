from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
import google.generativeai as genai
# --- Added imports for Google Search Grounding ---
from google.generativeai.types import Tool, GenerateContentConfig, GoogleSearch
# --- End Added imports ---
from src.personalization_engine.recommendation_engine import RecommendationEngine
from flask_cors import CORS
from src.utils.language_service import LanguageService
from src.utils.pdf_processor import extract_text_from_pdf
from src.embedding_service.embedding_generator import EmbeddingGenerator
from src.vector_database.vector_db_client import VectorDBClient
from src.config.config import GOOGLE_API_KEY
import logging # Added logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Configure Google Generative AI
if not GOOGLE_API_KEY:
    logging.error("GOOGLE_API_KEY environment variable not set")
    raise ValueError("GOOGLE_API_KEY environment variable not set")
genai.configure(api_key=GOOGLE_API_KEY)

# Configuration for file uploads
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

recommender = RecommendationEngine()
language_service = LanguageService()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/chat', methods=['POST'])
def chat_api():
    # ... existing chat_api implementation ...
    try:
        data = request.get_json()
        customer_id = data.get('customer_id')
        user_input_text = data.get('user_input_text')
        user_language = data.get('language', 'en')
        logging.info(f"Received chat request: customer_id={customer_id}, language={user_language}, input='{user_input_text[:50]}...'")

        if not customer_id or not user_input_text:
            logging.warning("Missing customer_id or user_input_text in chat request")
            return jsonify({"error": "Missing customer_id or user_input_text"}), 400

        english_query = language_service.translate_to_english(user_input_text, user_language)
        logging.info(f"Translated query to English: '{english_query[:50]}...'")

        response = recommender.process_user_interaction(customer_id, english_query, user_language=user_language)
        logging.info(f"Received response from recommender: {type(response)}")

        if isinstance(response, dict) and 'response' in response and not response.get('error'):
            original_english_response = response.get('original_llm_response', response['response'])
            logging.info(f"Original English response: '{original_english_response[:50]}...'")
            translated_response = language_service.translate_from_english(
                response['response'], # Translate the potentially cleaned response
                user_language
            )
            logging.info(f"Translated response to {user_language}: '{translated_response[:50]}...'")
            response['original_response'] = original_english_response # Keep original LLM English response
            response['response'] = translated_response # Overwrite with translated response
            response['detected_language'] = user_language
        elif isinstance(response, dict) and response.get('error'):
             logging.error(f"Recommender returned an error: {response.get('message')}")
        else:
            logging.warning(f"Unexpected response format from recommender: {response}")
            if isinstance(response, dict):
                response['response'] = response.get('response', "Sorry, I encountered an issue.")
            else:
                 response = {"response": "Sorry, I encountered an issue."}

        logging.info(f"Sending final response: {response}")
        return jsonify(response), 200

    except Exception as e:
        logging.exception(f"Error in chat_api: {str(e)}")
        return jsonify({"error": "Server error", "message": str(e)}), 500

@app.route('/gemini_search', methods=['POST'])
def gemini_search_api():
    try:
        data = request.get_json()
        query = data.get('query')
        user_language = data.get('language', 'en')
        logging.info(f"Received Gemini Search request: language={user_language}, query='{query[:50]}...'")

        if not query:
            logging.warning("Missing query in Gemini Search request")
            return jsonify({"error": "Missing query"}), 400

        # 1. Get relevant context from our vector database (FAISS)
        vector_db = VectorDBClient()
        embed_gen = EmbeddingGenerator()
        # Translate query to English for embedding/search consistency
        english_query_for_search = language_service.translate_to_english(query, user_language)
        logging.info(f"Translated Gemini query to English for search: '{english_query_for_search[:50]}...'")
        query_embedding = embed_gen.get_embedding(english_query_for_search, task_type="RETRIEVAL_QUERY")
        
        context = "" # Initialize context
        if query_embedding:
            results = vector_db.query_similar_embeddings(query_embedding, top_k=3)
            logging.info(f"FAISS query returned {len(results.get('matches', []))} matches.")
            if results and results.get('matches'):
                for match in results['matches']:
                    if match.get('metadata', {}).get('text'):
                        source_info = match['metadata'].get('filename', 'knowledge base')
                        context += f"Context from {source_info}:\n{match['metadata']['text']}\n\n---\n\n"
        else:
            logging.warning("Failed to generate embedding for Gemini search query.")

        # 2. Configure Gemini model and Google Search tool
        # Use a model that supports grounding, like gemini-1.5-flash or gemini-pro
        # Note: gemini-2.0-flash mentioned in docs might not be available via API yet, using 1.5 flash
        model = genai.GenerativeModel('gemini-1.5-flash') 
        google_search_tool = Tool(google_search=GoogleSearch())
        tool_config = GenerateContentConfig(tools=[google_search_tool])

        # 3. Create the prompt, instructing the model to use search if needed
        sbi_life_grounded_search_prompt = f"""You are an AI assistant for SBI Life Insurance. Your goal is to answer user queries accurately and helpfully, potentially aiding customer understanding and retention.

        First, use the provided context from our internal knowledge base (if relevant and sufficient) to answer the user's query. 
        If the internal context is insufficient, outdated, or doesn't answer the query (e.g., asking for the *very latest* schemes, news, or details not in the context), use Google Search to find the most current and relevant information about SBI Life.

        Internal Knowledge Base Context:
        {context if context else "No specific context retrieved from internal knowledge base."}
        ---

        User Query: {query}

        Instructions:
        1. Prioritize internal context if relevant and sufficient.
        2. Use Google Search ONLY if internal context is insufficient/outdated OR the query explicitly asks for latest info.
        3. Synthesize information from context and/or search results into a single, coherent response.
        4. Keep the response concise, clear, and easy for a customer to understand.
        5. Ensure accuracy, especially regarding policy details or financial information. Cite search results briefly if used.
        6. Respond in the user's preferred language code: {user_language}.
        7. Do NOT invent policy details or make promises SBI Life cannot keep.
        8. Do NOT include markdown formatting. Use plain text and standard lists ('- ' for bullets).

        Response:"""

        # 4. Generate response with grounding enabled
        logging.info("Calling Gemini API with search grounding enabled...")
        response = model.generate_content(
            sbi_life_grounded_search_prompt,
            generation_config=tool_config # Pass the tool config here
        )

        # Log grounding metadata if available (optional)
        try:
            if response.candidates and response.candidates[0].grounding_metadata:
                search_entry = response.candidates[0].grounding_metadata.search_entry_point
                if search_entry:
                    logging.info(f"Gemini used Google Search. Rendered Content: {search_entry.rendered_content[:100]}...")
                else:
                    logging.info("Grounding metadata present, but no search entry point found.")
            else:
                 logging.info("No grounding metadata found in response. Search likely not used.")
        except Exception as meta_error:
            logging.warning(f"Could not access or log grounding metadata: {meta_error}")

        # 5. Process and translate the response
        response_text = response.text
        logging.info(f"Received response from Gemini: '{response_text[:100]}...'")

        if user_language != 'en':
            logging.info(f"Translating Gemini response to {user_language}...")
            translated_response = language_service.translate_from_english(
                response_text,
                user_language
            )
            logging.info(f"Translated response: '{translated_response[:100]}...'")
            return jsonify({
                "response": translated_response,
                "original_response": response_text, # Keep original English response
                "detected_language": user_language
            }), 200
        
        return jsonify({"response": response_text}), 200

    except Exception as e:
        logging.exception(f"Error in gemini_search_api: {str(e)}")
        return jsonify({"error": "Server error during Gemini search", "message": str(e)}), 500

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf_api():
    # ... existing upload_pdf_api implementation ...
    if 'file' not in request.files:
        logging.warning("Upload PDF request missing file part")
        return jsonify({"error": "No file part in the request"}), 400
    file = request.files['file']
    if file.filename == '':
        logging.warning("Upload PDF request has empty filename")
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            file.save(pdf_path)
            logging.info(f"PDF file saved temporarily to: {pdf_path}")

            extracted_chunks = extract_text_from_pdf(pdf_path) # Assumes this returns chunks
            if not extracted_chunks:
                logging.warning(f"Failed to extract text from PDF: {filename}")
                return jsonify({"error": "Failed to extract text from PDF"}), 500
            logging.info(f"Extracted {len(extracted_chunks)} chunks from PDF: {filename}")

            logging.info("Initializing Embedding Generator for PDF...")
            embed_gen = EmbeddingGenerator()
            logging.info("Initializing Vector DB Client for PDF...")
            vector_db = VectorDBClient()

            processed_count = 0
            for i, chunk in enumerate(extracted_chunks):
                 if not chunk.strip(): continue # Skip empty chunks
                 vector_id = f"pdf_{filename}_chunk_{i}"
                 logging.debug(f"Processing chunk {i+1}/{len(extracted_chunks)} (ID: {vector_id})...")
                 embedding = embed_gen.get_embedding(chunk, task_type="RETRIEVAL_DOCUMENT")
                 if embedding:
                     metadata = {"source": "pdf", "filename": filename, "chunk_index": i, "text": chunk}
                     success = vector_db.upsert_embedding(vector_id, embedding, metadata)
                     if success:
                         logging.debug(f"Chunk {i+1} stored successfully.")
                         processed_count += 1
                     else:
                         logging.warning(f"Failed to store chunk {i+1} (ID: {vector_id}).")
                 else:
                     logging.warning(f"Failed to generate embedding for chunk {i+1} (ID: {vector_id}).")
            
            if processed_count > 0:
                logging.info(f"PDF '{filename}' processed: {processed_count}/{len(extracted_chunks)} chunks embedded successfully.")
                return jsonify({"message": f"PDF '{filename}' processed: {processed_count}/{len(extracted_chunks)} chunks embedded successfully."}), 200
            else:
                 logging.error(f"Failed to process any chunks from PDF '{filename}'.")
                 return jsonify({"error": "Failed to process any content from the PDF"}), 500

        except Exception as e:
            logging.exception(f"Error processing PDF upload '{filename}': {str(e)}")
            return jsonify({"error": "Server error during PDF processing", "message": str(e)}), 500
        finally:
            if os.path.exists(pdf_path):
                try:
                    os.remove(pdf_path)
                    logging.info(f"Removed temporary file: {pdf_path}")
                except Exception as e:
                    logging.error(f"Error removing temporary file {pdf_path}: {e}")
    else:
        logging.warning(f"Upload attempt with invalid file type: {file.filename}")
        return jsonify({"error": "Invalid file type. Only PDF files are allowed."}), 400

if __name__ == '__main__':
    logging.info("Starting Flask application...")
    app.run(debug=True)