"""
SQLAlchemy Models for SBI Personalization Engine
"""
from sqlalchemy import Column, String, DateTime, Text, Boolean, Float, Integer, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
import uuid

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(String(255), unique=True, nullable=False, index=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255))
    phone = Column(String(20))
    date_of_birth = Column(Date)
    preferred_language = Column(String(10), default='en')
    customer_segment = Column(String(100))
    risk_profile = Column(String(50))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    conversations = relationship("Conversation", back_populates="customer")
    messages = relationship("Message", back_populates="customer")
    interactions = relationship("UserInteraction", back_populates="customer")
    preferences = relationship("CustomerPreference", back_populates="customer")
    analytics_events = relationship("AnalyticsEvent", back_populates="customer")

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(String(255), unique=True, nullable=False, index=True)
    customer_id = Column(String(255), ForeignKey('customers.customer_id'), nullable=False)
    title = Column(String(500))
    status = Column(String(50), default='active')
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    customer = relationship("Customer", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")
    interactions = relationship("UserInteraction", back_populates="conversation")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    message_id = Column(String(255), unique=True, nullable=False)
    conversation_id = Column(String(255), ForeignKey('conversations.conversation_id'), nullable=False)
    customer_id = Column(String(255), ForeignKey('customers.customer_id'), nullable=False)
    speaker = Column(String(50), nullable=False)  # 'customer', 'assistant', 'system'
    message_text = Column(Text, nullable=False)
    message_type = Column(String(50), default='chatbot')  # 'chatbot', 'gemini_search', 'guidance'
    sentiment = Column(String(50))  # 'Positive', 'Negative', 'Neutral'
    language = Column(String(10), default='en')
    embedding_id = Column(String(255))  # Reference to FAISS vector ID
    metadata = Column(JSONB)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    customer = relationship("Customer", back_populates="messages")
    conversation = relationship("Conversation", back_populates="messages")

class UserInteraction(Base):
    __tablename__ = "user_interactions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    interaction_id = Column(String(255), unique=True, nullable=False)
    customer_id = Column(String(255), ForeignKey('customers.customer_id'), nullable=False)
    conversation_id = Column(String(255), ForeignKey('conversations.conversation_id'))
    interaction_type = Column(String(100), nullable=False)
    interaction_data = Column(JSONB, nullable=False)
    outcome = Column(String(100))
    response_time_ms = Column(Integer)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    customer = relationship("Customer", back_populates="interactions")
    conversation = relationship("Conversation", back_populates="interactions")

class Product(Base):
    __tablename__ = "products"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(String(255), unique=True, nullable=False)
    product_name = Column(String(500), nullable=False)
    product_type = Column(String(100))
    description = Column(Text)
    key_features = Column(JSONB)
    eligibility_criteria = Column(JSONB)
    premium_details = Column(JSONB)
    benefits = Column(JSONB)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

class CustomerPreference(Base):
    __tablename__ = "customer_preferences"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(String(255), ForeignKey('customers.customer_id'), nullable=False)
    preference_type = Column(String(100), nullable=False)
    preference_value = Column(JSONB, nullable=False)
    confidence_score = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    customer = relationship("Customer", back_populates="preferences")

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(String(255), unique=True, nullable=False)
    filename = Column(String(500), nullable=False)
    file_path = Column(Text)
    document_type = Column(String(100))
    content_text = Column(Text)
    chunk_count = Column(Integer, default=0)
    processing_status = Column(String(50), default='pending')
    upload_source = Column(String(100))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    processed_at = Column(DateTime(timezone=True))
    
    # Relationships
    chunks = relationship("DocumentChunk", back_populates="document")

class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chunk_id = Column(String(255), unique=True, nullable=False)
    document_id = Column(String(255), ForeignKey('documents.document_id'), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    chunk_text = Column(Text, nullable=False)
    chunk_metadata = Column(JSONB)
    vector_id = Column(String(255))  # Reference to FAISS vector ID
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    document = relationship("Document", back_populates="chunks")

class AnalyticsEvent(Base):
    __tablename__ = "analytics_events"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(String(255), unique=True, nullable=False)
    customer_id = Column(String(255), ForeignKey('customers.customer_id'))
    event_type = Column(String(100), nullable=False)
    event_data = Column(JSONB, nullable=False)
    session_id = Column(String(255))
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    customer = relationship("Customer", back_populates="analytics_events")

class MCPOperation(Base):
    __tablename__ = "mcp_operations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    operation_id = Column(String(255), unique=True, nullable=False)
    operation_type = Column(String(100), nullable=False)
    table_name = Column(String(100))
    operation_data = Column(JSONB)
    status = Column(String(50), default='pending')
    error_message = Column(Text)
    execution_time_ms = Column(Integer)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    completed_at = Column(DateTime(timezone=True))
