# AI-Powered Personalized Customer Retention Chatbot for SBI Life Insurance

[![Contribute](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg)](CONTRIBUTING.md)

This project leverages AI to enhance customer retention for SBI Life Insurance by moving beyond persona-based recommendations to deliver truly personalized, individual-centric experiences.  The chatbot analyzes customer interactions to understand their unique preferences and needs, optimizing upselling strategies and improving customer persistency.

## Project Description

SBI Life currently utilizes a broad, persona-based approach for customer recommendations, which lacks individual-level depth and often fails to resonate with unique customer preferences. This project aims to solve this by building an AI-driven chatbot that:

*   **Deepens Individual-Centric Insights:**  Develops a personalized understanding of customer behavior, preferences, and needs based on their interactions.
*   **Optimizes Upselling Strategies:** Suggests tailored policy terms, ticket prices, and durations to increase customer satisfaction and policy upgrades.
*   **Improves Customer Persistency:** Enhances the likelihood of prospective customers closing deals and existing customers maintaining their policies by providing relevant and personalized guidance.

This chatbot leverages Retrieval-Augmented Generation (RAG) with OpenAI to provide contextually relevant and personalized responses based on similar past customer interactions stored in a vector database.

## Tech Stack

*   **Frontend:**
    *   React
    *   JavaScript (ES6+)
    *   CSS
    *   npm/Node.js
    *   Lucide React (Icons)

*   **Backend:**
    *   Python
    *   Flask
    *   Sentence Transformers (for embeddings)
    *   LLM (for response generation)
    *   Pinecone (Vector Database)
    *   PyMuPDF (for PDF processing)

## Problem Statement

SBI Life currently relies on a 1000+ user persona-based approach for customer behavior recommendation, which limits the depth of individual-centric analysis and fails to resonate with their unique preference, reducing the likelihood of conversion.

## Goal

To leverage AI to:

*   **Deepen individual-centric insights:** Develop a more personalized understanding of customer behavior, preferences, and needs.
*   **Optimize upselling strategies:** Suggest tailored policy terms, ticket prices, and durations to increase customer satisfaction and retention.
*   **Improve customer persistency:** Enhance the likelihood of prospective customers closing deals and existing customers maintaining their policies.

## Key Features

*   **Personalized Chatbot Interface:** A user-friendly React-based chatbot interface for customer interaction.
*   **AI-Powered Recommendations:**  Utilizes Custom_LLM and RAG to generate personalized responses and recommendations based on context and past interactions.
*   **Vector Database (Pinecone) Integration:** Stores and retrieves conversation embeddings for semantic similarity search and personalized context.
*   **Dynamic Persona Creation:**  For returning customers, the chatbot builds a dynamic "persona" based on their individual interaction history.
*   **Similarity-Based Guidance:** For new customers, the chatbot leverages similar past customer interactions to guide them towards successful purchase paths.
*   **Scalable Backend:**  Built with Flask and Python for a modular and scalable backend architecture.
*   **PDF Data Ingestion:**  Includes scripts to ingest PDF policy documents into the Pinecone knowledge base.
*   **Audio Support (Future Enhancement):**  Planned feature to enable voice input and output for a more seamless user experience.
*   **Accurate RAG with SBI Data Sources:**  Focuses on utilizing official SBI Life data sources to ensure accurate and reliable information retrieval for RAG.
*   **Sales and Support Guidance:** Aims to provide effective sales guidance and customer support information within the chatbot conversations.
*   **Multi-Language Support (Future Enhancement):**  Intended to support multiple languages, including Hindi and English, to cater to a wider customer base.
*   **Individual Customer Persona:** Leverages historical customer data to create and refine individual customer personas for deeper personalization.
*   **And More:**  Continuously evolving with new features and improvements to enhance customer retention and personalization.

## Getting Started

To run this project locally, follow these steps:

**Backend Setup:**

1.  Navigate to the `backend` directory: `cd backend`
2.  Create a virtual environment (optional but recommended): `python -m venv venv`
3.  Activate the virtual environment:
    *   On Windows: `venv\Scripts\activate`
    *   On macOS/Linux: `source venv/bin/activate`
4.  Install backend dependencies: `pip install -r requirements.txt`
5.  Set your environment variables:
    *   `PINECONE_API_KEY`
    *   `PINECONE_ENVIRONMENT`
    *   `PINECONE_INDEX_NAME`
    (You can set these in a `.env` file in the `backend` directory)
6.  Run the Flask backend: `python run.py`

**Frontend Setup:**

1.  Navigate to the `frontend` directory: `cd frontend`
2.  Install frontend dependencies: `npm install` or `yarn install`
3.  Start the React frontend development server: `npm start` or `yarn start`

The chatbot interface should now be accessible in your browser, usually at `http://localhost:3000`. The backend API will be running at `http://127.0.0.1:5000`.

## Contributing

This project is open for contributions! If you'd like to contribute to enhance this project, please feel free to submit Pull Requests or create Issues to discuss potential improvements and bug fixes.

**Contributors:**

*   **ARUNKUMAR V:** [GitHub Profile](https://github.com/akv2011)
*   **HARIHARA SUDHAN:** [GitHub Profile](https://github.com/Harihara04sudhan)

**Contact:**

*   arunkumarv1530@gmail.com
*   harisudhan2284@gmail.com

💡 Feel free to contribute! Submit PRs or issues to enhance this project. 🚀
