# 🚀 Debugger AI Setup Guide

## Quick Start

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy the template
cp .env.template .env

# Edit .env with your API keys
# Minimum required: GEMINI_API_KEY
```

### 3. Start the Server
```bash
# Method 1: Using the run script (recommended)
python run.py

# Method 2: Direct uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Test the API
Open http://localhost:8000/docs in your browser to see the API documentation.

### 5. Use the Frontend
Open `frontend/index.html` in your browser for a user-friendly interface.

## 📋 API Keys Setup

### Google Gemini (Required)
1. Go to https://console.cloud.google.com/apis/credentials
2. Create a new API key
3. Add to .env: `GEMINI_API_KEY=AIza...`

### ChromaDB (Automatic - for vector search)
ChromaDB runs locally with persistent storage. No API key required.
Data is stored in: `./chroma_data/`

**Note**: ChromaDB is pinned to v0.4.18 with NumPy <2.0 for stability and compatibility.

### Reddit (Optional - for Reddit search)
1. Go to https://www.reddit.com/prefs/apps/
2. Create a new app (script type)
3. Add to .env:
   ```
   REDDIT_CLIENT_ID=...
   REDDIT_CLIENT_SECRET=...
   ```

## 🧪 Testing

### Test API Connections
```bash
python -m app.utils.setup_utils
```

### Test with curl
```bash
curl -X POST "http://localhost:8000/debug/" \
     -H "Content-Type: application/json" \
     -d '{
       "error": "NameError: name '\''pd'\'' is not defined",
       "code": "df = pd.DataFrame({'\''A'\'': [1, 2, 3]})"
     }'
```

### Run Unit Tests
```bash
pytest tests/
```

## 🔧 Advanced Setup

### Vector Database Population
```bash
# Populate vector database with common errors
python -m app.ingestion.data_ingestion
```

### Docker Deployment
```bash
docker build -t debugger-ai .
docker run -p 8000:8000 --env-file .env debugger-ai
```

## 📊 Usage Examples

### Python Error
```json
{
  "error": "ModuleNotFoundError: No module named 'pandas'",
  "code": "import pandas as pd"
}
```

### JavaScript Error
```json
{
  "error": "TypeError: Cannot read property 'length' of undefined",
  "code": "const arr = undefined; console.log(arr.length);"
}
```

### React Error
```json
{
  "error": "Warning: Each child in a list should have a unique 'key' prop",
  "code": "items.map(item => <li>{item}</li>)"
}
```

## 🚨 Troubleshooting

### Server Won't Start
- Check if port 8000 is available
- Verify Python 3.11+ is installed
- Ensure all dependencies are installed

### No Results Returned
- Verify Gemini API key is valid
- Check internet connection
- Try with a simpler error message

### Vector Search Not Working
- ChromaDB data is stored locally in `./chroma_data/`
- System falls back to direct search automatically
- Check write permissions for the data directory

## 📈 Performance Tips

1. **API Rate Limits**: Be aware of Gemini rate limits
2. **Vector Database**: Populate for better semantic search
3. **Caching**: Consider implementing response caching
4. **Batch Processing**: For multiple errors, consider batching

## 🔒 Security Notes

- Never commit API keys to version control
- Use environment variables for sensitive data
- Consider API key rotation policies
- Monitor API usage and costs
