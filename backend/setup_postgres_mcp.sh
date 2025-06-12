#!/bin/bash

# PostgreSQL MCP Setup Script for SBI Personalization Engine
# This script sets up PostgreSQL, installs dependencies, and configures the database

set -e  # Exit on any error

echo "🚀 Setting up PostgreSQL MCP for SBI Personalization Engine..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root (not recommended for this setup)
if [[ $EUID -eq 0 ]]; then
   print_warning "This script should not be run as root for security reasons."
   echo "Please run as a regular user with sudo privileges."
   exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install PostgreSQL
install_postgresql() {
    print_status "Installing PostgreSQL..."
    
    if command_exists apt-get; then
        # Ubuntu/Debian
        sudo apt-get update
        sudo apt-get install -y postgresql postgresql-contrib postgresql-client
    elif command_exists yum; then
        # CentOS/RHEL
        sudo yum install -y postgresql-server postgresql-contrib
        sudo postgresql-setup initdb
    elif command_exists dnf; then
        # Fedora
        sudo dnf install -y postgresql-server postgresql-contrib
        sudo postgresql-setup --initdb
    else
        print_error "Unsupported package manager. Please install PostgreSQL manually."
        exit 1
    fi
    
    # Start and enable PostgreSQL
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
    
    print_status "PostgreSQL installed and started successfully!"
}

# Function to configure PostgreSQL
configure_postgresql() {
    print_status "Configuring PostgreSQL..."
    
    # Get PostgreSQL version for config path
    PG_VERSION=$(sudo -u postgres psql -t -c "SHOW server_version;" | grep -o '[0-9]\+' | head -1)
    
    if [ -z "$PG_VERSION" ]; then
        print_error "Could not determine PostgreSQL version"
        exit 1
    fi
    
    # Common config paths
    PG_CONFIG_PATHS=(
        "/etc/postgresql/$PG_VERSION/main/postgresql.conf"
        "/var/lib/pgsql/data/postgresql.conf"
        "/var/lib/postgresql/data/postgresql.conf"
    )
    
    PG_HBA_PATHS=(
        "/etc/postgresql/$PG_VERSION/main/pg_hba.conf"
        "/var/lib/pgsql/data/pg_hba.conf"
        "/var/lib/postgresql/data/pg_hba.conf"
    )
    
    # Find the correct config file
    PG_CONFIG=""
    PG_HBA=""
    
    for path in "${PG_CONFIG_PATHS[@]}"; do
        if [ -f "$path" ]; then
            PG_CONFIG="$path"
            break
        fi
    done
    
    for path in "${PG_HBA_PATHS[@]}"; do
        if [ -f "$path" ]; then
            PG_HBA="$path"
            break
        fi
    done
    
    if [ -z "$PG_CONFIG" ] || [ -z "$PG_HBA" ]; then
        print_error "Could not find PostgreSQL configuration files"
        exit 1
    fi
    
    print_status "Found PostgreSQL config at: $PG_CONFIG"
    print_status "Found pg_hba.conf at: $PG_HBA"
    
    # Backup original configs
    sudo cp "$PG_CONFIG" "$PG_CONFIG.backup.$(date +%Y%m%d_%H%M%S)"
    sudo cp "$PG_HBA" "$PG_HBA.backup.$(date +%Y%m%d_%H%M%S)"
    
    # Configure PostgreSQL for local connections
    sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = 'localhost'/" "$PG_CONFIG"
    sudo sed -i "s/#port = 5432/port = 5432/" "$PG_CONFIG"
    
    # Configure authentication for local connections
    if ! grep -q "local   all             sbi_user" "$PG_HBA"; then
        sudo sed -i "/^local   all             all/a local   all             sbi_user                                md5" "$PG_HBA"
    fi
    
    if ! grep -q "host    all             sbi_user.*127.0.0.1/32" "$PG_HBA"; then
        sudo sed -i "/^host    all             all.*127.0.0.1/a host    all             sbi_user        127.0.0.1/32            md5" "$PG_HBA"
    fi
    
    # Restart PostgreSQL to apply changes
    sudo systemctl restart postgresql
    
    print_status "PostgreSQL configuration updated!"
}

