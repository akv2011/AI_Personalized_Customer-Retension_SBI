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
# Add Exa API import
from exa_py import Exa
from src.personalization_engine.recommendation_engine import RecommendationEngine
from flask_cors import CORS
from src.utils.language_service import LanguageService
from src.utils.pdf_processor import extract_text_from_pdf
from src.embedding_service.embedding_generator import EmbeddingGenerator
from src.vector_database.vector_db_client import VectorDBClient
from src.config.config import GOOGLE_API_KEY, EXA_API_KEY
# Add import for Smart Swadhan guidance
from src.web_scraping.hybrid_scraper import get_hybrid_smart_swadhan_guidance
# Add speech service import
from src.utils.speech_service import get_speech_service, speak_text, transcribe_audio, record_and_transcribe
import logging # Added logging
import asyncio # Add asyncio for database operations
import base64  # For audio data encoding

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

# Configure Exa API
if not EXA_API_KEY:
    logging.error("EXA_API_KEY environment variable not set")
    raise ValueError("EXA_API_KEY environment variable not set")
exa = Exa(EXA_API_KEY)

# Configuration for file uploads
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

recommender = RecommendationEngine()
language_service = LanguageService()

def format_response_text(text):
    """Format response text for better readability with proper spacing and structure"""
    if not text:
        return text
    
    # Remove markdown formatting
    import re
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Remove bold markdown
    text = re.sub(r'\*(.*?)\*', r'\1', text)      # Remove italic markdown
    text = re.sub(r'#{1,6}\s*(.*)', r'\1', text)  # Remove headers
    
    # Split into paragraphs and process
    paragraphs = text.split('\n\n')
    formatted_paragraphs = []
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
            
        # Check if it's a heading-like line (short and descriptive)
        if len(para) < 100 and ':' in para and not para.startswith('-'):
            # Format as heading
            formatted_paragraphs.append(f"\n{para.upper()}\n")
        elif para.startswith('-') or para.startswith('•'):
            # Format bullet points with proper spacing
            lines = para.split('\n')
            bullet_points = []
            for line in lines:
                line = line.strip()
                if line.startswith('-') or line.startswith('•'):
                    # Clean and format bullet point
                    clean_line = line.lstrip('-•').strip()
                    bullet_points.append(f"  • {clean_line}")
                else:
                    bullet_points.append(f"    {line}")
            formatted_paragraphs.append('\n'.join(bullet_points))
        else:
            # Regular paragraph
            formatted_paragraphs.append(para)
    
    # Join with proper spacing
    result = '\n\n'.join(formatted_paragraphs)
    
    # Ensure proper spacing around sections
    result = re.sub(r'\n{3,}', '\n\n', result)  # Limit multiple newlines
    
    return result.strip()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/chat', methods=['POST'])
