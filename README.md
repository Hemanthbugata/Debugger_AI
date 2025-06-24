# Debugger AI - Intelligent Code Error Resolver

An AI-powered debugging assistant that fetches solutions from StackOverflow and Reddit, combines them with Google Gemini's intelligence, and provides comprehensive solutions for programming errors.

## 🚀 Features

- **Multi-Source Intelligence**: Searches StackOverflow and Reddit for relevant solutions
- **AI-Enhanced Solutions**: Combines real-world solutions with Google Gemini's capabilities
- **Fallback Mechanism**: Uses pure Gemini when no relevant sources are found
- **Vector Database Integration**: Semantic search using Pinecone for better matching
- **Comprehensive Error Analysis**: Analyzes error types, programming languages, and libraries
- **RESTful API**: Easy integration with FastAPI backend
- **Feedback System**: Learn from user feedback to improve recommendations

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Error Input   │───▶│   Preprocessor  │───▶│ Search Engines  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Final Solution  │◀───│   RAG Pipeline  │◀───│ Vector Database │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📋 Prerequisites

- Python 3.11+
- Google Gemini API Key (Required)
- Pinecone API Key (Optional - for vector search)
- Reddit API Credentials (Optional - for Reddit search)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Debugger_AI/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.template .env
   # Edit .env file with your API keys
   ```

## ⚙️ Configuration

### Required Configuration
```env
GEMINI_API_KEY=your-gemini-api-key-here
```

### Optional Configuration
```env
# For vector database search
PINECONE_API_KEY=your-pinecone-api-key-here
PINECONE_ENV=us-west1-gcp

# For Reddit search
REDDIT_CLIENT_ID=your-reddit-client-id-here
REDDIT_CLIENT_SECRET=your-reddit-client-secret-here
REDDIT_USER_AGENT=agent-debugger-ai
```

## 🚀 Quick Start

1. **Test the setup**
   ```bash
   python -m app.utils.setup_utils
   ```

2. **Start the server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Test the API**
   ```bash
   curl -X POST "http://localhost:8000/debug/" \
        -H "Content-Type: application/json" \
        -d '{
          "error": "NameError: name '\''pd'\'' is not defined",
          "code": "df = pd.DataFrame({'\''A'\'': [1, 2, 3]})"
        }'
   ```

## 📡 API Endpoints

### Debug Endpoint
**POST** `/debug/`

Submit an error for debugging assistance.

**Request Body:**
```json
{
  "error": "Error message here",
  "code": "Optional code snippet"
}
```

**Response:**
```json
{
  "summary": "Clear explanation of the problem",
  "fix": "Detailed solution with code examples",
  "sources": [
    {
      "title": "Source title",
      "link": "https://stackoverflow.com/..."
    }
  ]
}
```

### Feedback Endpoint
**POST** `/feedback/`

Submit feedback about debugging results.

**Request Body:**
```json
{
  "debug_request": {"error": "...", "code": "..."},
  "response": {"summary": "...", "fix": "..."},
  "rating": 5,
  "comment": "Very helpful!"
}
```

## 🔄 Data Ingestion

To populate the vector database with StackOverflow and Reddit data:

```bash
python -m app.ingestion.data_ingestion
```

This will:
- Search for common programming errors
- Generate embeddings for found content
- Store in Pinecone vector database
- Enable semantic search capabilities

## 🏃‍♂️ How It Works

1. **Error Analysis**: The input preprocessor analyzes the error to extract:
   - Error type (TypeError, SyntaxError, etc.)
   - Programming language
   - Relevant libraries

2. **Multi-Source Search**: 
   - **StackOverflow**: Searches for questions matching the error
   - **Reddit**: Searches programming subreddits for discussions
   - **Vector Database**: Semantic search for similar issues

3. **Solution Generation**:   - Combines found solutions with Google Gemini's knowledge
   - Provides comprehensive fix with code examples
   - Falls back to Gemini-only solution if no sources found

4. **Response Formatting**:
   - Clear problem summary
   - Step-by-step solution
   - Source citations
   - Best practices and prevention tips

## 📊 Example Usage

### Python Import Error
```python
# Input
{
  "error": "ModuleNotFoundError: No module named 'pandas'",
  "code": "import pandas as pd"
}

# Response
{
  "summary": "The error indicates that pandas is not installed in your Python environment.",
  "fix": "Install pandas using pip:\n\npip install pandas\n\nOr if using conda:\nconda install pandas",
  "sources": [...]
}
```

### JavaScript TypeError
```python
# Input
{
  "error": "TypeError: Cannot read property 'length' of undefined",
  "code": "const arr = undefined;\nconsole.log(arr.length);"
}

# Response includes safe checking patterns and debugging tips
```

## 🐳 Docker Support

```bash
# Build the image
docker build -t debugger-ai .

# Run the container
docker run -p 8000:8000 --env-file .env debugger-ai
```

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Run specific test
pytest tests/test_debug.py::test_debug_endpoint
```

## 📝 Development

### Adding New Error Types
1. Update `InputPreprocessor` in `app/core/preprocessor.py`
2. Add patterns for new error types
3. Update search queries in data ingestion

### Extending Search Sources
1. Create new retriever in `app/ingestion/`
2. Implement search and fetch methods
3. Update debug endpoint to include new source

### Improving AI Responses
1. Update prompts in `RAGPipeline`
2. Adjust temperature and max_tokens
3. Test with various error types

## 🚨 Troubleshooting

### Common Issues

1. **Gemini API Errors**
   - Check API key validity
   - Verify sufficient credits
   - Check rate limits

2. **Pinecone Connection Issues**
   - Verify API key and environment
   - Check index creation permissions
   - Ensure correct dimension settings

3. **Reddit API Issues**
   - Verify app credentials
   - Check user agent string
   - Ensure read permissions

4. **No Results Found**
   - The system will fallback to Gemini-only solutions
   - Consider running data ingestion to populate vector DB
   - Check search query preprocessing

### Debug Mode
Set `DEBUG=true` in `.env` for verbose logging.

## 🔮 Future Enhancements

- [ ] GitHub Issues integration
- [ ] Multiple programming language support expansion
- [ ] Real-time error monitoring integration
- [ ] Machine learning model for error classification
- [ ] Web interface for easier interaction
- [ ] Slack/Discord bot integration
- [ ] IDE plugins (VSCode, PyCharm)

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📞 Support

For support, email your-email@example.com or create an issue in the repository.