# Function to install Python dependencies
install_python_dependencies() {
    print_status "Installing Python dependencies..."
    
    # Check if we're in a virtual environment
    if [[ "$VIRTUAL_ENV" != "" ]]; then
        print_status "Virtual environment detected: $VIRTUAL_ENV"
    else
        print_warning "No virtual environment detected. Consider using one for isolation."
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    
    # Install requirements
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        print_status "Python dependencies installed!"
    else
        print_error "requirements.txt not found in current directory"
        exit 1
    fi
}

# Function to create database and user
setup_database() {
    print_status "Setting up database and user..."
    
    # Prompt for password
    echo "Enter password for PostgreSQL user 'sbi_user':"
    read -s SBI_PASSWORD
    echo
    
    # Create user and database
    sudo -u postgres psql << EOF
-- Create user
DO \$\$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_user WHERE usename = 'sbi_user') THEN
        CREATE USER sbi_user WITH PASSWORD '$SBI_PASSWORD';
    END IF;
END
\$\$;

-- Create database
SELECT 'CREATE DATABASE sbi_personalization OWNER sbi_user'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'sbi_personalization');

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE sbi_personalization TO sbi_user;

\q
EOF

    print_status "Database and user created successfully!"
    
    # Create .env file if it doesn't exist
    if [ ! -f ".env" ]; then
        print_status "Creating .env file..."
        cp .env.example .env
        
        # Update database password in .env
        sed -i "s/POSTGRES_PASSWORD=sbi_password/POSTGRES_PASSWORD=$SBI_PASSWORD/" .env
        
        print_status ".env file created. Please update it with your API keys."
    else
        print_status ".env file already exists. Please ensure POSTGRES_PASSWORD is set correctly."
    fi
}

# Function to initialize database schema
initialize_schema() {
    print_status "Initializing database schema..."
    
    if [ -f "init_postgres_mcp.py" ]; then
        python init_postgres_mcp.py
        print_status "Database schema initialized!"
    else
        print_error "init_postgres_mcp.py not found"
        exit 1
    fi
}

# Function to test the setup
test_setup() {
    print_status "Testing the setup..."
    
    # Test PostgreSQL connection
    if PGPASSWORD=$SBI_PASSWORD psql -h localhost -U sbi_user -d sbi_personalization -c "SELECT version();" >/dev/null 2>&1; then
        print_status "✅ PostgreSQL connection test passed!"
    else
        print_error "❌ PostgreSQL connection test failed!"
        return 1
    fi
    
    # Test Python imports
    if python -c "from src.database.postgres_mcp_server import mcp_server; print('✅ MCP imports successful!')" 2>/dev/null; then
        print_status "✅ Python MCP imports test passed!"
    else
        print_error "❌ Python MCP imports test failed!"
        return 1
    fi
    
    print_status "🎉 All tests passed! Setup completed successfully!"
    return 0
}

# Main execution
main() {
    echo "=========================================="
    echo "PostgreSQL MCP Setup for SBI Engine"
    echo "=========================================="
    echo
    
    # Check if PostgreSQL is already installed
    if command_exists psql; then
        print_status "PostgreSQL is already installed."
        if sudo systemctl is-active --quiet postgresql; then
            print_status "PostgreSQL service is running."
        else
            print_status "Starting PostgreSQL service..."
            sudo systemctl start postgresql
        fi
    else
        install_postgresql
    fi
    
    # Configure PostgreSQL
    configure_postgresql
    
    # Install Python dependencies
    install_python_dependencies
    
    # Setup database
    setup_database
    
    # Initialize schema
    initialize_schema
    
    # Test setup
    if test_setup; then
        echo
        print_status "🚀 Setup completed successfully!"
        echo
        echo "Next steps:"
        echo "1. Update your .env file with the correct API keys"
        echo "2. Run: python run.py"
        echo "3. Test the database endpoints at /api/database/status"
        echo
    else
        print_error "Setup completed with errors. Please check the logs above."
        exit 1
    fi
}

# Run main function
main "$@"