def chat_api():
    """Enhanced chat API with PostgreSQL MCP Server integration"""
    try:
        data = request.get_json()
        if not data:
            logging.warning("No JSON data received in chat request")
            return jsonify({"error": "No JSON data received"}), 400
            
        customer_id = data.get('customer_id')
        user_input_text = data.get('user_input_text')
        user_language = data.get('language', 'en')
        logging.info(f"Received chat request: customer_id={customer_id}, language={user_language}, input='{user_input_text[:50] if user_input_text else 'None'}...'")

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
def exa_search_api():
    """Enhanced search API using Exa web search with internal knowledge base grounding"""
    try:
        data = request.get_json()
        query = data.get('query')
        user_language = data.get('language', 'en')
        logging.info(f"Received Exa Search request: language={user_language}, query='{query[:50]}...'")

        if not query:
            logging.warning("Missing query in Exa Search request")
            return jsonify({"error": "Missing query"}), 400

        # 1. Get relevant context from our vector database (FAISS)
        vector_db = VectorDBClient()
        embed_gen = EmbeddingGenerator()
        # Translate query to English for embedding/search consistency
        english_query_for_search = language_service.translate_to_english(query, user_language)
        logging.info(f"Translated Exa query to English for search: '{english_query_for_search[:50]}...'")
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
            logging.warning("Failed to generate embedding for Exa search query.")

        # 2. Perform Exa web search for additional information
        web_search_results = ""
        try:
            logging.info("Performing Exa web search...")
            # Create search query focused on SBI Life
            search_query = f"SBI Life Insurance {english_query_for_search}"
            
            # Perform search and get content
            exa_results = exa.search_and_contents(
                search_query,
                type="auto",  # Let Exa choose between neural and keyword search
                num_results=3,  # Get top 3 results
                text=True  # Get full text content
            )
            
            if exa_results and exa_results.results:
                logging.info(f"Exa search returned {len(exa_results.results)} results")
                for i, result in enumerate(exa_results.results[:3]):
                    web_search_results += f"Web Result {i+1} - {result.title}:\n"
                    web_search_results += f"URL: {result.url}\n"
                    if result.text:
                        # Truncate text to prevent overly long responses
                        content_snippet = result.text[:500] + "..." if len(result.text) > 500 else result.text
                        web_search_results += f"Content: {content_snippet}\n\n---\n\n"
            else:
                logging.warning("No results returned from Exa search")
                web_search_results = "No additional web results found."
                
        except Exception as exa_error:
            logging.error(f"Exa search failed: {exa_error}")
            web_search_results = "Web search temporarily unavailable."

        # 3. Use OpenAI to synthesize the response
        try:
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            
            synthesis_prompt = f"""You are an AI assistant for SBI Life Insurance. Your goal is to answer user queries accurately and helpfully, potentially aiding customer understanding and retention.

You have access to two sources of information:

Internal Knowledge Base Context:
{context if context else "No specific context retrieved from internal knowledge base."}

Web Search Results:
{web_search_results}

User Query: {query}

Instructions:
1. Prioritize internal context if relevant and sufficient.
2. Use web search results to supplement or provide the latest information if internal context is insufficient.
3. Synthesize information from both sources into a single, coherent response.
4. Format your response with clear headings and bullet points for better readability.
5. Use the following structure when applicable:
   - Start with a brief overview paragraph
   - Use clear section headings (e.g., "KEY BENEFITS:", "ELIGIBILITY:", "PREMIUM OPTIONS:")
   - Use bullet points with proper spacing for lists
   - End with a helpful summary or next steps
6. Keep the response concise, clear, and easy for a customer to understand.
7. Ensure accuracy, especially regarding policy details or financial information.
8. If you use web search results, briefly mention that the information comes from recent sources.
9. Do NOT invent policy details or make promises SBI Life cannot keep.
10. Do NOT use markdown formatting like ** or *. Use plain text with clear spacing and structure.
11. Focus specifically on SBI Life products and services.
12. Use proper spacing between sections and bullet points for readability.

Example format:
PRODUCT OVERVIEW:
Brief description of the product.

KEY BENEFITS:
  • First benefit with clear explanation
  • Second benefit with details
  • Third benefit

ELIGIBILITY CRITERIA:
  • Age requirements
  • Other conditions

PREMIUM INFORMATION:
  • Payment options
  • Amount details

Respond in English first, then translate if needed."""

            response = client.chat.completions.create(
                model="gpt-4o",  # Use the latest model available
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for SBI Life Insurance customers."},
                    {"role": "user", "content": synthesis_prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            response_text = response.choices[0].message.content
            logging.info(f"Received response from OpenAI: '{response_text[:100]}...'")
            
            # Format the response text for better readability
            response_text = format_response_text(response_text)
        except Exception as openai_error:
            logging.error(f"OpenAI synthesis failed: {openai_error}")
            # Fallback to simple concatenation
            if context:
                response_text = f"Based on our knowledge base:\n\n{context[:400]}..."
            elif web_search_results and "No additional web results found" not in web_search_results:
                response_text = f"Based on recent information:\n\n{web_search_results[:400]}..."
            else:
                response_text = "I apologize, but I'm unable to find specific information about your query at the moment. Please contact SBI Life customer service for detailed assistance."
            
            # Apply formatting to fallback responses too
            response_text = format_response_text(response_text)

        # 4. Translate response if needed
        if user_language != 'en':
            logging.info(f"Translating response to {user_language}...")
            translated_response = language_service.translate_from_english(
                response_text,
                user_language
            )
            logging.info(f"Translated response: '{translated_response[:100]}...'")
            return jsonify({
                "response": translated_response,
                "original_response": response_text,
                "detected_language": user_language
            }), 200
        
        return jsonify({"response": response_text}), 200

    except Exception as e:
        logging.exception(f"Error in exa_search_api: {str(e)}")
        return jsonify({"error": "Server error during Exa search", "message": str(e)}), 500

@app.route('/smart_swadhan_guidance', methods=['POST'])
def smart_swadhan_guidance_api():
    """API endpoint for Smart Swadhan Supreme navigation guidance with hybrid scraping"""
    try:
        data = request.get_json()
        user_query = data.get('query', 'Guide me to Smart Swadhan Supreme')
        
        logging.info(f"Smart Swadhan guidance requested: {user_query}")
        
        # Get AI-powered guidance with hybrid scraping
        guidance_result = get_hybrid_smart_swadhan_guidance(user_query)
        
        if guidance_result.get('success'):
            mode = guidance_result.get('mode', 'unknown')
            processing_time = guidance_result.get('processing_time', 0)
            
            logging.info(f"Smart Swadhan guidance generated successfully using {mode} in {processing_time:.2f}s")
            
            return jsonify({
                "success": True,
                "mode": mode,
                "guidance": guidance_result.get('guidance'),
                "navigation_steps": guidance_result.get('navigation_steps', []),
                "product_summary": guidance_result.get('product_summary', ''),
                "total_steps": guidance_result.get('guidance', {}).get('total_steps', 0),
                "recommended_actions": guidance_result.get('guidance', {}).get('recommended_actions', []),
                "processing_time": processing_time,
                "note": guidance_result.get('note', ''),
                "timestamp": guidance_result.get('timestamp')
            }), 200
        else:
            logging.error(f"Failed to generate Smart Swadhan guidance: {guidance_result.get('error')}")
            return jsonify({
                "success": False,
                "error": guidance_result.get('error', 'Unknown error'),
                "message": "Failed to generate navigation guidance",
                "mode": guidance_result.get('mode', 'unknown')
            }), 500
            
    except Exception as e:
        logging.exception(f"Error in smart_swadhan_guidance_api: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Server error during guidance generation",
            "message": str(e)
        }), 500

@app.route('/test_scraper', methods=['GET'])
def test_scraper_api():
    """Test endpoint to verify the scraper functionality"""
    try:
        # Import and test the scraper
        from src.web_scraping.hyper_sbi_scraper import get_smart_swadhan_guidance_sync
        
        result = get_smart_swadhan_guidance_sync("Test Smart Swadhan navigation")
        
        return jsonify({
            "success": True,
            "message": "Scraper test completed",
            "result": result
        }), 200
        
    except Exception as e:
        logging.exception(f"Error in test_scraper_api: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Scraper test failed"
        }), 500

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

