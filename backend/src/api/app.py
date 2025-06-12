from flask import Flask, request, jsonify
import os
from datetime import datetime
from werkzeug.utils import secure_filename
import google.generativeai as genai
# --- Added imports for Google Search Grounding ---
# Remove the incorrect import line below
# from google.generativeai.types import Tool, GenerateContentConfig, GoogleSearch 
# Add the corrected import lines below
# Remove GoogleSearch from this import
from google.generativeai.types import Tool 
from google.generativeai import GenerationConfig # Corrected import for GenerationConfig
# --- End Added imports ---
from src.personalization_engine.recommendation_engine import RecommendationEngine
from flask_cors import CORS
from src.utils.language_service import LanguageService
from src.utils.pdf_processor import extract_text_from_pdf
from src.embedding_service.embedding_generator import EmbeddingGenerator
from src.vector_database.vector_db_client import VectorDBClient
from src.config.config import GOOGLE_API_KEY
import logging # Added logging
import asyncio # Add asyncio for database operations

# Add database service imports
try:
    from src.database.database_service import get_database_service, initialize_database_service
    from src.database.postgres_mcp_server import initialize_mcp_server
    DATABASE_AVAILABLE = True
except ImportError:
    logging.warning("Database service not available. Running in FAISS-only mode.")
    DATABASE_AVAILABLE = False

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
    """Enhanced chat API with PostgreSQL MCP Server integration"""
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

        db_storage_success = False
        if DATABASE_AVAILABLE:
            try:
                async def store_interaction_async():
                    from src.database.database_service import db_service
                    from src.database.postgres_mcp_server import mcp_server
                    
                    # Initialize mcp_server and db_service for the current event loop
                    await mcp_server.initialize()
                    await db_service.initialize()

                    db_result = await db_service.store_interaction(
                        customer_id=customer_id,
                        interaction_text=english_query,
                        interaction_type="chatbot",
                        user_language=user_language,
                        additional_metadata={"api_endpoint": "chat"}
                    )
                    
                    # Clean up mcp_server resources for this loop
                    await mcp_server.close()
                    return db_result

                db_result = asyncio.run(store_interaction_async())
                
                if db_result["success"]:
                    logging.info(f"Database storage successful: {db_result['conversation_id']}")
                    db_storage_success = True
                else:
                    logging.warning(f"Database storage failed: {db_result.get('error')}")
            except Exception as db_error:
                logging.error(f"Database service error in chat_api: {db_error}")
                # Ensure a response is still sent if DB operations fail
        
        response = recommender.process_user_interaction(customer_id, english_query, user_language=user_language)
        
        if isinstance(response, dict):
            response['database_stored'] = db_storage_success
        
        logging.info(f"Received response from processing: {type(response)}")

        if isinstance(response, dict) and 'response' in response and not response.get('error'):
            original_english_response = response.get('original_llm_response', response['response'])
            logging.info(f"Original English response: '{original_english_response[:50]}...'")
            translated_response = language_service.translate_from_english(
                response['response'],
                user_language
            )
            logging.info(f"Translated response to {user_language}: '{translated_response[:50]}...'")
            response['original_response'] = original_english_response
            response['response'] = translated_response
            response['detected_language'] = user_language
        elif isinstance(response, dict) and response.get('error'):
             logging.error(f"Processing returned an error: {response.get('message')}")
        else:
            logging.warning(f"Unexpected response format: {response}")
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
        # --- Corrected model name ---
        model = genai.GenerativeModel('gemini-1.5-flash-001') # Use a model known to support grounding well
        # --- Define the Tool ---
        google_search_tool = Tool(google_search_retrieval={})
        # --- Remove incorrect GenerationConfig initialization for tools ---
        # tool_config = GenerationConfig(tools=[google_search_tool]) 
        # --- End Correction ---

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
            # --- Pass tools directly to generate_content ---
            tools=[google_search_tool] 
            # generation_config=tool_config # Remove this line
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

# === Database API Endpoints ===

