# News Verification API - Backend

Production-ready FastAPI backend for AI-powered news verification using Groq and SerpAPI.

## Features

- ✅ News content verification using Groq AI (LLaMA 3.1 / Mixtral)
- ✅ Related news search via SerpAPI
- ✅ Article text extraction with Newspaper3k
- ✅ Async endpoints for performance
- ✅ CORS enabled for mobile/web apps
- ✅ Comprehensive error handling
- ✅ Request/response validation with Pydantic

## Prerequisites

- Python 3.8 or higher
- Groq API key ([Get it here](https://console.groq.com))
- SerpAPI key ([Get it here](https://serpapi.com))

## Installation

### 1. Clone or navigate to the backend directory

```bash
cd backend
```

### 2. Create a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the `.env.template` file to `.env`:

```bash
# Windows
copy .env.template .env

# Linux/Mac
cp .env.template .env
```

Edit `.env` and add your API keys:

```env
GROQ_API_KEY=your_groq_api_key_here
SERPAPI_KEY=your_serpapi_key_here
```

## Running the Server

### Development mode (with auto-reload)

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at:
- **Local**: http://localhost:8000
- **Network**: http://YOUR_IP:8000

## API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### 1. Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "message": "All services operational"
}
```

### 2. Verify News

```http
POST /verify
Content-Type: application/json

{
  "content": "News text or article URL here"
}
```

**Response:**
```json
{
  "verdict": "True|False|Misleading|Unverified",
  "confidence": 85,
  "summary": "Analysis summary explaining the verdict...",
  "evidence_links": [
    "https://source1.com/article",
    "https://source2.com/article"
  ]
}
```

## Testing the API

### Using curl (Windows PowerShell)

```powershell
# Health check
curl http://localhost:8000/health

# Verify news with text content
curl -X POST http://localhost:8000/verify `
  -H "Content-Type: application/json" `
  -d '{"content": "Breaking news: Scientists discover new planet"}'

# Verify news with URL
curl -X POST http://localhost:8000/verify `
  -H "Content-Type: application/json" `
  -d '{"content": "https://example.com/news-article"}'
```

### Using Python

```python
import requests

url = "http://localhost:8000/verify"
data = {
    "content": "Your news content or URL here"
}

response = requests.post(url, json=data)
print(response.json())
```

## Project Structure

```
backend/
├── main.py              # FastAPI application entry point
├── models.py            # Pydantic models for validation
├── groq_client.py       # Groq AI integration
├── news_search.py       # SerpAPI news search
├── extract.py           # Article text extraction
├── requirements.txt     # Python dependencies
├── .env.template        # Environment variables template
├── .env                 # Your API keys (git-ignored)
└── utils/
    ├── __init__.py
    └── helpers.py       # Utility functions
```

## How It Works

1. **Input**: User submits news content (text or URL)
2. **Extraction**: If URL, extract article text using Newspaper3k
3. **Search**: Find 5-10 related articles using SerpAPI
4. **Extract Related**: Get text from related articles
5. **Analysis**: Send all content to Groq AI for verification
6. **Response**: Return verdict, confidence, summary, and evidence links

## Troubleshooting

### ModuleNotFoundError

Make sure virtual environment is activated and all dependencies are installed:

```bash
pip install -r requirements.txt
```

### API Key Errors

Verify your `.env` file has valid API keys:

```bash
# View your .env file (Windows)
type .env
```

### Port Already in Use

Change the port in `main.py` or when running uvicorn:

```bash
uvicorn main:app --port 8001
```

### CORS Issues

If connecting from a mobile app or web frontend, CORS is already enabled for all origins. For production, modify the `allow_origins` in `main.py` to specify exact domains.

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Groq API key for AI analysis | Yes |
| `SERPAPI_KEY` | SerpAPI key for news search | Yes |

## Dependencies

- **FastAPI**: Modern web framework
- **Uvicorn**: ASGI server
- **Groq**: AI model API client
- **SerpAPI**: Google search API
- **Newspaper3k**: Article extraction
- **Pydantic**: Data validation
- **python-dotenv**: Environment variable management

## License

MIT License - Feel free to use in your projects!

## Support

For issues or questions:
1. Check the API documentation at `/docs`
2. Review the logs for error messages
3. Verify API keys are valid and have sufficient credits
