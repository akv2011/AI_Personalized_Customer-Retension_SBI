-- PostgreSQL Schema for SBI Personalization Engine with MCP Support
-- Database: sbi_personalization

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Customer table for storing customer information
CREATE TABLE IF NOT EXISTS customers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(20),
    date_of_birth DATE,
    preferred_language VARCHAR(10) DEFAULT 'en',
    customer_segment VARCHAR(100),
    risk_profile VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Conversations table for storing chat conversations
CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id VARCHAR(255) UNIQUE NOT NULL,
    customer_id VARCHAR(255) NOT NULL,
    title VARCHAR(500),
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Messages table for storing individual messages
CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    message_id VARCHAR(255) UNIQUE NOT NULL,
    conversation_id VARCHAR(255) NOT NULL,
    customer_id VARCHAR(255) NOT NULL,
    speaker VARCHAR(50) NOT NULL, -- 'customer', 'assistant', 'system'
    message_text TEXT NOT NULL,
    message_type VARCHAR(50) DEFAULT 'chatbot', -- 'chatbot', 'gemini_search', 'guidance'
    sentiment VARCHAR(50), -- 'Positive', 'Negative', 'Neutral'
    language VARCHAR(10) DEFAULT 'en',
    embedding_id VARCHAR(255), -- Reference to FAISS vector ID
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- User interactions table for detailed interaction tracking
CREATE TABLE IF NOT EXISTS user_interactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    interaction_id VARCHAR(255) UNIQUE NOT NULL,
    customer_id VARCHAR(255) NOT NULL,
    conversation_id VARCHAR(255),
    interaction_type VARCHAR(100) NOT NULL, -- 'chat', 'search', 'pdf_upload', 'guidance_request'
    interaction_data JSONB NOT NULL,
    outcome VARCHAR(100), -- 'successful', 'failed', 'pending'
    response_time_ms INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id)
);

-- Products table for insurance products
CREATE TABLE IF NOT EXISTS products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_id VARCHAR(255) UNIQUE NOT NULL,
    product_name VARCHAR(500) NOT NULL,
    product_type VARCHAR(100), -- 'term_insurance', 'endowment', 'ulip', etc.
    description TEXT,
    key_features JSONB,
    eligibility_criteria JSONB,
    premium_details JSONB,
    benefits JSONB,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Customer interests and preferences
CREATE TABLE IF NOT EXISTS customer_preferences (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id VARCHAR(255) NOT NULL,
    preference_type VARCHAR(100) NOT NULL, -- 'product_interest', 'communication_preference', etc.
    preference_value JSONB NOT NULL,
    confidence_score FLOAT DEFAULT 0.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- PDF documents and processed content
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id VARCHAR(255) UNIQUE NOT NULL,
    filename VARCHAR(500) NOT NULL,
    file_path TEXT,
    document_type VARCHAR(100), -- 'brochure', 'policy_document', 'faq', etc.
    content_text TEXT,
    chunk_count INTEGER DEFAULT 0,
    processing_status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'processed', 'failed'
    upload_source VARCHAR(100), -- 'admin_upload', 'customer_query', etc.
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP WITH TIME ZONE
);

-- Document chunks for vector storage mapping
CREATE TABLE IF NOT EXISTS document_chunks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chunk_id VARCHAR(255) UNIQUE NOT NULL,
    document_id VARCHAR(255) NOT NULL,
    chunk_index INTEGER NOT NULL,
    chunk_text TEXT NOT NULL,
    chunk_metadata JSONB,
    vector_id VARCHAR(255), -- Reference to FAISS vector ID
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (document_id) REFERENCES documents(document_id)
);

-- Analytics and metrics
CREATE TABLE IF NOT EXISTS analytics_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_id VARCHAR(255) UNIQUE NOT NULL,
    customer_id VARCHAR(255),
    event_type VARCHAR(100) NOT NULL, -- 'page_view', 'chat_start', 'product_interest', etc.
    event_data JSONB NOT NULL,
    session_id VARCHAR(255),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- MCP operations log
CREATE TABLE IF NOT EXISTS mcp_operations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    operation_id VARCHAR(255) UNIQUE NOT NULL,
    operation_type VARCHAR(100) NOT NULL, -- 'query', 'insert', 'update', 'delete'
    table_name VARCHAR(100),
    operation_data JSONB,
    status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'completed', 'failed'
    error_message TEXT,
    execution_time_ms INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE
);

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_customers_customer_id ON customers(customer_id);
CREATE INDEX IF NOT EXISTS idx_conversations_customer_id ON conversations(customer_id);
CREATE INDEX IF NOT EXISTS idx_conversations_created_at ON conversations(created_at);
CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_messages_customer_id ON messages(customer_id);
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at);
CREATE INDEX IF NOT EXISTS idx_user_interactions_customer_id ON user_interactions(customer_id);
CREATE INDEX IF NOT EXISTS idx_user_interactions_type ON user_interactions(interaction_type);
CREATE INDEX IF NOT EXISTS idx_customer_preferences_customer_id ON customer_preferences(customer_id);
CREATE INDEX IF NOT EXISTS idx_document_chunks_document_id ON document_chunks(document_id);
CREATE INDEX IF NOT EXISTS idx_document_chunks_vector_id ON document_chunks(vector_id);
CREATE INDEX IF NOT EXISTS idx_analytics_events_customer_id ON analytics_events(customer_id);
CREATE INDEX IF NOT EXISTS idx_analytics_events_type ON analytics_events(event_type);
CREATE INDEX IF NOT EXISTS idx_mcp_operations_type ON mcp_operations(operation_type);
CREATE INDEX IF NOT EXISTS idx_mcp_operations_status ON mcp_operations(status);

-- Functions for automatic timestamp updates
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for automatic timestamp updates
CREATE TRIGGER update_customers_updated_at BEFORE UPDATE ON customers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_conversations_updated_at BEFORE UPDATE ON conversations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_products_updated_at BEFORE UPDATE ON products
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_customer_preferences_updated_at BEFORE UPDATE ON customer_preferences
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();