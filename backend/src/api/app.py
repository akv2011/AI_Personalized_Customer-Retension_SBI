from flask import Flask, request, jsonify
import os # Added for file path operations
from werkzeug.utils import secure_filename # Added for secure file handling

from src.personalization_engine.recommendation_engine import RecommendationEngine
from flask_cors import CORS
from src.utils.language_service import LanguageService
from src.utils.pdf_processor import extract_text_from_pdf # Added PDF processor
from src.embedding_service.embedding_generator import EmbeddingGenerator # Added Embedding Generator
from src.vector_database.vector_db_client import VectorDBClient # Added Vector DB Client

app = Flask(__name__)
CORS(app)

# Configuration for file uploads
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Instantiate services (consider if global instantiation is appropriate for your scaling needs)
# For simplicity, RecommendationEngine and LanguageService are global.
# EmbeddingGenerator and VectorDBClient might be better instantiated per-request
# or managed differently depending on resource usage and statefulness.
recommender = RecommendationEngine()
language_service = LanguageService()
# embed_gen = EmbeddingGenerator() # Instantiated within the route for now
# vector_db = VectorDBClient() # Instantiated within the route for now

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/chat', methods=['POST'])
def chat_api():
    try:
        data = request.get_json()
        customer_id = data.get('customer_id')
        user_input_text = data.get('user_input_text')
        user_language = data.get('language', 'en') # Get language from request, default to 'en'
        if not customer_id or not user_input_text:
            return jsonify({"error": "Missing customer_id or user_input_text"}), 400

        # Translate user input to English for processing
        # (Assuming LanguageService handles 'en' input correctly)
        english_query = language_service.translate_to_english(user_input_text, user_language)

        # Pass english_query AND original user_language to the recommender
        response = recommender.process_user_interaction(customer_id, english_query, user_language=user_language)

        # Translate response back to user's language
        if isinstance(response, dict) and 'response' in response and not response.get('error'):
            translated_response = language_service.translate_from_english(
                response['response'],
                user_language
            )
            response['original_response'] = response['response'] # Keep original English response
            response['response'] = translated_response # Overwrite with translated response
            # Keep detected_language and add sentiment if present
            response['detected_language'] = user_language
            # Sentiment will be added later if returned by recommender

        return jsonify(response), 200

    except Exception as e:
        print(f"Error in chat_api: {str(e)}")
        return jsonify({"error": "Server error", "message": str(e)}), 500

# --- New PDF Upload Endpoint --- 
@app.route('/upload_pdf', methods=['POST'])
def upload_pdf_api():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            file.save(pdf_path)
            print(f"PDF file saved temporarily to: {pdf_path}")

            # 1. Extract text from PDF
            extracted_text = extract_text_from_pdf(pdf_path)
            if not extracted_text:
                return jsonify({"error": "Failed to extract text from PDF"}), 500

            # 2. Generate Embedding (Instantiate here for simplicity)
            # Consider chunking large texts before embedding
            print("Initializing Embedding Generator...")
            embed_gen = EmbeddingGenerator()
            print("Generating embedding for extracted PDF text...")
            embedding = embed_gen.get_embedding(extracted_text)
            if not embedding:
                 return jsonify({"error": "Failed to generate embedding for PDF content"}), 500
            print(f"Embedding generated (dimensions: {len(embedding)})...")

            # 3. Upsert into Vector DB (Instantiate here for simplicity)
            print("Initializing Vector DB Client...")
            vector_db = VectorDBClient()
            # Create a unique ID (e.g., using filename) and metadata
            vector_id = f"pdf_{filename}"
            # Store the FULL extracted text in metadata under the key 'text'
            metadata = {
                "source": "pdf",
                "filename": filename,
                "text": extracted_text # Store full text
            }
            print(f"Upserting vector with ID: {vector_id}")
            success = vector_db.upsert_embedding(vector_id, embedding, metadata)

            if success:
                print("Upsert successful.")
                return jsonify({"message": f"PDF '{filename}' processed and embedded successfully.", "vector_id": vector_id}), 200
            else:
                print("Upsert failed.")
                return jsonify({"error": "Failed to store embedding in vector database"}), 500

        except Exception as e:
            print(f"Error processing PDF upload: {str(e)}")
            return jsonify({"error": "Server error during PDF processing", "message": str(e)}), 500
        finally:
            # 4. Clean up the uploaded file
            if os.path.exists(pdf_path):
                try:
                    os.remove(pdf_path)
                    print(f"Removed temporary file: {pdf_path}")
                except Exception as e:
                    print(f"Error removing temporary file {pdf_path}: {e}")
    else:
        return jsonify({"error": "Invalid file type. Only PDF files are allowed."}), 400

if __name__ == '__main__':
    app.run(debug=True)