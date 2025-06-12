# PostgreSQL MCP Installation Guide for SBI Personalization Engine

This guide will help you set up PostgreSQL with Model Context Protocol (MCP) for the SBI Personalization Engine.

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

1. **Navigate to the backend directory:**
   ```bash
   cd /home/harisudhan/Documents/sbi/AI_Personalized_Customer-Retension_SBI/backend
   ```

2. **Run the automated setup script:**
   ```bash
   ./setup_postgres_mcp.sh
   ```

3. **Follow the prompts** to:
   - Install PostgreSQL (if not already installed)
   - Create database user and database
   - Install Python dependencies
   - Initialize database schema
   - Test the setup

### Option 2: Manual Setup

If you prefer manual installation or the automated script fails:

#### Step 1: Install PostgreSQL

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib postgresql-client
```

**CentOS/RHEL:**
```bash
sudo yum install postgresql-server postgresql-contrib
sudo postgresql-setup initdb
```

**Fedora:**
```bash
sudo dnf install postgresql-server postgresql-contrib
sudo postgresql-setup --initdb
```

#### Step 2: Start PostgreSQL Service

```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### Step 3: Create Database User and Database

```bash
sudo -u postgres psql
```

In the PostgreSQL prompt:
```sql
CREATE USER sbi_user WITH PASSWORD 'your_secure_password';
CREATE DATABASE sbi_personalization OWNER sbi_user;
GRANT ALL PRIVILEGES ON DATABASE sbi_personalization TO sbi_user;
\q
```

#### Step 4: Install Python Dependencies

```bash
# Make sure you're in a virtual environment (recommended)
pip install -r requirements.txt
```

#### Step 5: Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and update the following variables:
   ```env
   # PostgreSQL Configuration
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   POSTGRES_DB=sbi_personalization
   POSTGRES_USER=sbi_user
   POSTGRES_PASSWORD=your_secure_password
   DATABASE_URL=postgresql://sbi_user:your_secure_password@localhost:5432/sbi_personalization
   
   # API Keys (update with your actual keys)
   OPENAI_API_KEY=your_openai_api_key_here
   GOOGLE_API_KEY=your_google_api_key_here
   ```

#### Step 6: Initialize Database Schema

```bash
python init_postgres_mcp.py
```

## 🧪 Testing the Setup

### Test Database Connectivity

1. **Test PostgreSQL connection directly:**
   ```bash
   psql -h localhost -U sbi_user -d sbi_personalization -c "SELECT version();"
   ```

2. **Test through the application:**
   ```bash
   python run.py
   ```
   
   Then visit: `http://localhost:5000/api/database/status`

### Test MCP Functionality

1. **Start the Flask application:**
   ```bash
   python run.py
   ```

2. **Test the API endpoints:**
   ```bash
   # Check database status
   curl http://localhost:5000/api/database/status
   
   # Test customer profile (will create if doesn't exist)
   curl http://localhost:5000/api/customer/TEST_USER_001/profile
   
   # Test analytics
   curl http://localhost:5000/api/analytics/summary
   ```

## 📊 Database Schema Overview

The PostgreSQL MCP setup includes the following tables:

- **customers** - Customer information and profiles
- **conversations** - Chat conversation metadata
- **messages** - Individual chat messages with sentiment analysis
- **user_interactions** - Detailed interaction tracking
- **products** - Insurance product information
- **customer_preferences** - Customer preferences and interests
- **documents** - Uploaded PDF documents and metadata
- **document_chunks** - Document chunks for vector storage mapping
- **analytics_events** - User behavior analytics
- **mcp_operations** - MCP operation logging and monitoring

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `POSTGRES_HOST` | PostgreSQL host | `localhost` |
| `POSTGRES_PORT` | PostgreSQL port | `5432` |
| `POSTGRES_DB` | Database name | `sbi_personalization` |
| `POSTGRES_USER` | Database user | `sbi_user` |
| `POSTGRES_PASSWORD` | Database password | `sbi_password` |
| `DATABASE_URL` | Full database URL | Constructed from above |
| `MCP_SERVER_NAME` | MCP server identifier | `sbi-postgres-mcp` |

### PostgreSQL Configuration

The setup script automatically configures PostgreSQL for:
- Local connections on port 5432
- MD5 authentication for the `sbi_user`
- Optimized settings for the application

## 🚨 Troubleshooting

### Common Issues

1. **PostgreSQL service not starting:**
   ```bash
   sudo systemctl status postgresql
   sudo journalctl -u postgresql
   ```

2. **Connection refused errors:**
   - Check if PostgreSQL is running: `sudo systemctl status postgresql`
   - Verify port 5432 is open: `netstat -ln | grep 5432`
   - Check pg_hba.conf for authentication settings

3. **Permission denied errors:**
   - Ensure the `sbi_user` has correct permissions
   - Check database ownership: `sudo -u postgres psql -c "\l"`

4. **Python import errors:**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check virtual environment is activated

5. **MCP initialization fails:**
   - Verify database credentials in `.env`
   - Check PostgreSQL logs for connection issues
   - Ensure UUID extension is available: `sudo -u postgres psql -d sbi_personalization -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"`

### Logs and Debugging

1. **PostgreSQL logs:**
   ```bash
   sudo tail -f /var/log/postgresql/postgresql-*.log
   ```

2. **Application logs:**
   The Flask application logs to console. Increase log level in config if needed.

3. **MCP operation logs:**
   Check the `mcp_operations` table for operation history:
   ```sql
   SELECT * FROM mcp_operations ORDER BY created_at DESC LIMIT 10;
   ```

## 🔒 Security Considerations

1. **Database Security:**
   - Use strong passwords for database users
   - Restrict network access in production
   - Enable SSL/TLS for database connections in production

2. **Application Security:**
   - Keep API keys secure and use environment variables
   - Implement rate limiting for production
   - Use HTTPS in production environments

3. **PostgreSQL Hardening:**
   - Regular security updates
   - Proper firewall configuration
   - Database backup and recovery procedures

## 📈 Performance Optimization

1. **Database Indexing:**
   - The schema includes optimized indexes for common queries
   - Monitor query performance and add indexes as needed

2. **Connection Pooling:**
   - The MCP server uses connection pooling for efficiency
   - Adjust pool sizes based on load requirements

3. **FAISS Integration:**
   - Vector operations still use FAISS for performance
   - PostgreSQL stores structured metadata and relationships

## 🔄 Backup and Recovery

1. **Database Backup:**
   ```bash
   pg_dump -h localhost -U sbi_user sbi_personalization > backup.sql
   ```

2. **Database Restore:**
   ```bash
   psql -h localhost -U sbi_user sbi_personalization < backup.sql
   ```

3. **FAISS Index Backup:**
   The FAISS index files are stored in the backend directory and should be backed up separately.

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review the application logs
3. Verify your environment configuration
4. Ensure all dependencies are properly installed

## 🎯 Next Steps

After successful installation:

1. **Configure API Keys:** Update `.env` with your actual OpenAI and Google API keys
2. **Test Integration:** Run the full application and test all endpoints
3. **Upload Documents:** Use the PDF upload feature to populate the knowledge base
4. **Monitor Performance:** Use the analytics endpoints to monitor system performance
5. **Scale as Needed:** Adjust PostgreSQL and connection pool settings based on usage
