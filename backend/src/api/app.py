
from flask import Flask, request, jsonify
from src.personalization_engine.recommendation_engine import RecommendationEngine
from flask_cors import CORS
from src.utils.language_service import LanguageService

app = Flask(__name__)
CORS(app)
recommender = RecommendationEngine()
language_service = LanguageService()

@app.route('/chat', methods=['POST'])
def chat_api():
    try:
        data = request.get_json()
        customer_id = data.get('customer_id')
        user_input_text = data.get('user_input_text')
        user_language = data.get('language', 'en')  
        if not customer_id or not user_input_text:
            return jsonify({"error": "Missing customer_id or user_input_text"}), 400

        
        english_query = language_service.translate_to_english(user_input_text, user_language)

       
        response = recommender.process_user_interaction(customer_id, english_query)

        
        if isinstance(response, dict) and 'response' in response:
            translated_response = language_service.translate_from_english(
                response['response'], 
                user_language
            )
            response['original_response'] = response['response']
            response['response'] = translated_response
            response['detected_language'] = user_language

        return jsonify(response), 200

    except Exception as e:
        print(f"Error in chat_api: {str(e)}")
        return jsonify({"error": "Server error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)