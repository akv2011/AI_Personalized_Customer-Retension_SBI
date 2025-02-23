# AI-Powered Customer Retention & Personalization for SBI Life

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## **Project Overview**
This project implements an **AI-driven chatbot** to enhance customer interaction for **SBI Life Insurance**. Unlike traditional persona-based approaches, this chatbot utilizes **Retrieval-Augmented Generation (RAG)** and **Vector Database (Pinecone)** to offer **hyper-personalized experiences**, increasing customer satisfaction, policy persistency, and conversion rates.

### **Problem Statement**
SBI Life currently employs a **persona-based recommendation system**, which limits deep personalization. This results in **generic recommendations** that do not effectively engage customers, affecting **conversion rates and retention**.

### **Solution**
Our intelligent chatbot dynamically adapts to each customer by:
✅ **Deepening Individual Insights** – Stores & analyzes past interactions to build a **rich customer profile**.  
✅ **Optimizing Upselling Strategies** – AI suggests tailored **policy terms, coverage, and duration** based on successful interactions.  
✅ **Improving Customer Persistency** – Engages customers with **relevant and meaningful conversations**, reducing policy lapses.  

## **Key Features**
✔️ **Personalized AI Conversations** – Uses past interactions for **context-aware responses**.  
✔️ **Retrieval-Augmented Generation (RAG)** – Improves chatbot responses with **relevant historical data and various SBI_Guide docs knowledge**.  
✔️ **Vector Database (Pinecone)** – Efficiently stores and retrieves conversation embeddings for **fast similarity searches**.  
✔️ **Sentence Transformer Embeddings** – Captures **semantic meaning** for accurate context matching.  
✔️ **Scalable Flask Backend** – Ensures **robust and seamless integration** with SBI Life’s ecosystem.  
✔️ **Interactive React Frontend** – Provides a **smooth, user-friendly chat experience**.  
✔️ **Future-Ready Architecture** – Supports **LLM integration, sentiment analysis, and deep profile enrichment**.  

---
## **Getting Started**
### **Prerequisites**
- **Python 3.7+**
- **Node.js & npm (or yarn)**
- **Pinecone API Key & Environment** (Create an account at [Pinecone](https://app.pinecone.io/))

### **Installation & Setup**
#### **1. Clone the Repository**
```bash
git clone [repository URL]
cd sbi_life_chatbot
```

#### **2. Set Up Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Linux/macOS
# venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

Create a `.env` file and add your Pinecone credentials:
```plaintext
PINECONE_API_KEY=YOUR_PINECONE_API_KEY
PINECONE_ENVIRONMENT=YOUR_PINECONE_ENVIRONMENT
```

#### **3. Set Up Pinecone Index**
Ensure you create a Pinecone index named `sbi-life-conversations-index` (dimension: 384, cosine similarity).

#### **4. Run Backend**
```bash
python run.py
```
API will be available at `http://127.0.0.1:5000`.

#### **5. Set Up Frontend**
```bash
cd ../frontend
npm install  # or yarn install
npm start  # or yarn start
```
Frontend will open at `http://localhost:3000`.

### **Usage**
1. Open the chatbot at `http://localhost:3000`.
2. Start interacting by typing queries.
3. Experience **personalized AI responses** based on past interactions.

---
## **Technologies Used**
### **Backend**
- Python
- Flask (Web Framework)
- Sentence Transformers (Embeddings)
- Pinecone (Vector Database)
- dotenv (Environment Variables)

### **Frontend**
- React.js
- Lucide React (Icons)
- Tailwind CSS (Styling)

### **Cloud & Security**
- AWS/GCP/Azure (for scalability)
- OAuth 2.0 / JWT Authentication
- GDPR-compliant data handling

---
## **Challenges & Future Enhancements**
### **Current Challenges**
🚧 **Basic RAG Implementation** – Further tuning required for improved retrieval accuracy.  
🚧 **Limited Personalization** – Future AI models will integrate customer profiles and preferences.  
🚧 **No LLM Integration (Yet)** – Placeholder-based responses will evolve into **LLM-powered natural responses**.  

### **Future Enhancements**
🚀 **Integrate a Language Model (LLM)** – For **fluent, AI-generated responses**.  
🚀 **Advanced RAG Techniques** – Query expansion, re-ranking, and prompt optimization.  
🚀 **Sentiment Analysis** – Detects emotions for **enhanced customer engagement**.  
🚀 **Customer Profile Enrichment** – Expands personalization using **demographics & policy history**.  
🚀 **Real-time Data Ingestion** – Keeps chatbot up-to-date with latest **policy details**.  
🚀 **Cloud Deployment** – Scalable hosting for **production-ready implementation**.  

---
## **License**
[MIT License](LICENSE)  

## **Author**
HARIHARA SUDHAN - [[GitHub Profile]](https://github.com/Harihara04sudhan) - harisudhan2284@gmail.com

💡 *Feel free to contribute! Submit PRs or issues to enhance this project.* 🚀