# === Speech Service API Endpoints ===

@app.route('/api/speech/text-to-speech', methods=['POST'])
def text_to_speech_api():
    """Convert text to speech and return audio"""
    try:
        data = request.get_json()
        text = data.get('text')
        language = data.get('language', 'english')

        if not text:
            return jsonify({"error": "Missing text to convert to speech"}), 400

        # Map language codes to full names
        language_map = {
            'hi': 'hindi',
            'en': 'english', 
            'mr': 'marathi'
        }
        language = language_map.get(language, language)

        logging.info(f"Converting text to speech: '{text[:50]}...' in {language}")
        
        # Get speech service and convert text to speech
        speech_service = get_speech_service()
        result = speech_service.text_to_speech(text, language)

        if result['success']:
            # Handle different response types
            if 'audio_data' in result:
                # Encode audio data to base64 for JSON response
                audio_base64 = base64.b64encode(result['audio_data']).decode('utf-8')
                return jsonify({
                    "success": True,
                    "audio_base64": audio_base64,
                    "service": result.get('service', 'unknown'),
                    "language": result.get('language', language)
                }), 200
            elif 'audio_path' in result:
                # Return path for download
                return jsonify({
                    "success": True,
                    "audio_path": result['audio_path'],
                    "service": result.get('service', 'unknown'),
                    "language": result.get('language', language)
                }), 200
        else:
            return jsonify({
                "success": False,
                "error": result.get('error', 'TTS conversion failed')
            }), 400

    except Exception as e:
        logging.exception(f"Error in text_to_speech_api: {str(e)}")
        return jsonify({"error": "Server error during TTS conversion", "message": str(e)}), 500

