# AI_Personalized_Customer-Retension_SBI

# SBI Life AI-Driven Personalization Chatbot

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Enhancing Customer Experience and Retention through Intelligent Conversations**

## Project Overview

This project implements an AI-driven chatbot designed to revolutionize customer interaction for SBI Life Insurance.  Moving beyond traditional persona-based approaches, this chatbot leverages cutting-edge technologies to provide **hyper-personalized experiences**, leading to increased customer satisfaction, improved policy persistency, and a higher propensity to purchase.

**Problem:**

SBI Life currently employs a persona-based recommendation system. While functional, this approach lacks the depth of individual customer understanding, resulting in generic recommendations that fail to resonate with unique preferences and needs. This limits engagement and ultimately impacts conversion rates and customer retention.

**Solution:**

Our solution is an intelligent chatbot powered by **Retrieval-Augmented Generation (RAG)** and a **Vector Database (Pinecone)**. This chatbot dynamically adapts to each customer by:

*   **Deepening Individual-Centric Insights:**  By storing and understanding past customer interactions, the chatbot builds a rich, individual profile beyond static personas.
*   **Optimizing Upselling Strategies:**  The chatbot can suggest tailored policy terms, coverage amounts, and durations based on the context of the conversation and retrieved similar successful interactions.
*   **Improving Customer Persistency:**  Through personalized and relevant conversations, the chatbot enhances the likelihood of prospective customers closing deals and encourages existing customers to maintain their policies.

**Key Features:**

*   **Personalized Conversations:**  Leverages past conversation history (stored in Pinecone) to provide contextually relevant and tailored responses.
*   **RAG-Based Approach:**  Uses Retrieval-Augmented Generation to ground chatbot responses in relevant information, making interactions more informative and helpful.
*   **Vector Database (Pinecone):**  Employs Pinecone for efficient storage and retrieval of conversation embeddings, enabling fast similarity searches for context retrieval.
*   **Sentence Transformer Embeddings:** Utilizes Sentence Transformers to generate high-quality vector embeddings of conversation turns, capturing semantic meaning for accurate context matching.
*   **Scalable Backend (Flask):**  Built with a Flask backend in Python for scalability, robustness, and easy integration with other systems.
*   **Interactive Frontend (React):**  Features a user-friendly and engaging chat interface built with React, providing a seamless customer experience.
*   **Easy to Extend:**  Modular architecture allows for future enhancements like integration with Language Models (LLMs) for more sophisticated response generation, sentiment analysis, and deeper customer profile enrichment.



## Getting Started

Follow these steps to set up and run the SBI Life AI Chatbot on your local machine.

**Prerequisites:**

*   **Python 3.7+**
*   **Node.js and npm (or yarn)**
*   **Pinecone API Key and Environment:**  You need to create a Pinecone account and obtain your API key and environment from [https://app.pinecone.io/](https://app.pinecone.io/).

**Installation and Setup:**

1.  **Clone the repository:**
    ```bash
    git clone [repository URL]
    cd sbi_life_chatbot
    ```

2.  **Set up Backend:**
    *   Navigate to the `backend` directory:
        ```bash
        cd backend
        ```
    *   Create a virtual environment:
        ```bash
        python -m venv venv
        ```
    *   Activate the virtual environment:
        ```bash
        source venv/bin/activate  # On Linux/macOS
        # venv\Scripts\activate  # On Windows
        ```
    *   Install Python dependencies:
        ```bash
        pip install -r requirements.txt
        ```
    *   Create a `.env` file in the `backend/` directory and add your Pinecone API key and environment:
        ```
        PINECONE_API_KEY=YOUR_PINECONE_API_KEY
        PINECONE_ENVIRONMENT=YOUR_PINECONE_ENVIRONMENT
        ```
        **Replace `YOUR_PINECONE_API_KEY` and `YOUR_PINECONE_ENVIRONMENT` with your actual Pinecone credentials.**

3.  **Set up Pinecone Index:**
    *   If you haven't already, create a Pinecone index named `sbi-life-conversations-index` (or the name specified in `backend/src/config/config.py`) in your Pinecone project. The index should have a dimension of 384 and use cosine similarity.

4.  **Run Backend:**
    *   From the `backend/` directory, run the Flask backend:
        ```bash
        python run.py
        ```
        The backend API will start running on `http://127.0.0.1:5000`.

5.  **Set up Frontend:**
    *   Navigate back to the project root and then to the `frontend` directory:
        ```bash
        cd ../frontend
        ```
    *   Install frontend dependencies:
        ```bash
        npm install  # or yarn install
        ```

6.  **Run Frontend:**
    *   From the `frontend/` directory, start the React development server:
        ```bash
        npm start  # or yarn start
        ```
        The React frontend will usually open in your browser at `http://localhost:3000`.

**Usage:**

1.  Open the chatbot interface in your browser (usually `http://localhost:3000`).
2.  Start interacting with the chatbot by typing messages in the input area and pressing "Send" or Enter.
3.  Observe the chatbot's responses.  Initially, the chatbot will provide placeholder responses. As you develop the RAG logic in the backend, you will see more personalized and context-aware responses based on the conversation history.

## Technologies Used

*   **Backend:**
    *   Python
    *   Flask (Web Framework)
    *   Sentence Transformers (for Embeddings)
    *   Pinecone Client (for Vector Database)
    *   python-dotenv (for Environment Variable Management)
*   **Frontend:**
    *   React
    *   Lucide React (for Icons)
    *   Tailwind CSS (for Styling - via create-react-app default)
*   **Vector Database:**
    *   Pinecone

## Challenges and Future Enhancements

**Current Challenges:**

*   **Basic RAG Implementation:** The current RAG logic is a placeholder.  Implementing a robust and effective RAG pipeline requires further development, including fine-tuning retrieval strategies and response generation.
*   **Limited Personalization:**  Personalization is currently based on storing and retrieving conversations. More advanced personalization could involve incorporating user profiles, preferences, and more sophisticated AI models.
*   **No LLM Integration (Yet):**  Response generation is currently placeholder-based. Integrating a Language Model (LLM) like GPT-3.5/4 or open-source models is a crucial next step for generating more natural and intelligent chatbot responses.

**Future Enhancements:**

*   **Integrate a Language Model (LLM):**  Use an LLM to generate more fluent, contextually relevant, and creative chatbot responses based on retrieved context from Pinecone.
*   **Implement Advanced RAG Techniques:** Explore techniques like query expansion, re-ranking, and more sophisticated prompt engineering to improve retrieval accuracy and response quality.
*   **Sentiment Analysis:** Incorporate sentiment analysis to understand customer emotions and tailor responses accordingly (especially for handling negative sentiment effectively).
*   **Customer Profile Enrichment:**  Expand customer profiles with more data points (demographics, policy information, purchase history) to enable even deeper personalization.
*   **Real-time Data Ingestion:**  Connect the chatbot to real-time data sources for up-to-date information and policy details.
*   **Improved UI/UX:**  Enhance the user interface and user experience of the chatbot based on user feedback and usability testing.
*   **Deployment to Cloud Platform:**  Deploy the chatbot to a cloud platform (e.g., AWS, Azure, GCP) for scalability and production readiness.

## License

[MIT License](LICENSE) (Optional - Add a LICENSE file in the root directory if you choose to use a license)

## Author

[Your Name] - [Your GitHub Profile URL (optional)] - [Your Email (optional)]

Feel free to contribute to this project by submitting pull requests or opening issues for bug reports and feature requests!