@app.route('/api/customer/<customer_id>/profile', methods=['GET'])
def get_customer_profile(customer_id):
    """Get comprehensive customer profile"""
    if not DATABASE_AVAILABLE:
        return jsonify({"error": "Database service not available"}), 503
    
    try:
        async def get_profile_async_wrapper():
            from src.database.database_service import db_service
            from src.database.postgres_mcp_server import mcp_server
            
            await mcp_server.initialize()
            await db_service.initialize() # Ensures db_service uses the initialized mcp_server

            profile_data = await db_service.get_customer_profile(customer_id)
            
            await mcp_server.close()
            return profile_data
        
        result = asyncio.run(get_profile_async_wrapper())
        
        if result["success"]:
            return jsonify(result["profile"]), 200
        else:
            logging.error(f"Profile retrieval failed for {customer_id}: {result.get('error')}")
            return jsonify({"error": result.get("error", "Failed to get profile")}), 400
            
    except Exception as e:
        logging.exception(f"Error getting customer profile for {customer_id}: {e}")
        if isinstance(e, RuntimeError) and "event loop" in str(e).lower():
            return jsonify({"error": "Event loop management issue", "detail": str(e)}), 500
        return jsonify({"error": "Server error during profile retrieval", "detail": str(e)}), 500

@app.route('/api/customer/<customer_id>/preferences', methods=['POST'])
def update_customer_preferences(customer_id):
    """Update customer preferences"""
    if not DATABASE_AVAILABLE:
        return jsonify({"error": "Database service not available"}), 503
    
    try:
        data = request.get_json()
        preference_type = data.get('preference_type')
        preference_value = data.get('preference_value')
        confidence_score = data.get('confidence_score', 0.5)
        
        if not preference_type or preference_value is None:
            return jsonify({"error": "Missing preference_type or preference_value"}), 400
        
        async def update_preferences_wrapper():
            from src.database.database_service import db_service
            from src.database.postgres_mcp_server import mcp_server

            await mcp_server.initialize()
            await db_service.initialize()

            update_result = await db_service.update_customer_preferences(
                customer_id, preference_type, preference_value, confidence_score
            )
            
            await mcp_server.close()
            return update_result
        
        result = asyncio.run(update_preferences_wrapper())
        
        if result["success"]:
            return jsonify({"message": "Preferences updated successfully"}), 200
        else:
            logging.error(f"Failed to update preferences for {customer_id}: {result.get('error')}")
            return jsonify({"error": result.get("error", "Failed to update preferences")}), 400
            
    except Exception as e:
        logging.exception(f"Error updating customer preferences for {customer_id}: {e}")
        if isinstance(e, RuntimeError) and "event loop" in str(e).lower():
            return jsonify({"error": "Event loop management issue", "detail": str(e)}), 500
        return jsonify({"error": "Server error during preference update", "detail": str(e)}), 500

@app.route('/api/customer/<customer_id>/similar-interactions', methods=['POST'])
def search_similar_interactions(customer_id):
    """Search for similar interactions"""
    if not DATABASE_AVAILABLE:
        return jsonify({"error": "Database service not available"}), 503
    
    try:
        data = request.get_json()
        query_text = data.get('query_text')
        top_k = data.get('top_k', 5)
        
        if not query_text:
            return jsonify({"error": "Missing query_text"}), 400
        
        async def search_interactions_wrapper():
            from src.database.database_service import db_service
            from src.database.postgres_mcp_server import mcp_server

            await mcp_server.initialize()
            await db_service.initialize()

            search_result = await db_service.search_similar_interactions(customer_id, query_text, top_k)
            
            await mcp_server.close()
            return search_result
            
        result = asyncio.run(search_interactions_wrapper())
        
        if result["success"]:
            return jsonify(result), 200
        else:
            logging.error(f"Similar interactions search failed for {customer_id}: {result.get('error')}")
            return jsonify({"error": result.get("error", "Search failed")}), 400
            
    except Exception as e:
        logging.exception(f"Error searching similar interactions for {customer_id}: {e}")
        if isinstance(e, RuntimeError) and "event loop" in str(e).lower():
            return jsonify({"error": "Event loop management issue", "detail": str(e)}), 500
        return jsonify({"error": "Server error during similar interactions search", "detail": str(e)}), 500

@app.route('/api/analytics/summary', methods=['GET'])
def get_analytics_summary():
    """Get analytics summary"""
    if not DATABASE_AVAILABLE:
        return jsonify({"error": "Database service not available"}), 503
    
    try:
        customer_id = request.args.get('customer_id')
        days = int(request.args.get('days', 30))
        
        async def get_analytics_wrapper():
            from src.database.database_service import db_service
            from src.database.postgres_mcp_server import mcp_server

            await mcp_server.initialize()
            await db_service.initialize()

            analytics_data = await db_service.get_analytics_summary(customer_id, days)
            
            await mcp_server.close()
            return analytics_data
            
        result = asyncio.run(get_analytics_wrapper())
        
        if result["success"]:
            return jsonify(result), 200
        else:
            logging.error(f"Analytics retrieval failed: {result.get('error')}")
            return jsonify({"error": result.get("error", "Analytics failed")}), 400
            
    except Exception as e:
        logging.exception(f"Error getting analytics: {e}")
        if isinstance(e, RuntimeError) and "event loop" in str(e).lower():
            return jsonify({"error": "Event loop management issue", "detail": str(e)}), 500
        return jsonify({"error": "Server error during analytics retrieval", "detail": str(e)}), 500