@app.route('/api/speech/speech-to-text', methods=['POST'])
def speech_to_text_api():
    """Convert speech to text from uploaded audio file"""
    try:
        language = request.form.get('language', 'english')
        mime_type = request.form.get('mimeType', 'audio/webm')
        
        # Map language codes to full names
        language_map = {
            'hi': 'hindi',
            'en': 'english', 
            'mr': 'marathi'
        }
        language = language_map.get(language, language)

        if 'audio' not in request.files:
            return jsonify({"error": "No audio file provided"}), 400
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({"error": "No audio file selected"}), 400

        # Save the uploaded audio file temporarily
        filename = secure_filename(audio_file.filename)
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        audio_file.save(audio_path)
        
        logging.info(f"Processing audio file: {filename} (mimeType: {mime_type}) for {language}")
        logging.info(f"Audio file size: {os.path.getsize(audio_path)} bytes")

        # Get speech service and transcribe
        speech_service = get_speech_service()
        result = speech_service.speech_to_text(audio_path, language)

        # Clean up temporary file
        try:
            os.remove(audio_path)
        except:
            pass

        if result['success']:
            return jsonify({
                "success": True,
                "transcription": result['transcription'],
                "confidence": result.get('confidence', 0.0),
                "service": result.get('service', 'unknown'),
                "language": result.get('language', language)
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": result.get('error', 'STT conversion failed')
            }), 400

    except Exception as e:
        logging.exception(f"Error in speech_to_text_api: {str(e)}")
        return jsonify({"error": "Server error during STT conversion", "message": str(e)}), 500

@app.route('/api/speech/record-and-transcribe', methods=['POST'])
def record_and_transcribe_api():
    """Record audio from microphone and transcribe"""
    try:
        data = request.get_json()
        language = data.get('language', 'english')
        duration = data.get('duration', 5)  # Default 5 seconds

        # Map language codes to full names
        language_map = {
            'hi': 'hindi',
            'en': 'english', 
            'mr': 'marathi'
        }
        language = language_map.get(language, language)

        logging.info(f"Recording audio for {duration} seconds in {language}")

        # Get speech service and record + transcribe
        speech_service = get_speech_service()
        result = speech_service.record_from_microphone(duration, language)

        if result['success']:
            return jsonify({
                "success": True,
                "transcription": result['transcription'],
                "confidence": result.get('confidence', 0.0),
                "service": result.get('service', 'unknown'),
                "language": result.get('language', language),
                "duration": result.get('recording_duration', duration)
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": result.get('error', 'Recording failed')
            }), 400

    except Exception as e:
        logging.exception(f"Error in record_and_transcribe_api: {str(e)}")
        return jsonify({"error": "Server error during recording", "message": str(e)}), 500

@app.route('/api/speech/test', methods=['GET'])
def test_speech_services():
    """Test all speech services"""
    try:
        speech_service = get_speech_service()
        test_results = speech_service.test_speech_services()
        
        return jsonify({
            "success": True,
            "test_results": test_results
        }), 200

    except Exception as e:
        logging.exception(f"Error testing speech services: {str(e)}")
        return jsonify({"error": "Error testing speech services", "message": str(e)}), 500

@app.route('/api/speech/voices', methods=['GET'])
def get_available_voices():
    """Get available voices for a language"""
    try:
        language = request.args.get('language', 'english')
        
        speech_service = get_speech_service()
        result = speech_service.get_available_voices(language)
        
        return jsonify(result), 200

    except Exception as e:
        logging.exception(f"Error getting voices: {str(e)}")
        return jsonify({"error": "Error getting voices", "message": str(e)}), 500

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