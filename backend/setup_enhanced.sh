#!/bin/bash
# Enhanced Setup Script for SBI Chatbot with PostgreSQL MCP Integration

echo "🚀 Setting up Enhanced SBI Chatbot Environment"
echo "=============================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Python version
echo "🐍 Checking Python environment..."
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo "✅ Python found: $PYTHON_VERSION"
else
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

# Check PostgreSQL
echo "🗄️ Checking PostgreSQL..."
if command_exists psql; then
    echo "✅ PostgreSQL found"
else
    echo "❌ PostgreSQL not found. Please install PostgreSQL"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo "📦 Installing/updating dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🗄️ Setting up PostgreSQL database..."
if [ -f ".env" ]; then
    echo "✅ .env file found"
else
    echo "📝 Creating .env file template..."
    cat > .env << EOF
# Database Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=sbi_personalization
POSTGRES_USER=sbi_user
POSTGRES_PASSWORD=sbi_password_123
DATABASE_URL=postgresql://sbi_user:sbi_password_123@localhost:5432/sbi_personalization

# API Keys
GOOGLE_API_KEY=your_google_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Other configurations
SYSTEM_PROMPT_PATH=src/config/system_prompt.txt
EOF
    echo "⚠️ Please update .env file with your actual API keys and database credentials"
fi

echo "🔧 Initializing PostgreSQL MCP Server..."
python init_postgres_mcp.py

echo "🧪 Running MCP setup tests..."
python test_mcp_setup.py

echo ""
echo "🎉 Setup completed!"
echo "==================="
echo ""
echo "📋 NEXT STEPS:"
echo "1. Update .env file with your API keys"
echo "2. Start the Flask server: python run.py"
echo "3. Run integration tests: python test_integration.py"
echo "4. Monitor with dashboard: python monitor_dashboard.py"
echo "5. Start frontend: cd ../frontend && npm start"
echo ""
echo "🔗 Useful commands:"
echo "   🚀 Start backend:     python run.py"
echo "   🧪 Test integration:  python test_integration.py"
echo "   📊 Monitor dashboard: python monitor_dashboard.py"
echo "   🗄️ Test MCP:         python test_mcp_setup.py"
echo ""
echo "📚 Documentation:"
echo "   - README.md: Project overview"
echo "   - POSTGRES_MCP_SETUP.md: MCP server details"
echo "   - implementation.md: Technical implementation"
echo ""
echo "✨ Your enhanced SBI chatbot is ready with:"
echo "   ✅ PostgreSQL MCP Server integration"
echo "   ✅ Enhanced chat API with database storage"  
echo "   ✅ Customer profile management"
echo "   ✅ Real-time analytics and monitoring"
echo "   ✅ Multi-language support"
echo "   ✅ Gemini search with grounding"