@app.route('/api/database/status', methods=['GET'])
def get_database_status():
    """Get database and MCP server status"""
    try:
        status = {
            "database_available": DATABASE_AVAILABLE,
            "timestamp": datetime.now().isoformat()
        }
        
        if DATABASE_AVAILABLE:
            try:
                # Use threading to avoid event loop conflicts
                import threading
                import queue
                
                result_queue = queue.Queue()
                
                def check_db_status():
                    try:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        
                        async def check_status():
                            db_service = await get_database_service()
                            return db_service is not None
                        
                        db_healthy = loop.run_until_complete(check_status())
                        loop.close()
                        result_queue.put(("success", db_healthy))
                    except Exception as e:
                        result_queue.put(("error", str(e)))
                
                thread = threading.Thread(target=check_db_status)
                thread.start()
                thread.join(timeout=10)  # 10 second timeout
                
                if thread.is_alive():
                    status["database_healthy"] = False
                    status["mcp_server"] = "timeout"
                else:
                    result_status, result = result_queue.get_nowait()
                    if result_status == "success":
                        status["database_healthy"] = result
                        status["mcp_server"] = "operational" if result else "error"
                    else:
                        status["database_healthy"] = False
                        status["mcp_server"] = "error"
                        status["error"] = result
            except Exception as e:
                status["database_healthy"] = False
                status["mcp_server"] = "error"
                status["error"] = str(e)
        
        return jsonify(status), 200
        
    except Exception as e:
        logging.exception(f"Error checking database status: {e}")
        return jsonify({"error": "Server error", "message": str(e)}), 500

@app.route('/api/mcp/operations', methods=['GET'])
def get_mcp_operations():
    """Get recent MCP operations for monitoring"""
    if not DATABASE_AVAILABLE:
        return jsonify({"error": "Database service not available"}), 503
    
    try:
        limit = int(request.args.get('limit', 10))
        
        async def get_operations_async():
            from src.database.postgres_mcp_server import PostgresMCPServer
            mcp_server = PostgresMCPServer()
            await mcp_server.initialize()
            
            # Use $1 parameter instead of %s for PostgreSQL
            result = await mcp_server.execute_query("""
                SELECT operation_id, operation_type, status, created_at, 
                       execution_time_ms, error_message
                FROM mcp_operations 
                ORDER BY created_at DESC 
                LIMIT $1
            """, [limit])
            
            await mcp_server.close()
            return result
        
        # Run in a new event loop
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(get_operations_async())
            loop.close()
        except RuntimeError:
            # If we can't create a new loop, try to get the existing one
            result = asyncio.create_task(get_operations_async())
            result = asyncio.get_event_loop().run_until_complete(result)
        
        if result["success"]:
            return jsonify({
                "success": True,
                "operations": result["rows"],
                "count": len(result["rows"])
            }), 200
        else:
            return jsonify({"error": result.get("error", "Failed to get operations")}), 400
            
    except Exception as e:
        logging.exception(f"Error getting MCP operations: {e}")
        return jsonify({"error": "Server error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
def database_status():
    """Check database connectivity status"""
    status = {
        "database_available": DATABASE_AVAILABLE,
        "faiss_available": True,  # FAISS is always available
        "services": {}
    }
    
    if DATABASE_AVAILABLE:
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            async def check_services():
                from src.database.postgres_mcp_server import mcp_server
                # Simple connectivity test
                result = await mcp_server.execute_query("SELECT 1 as test")
                return result["success"]
            
            postgres_status = loop.run_until_complete(check_services())
            loop.close()
            
            status["services"]["postgresql_mcp"] = postgres_status
            
        except Exception as e:
            logging.error(f"Database status check failed: {e}")
            status["services"]["postgresql_mcp"] = False
    
    return jsonify(status), 200

if __name__ == '__main__':
    logging.info("Starting Flask application...")
    app.run(debug=True)