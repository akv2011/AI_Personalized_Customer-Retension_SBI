# backend/src/api/app.py
from flask import Flask, request, jsonify
from src.personalization_engine.recommendation_engine import RecommendationEngine
from flask_cors import CORS # Import CORS



app = Flask(__name__)
CORS(app) 
recommender = RecommendationEngine()

@app.route('/chat', methods=['POST'])
def chat_api():
    try:
        data = request.get_json()
        customer_id = data.get('customer_id')
        user_input_text = data.get('user_input_text')

        if not customer_id or not user_input_text:
            return jsonify({"error": "Missing customer_id or user_input_text"}), 400

        response = recommender.process_user_interaction(customer_id, user_input_text)
        return jsonify(response), 200

    except Exception as e:
        print(f"Error in chat_api: {str(e)}")
        return jsonify({"error": "Server error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)