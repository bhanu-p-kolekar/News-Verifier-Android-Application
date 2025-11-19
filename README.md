# News Verification AI App - Full Stack Project

## 🎯 Project Overview

A complete, production-ready news verification application powered by AI. The system uses Groq's LLaMA 3.1 model to analyze news content by cross-referencing it with related articles found via SerpAPI.

### Features
✅ AI-powered news verification using Groq (LLaMA 3.1 / Mixtral)  
✅ Related news search via SerpAPI  
✅ Automatic article text extraction  
✅ RESTful API with FastAPI  
✅ Android app with Kotlin + Retrofit  
✅ Real-time verification with confidence scores  
✅ Evidence-based analysis with source links  

## 🏗️ Architecture

```
┌─────────────────┐
│  Android App    │ ← User Interface (Kotlin)
└────────┬────────┘
         │ HTTP/JSON
         ▼
┌─────────────────┐
│  FastAPI        │ ← Backend API (Python)
│  Backend        │
└────────┬────────┘
         │
    ┌────┴─────┬──────────┬─────────┐
    ▼          ▼          ▼         ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│ Groq   │ │SerpAPI │ │News-   │ │Article │
│ AI API │ │        │ │paper3k │ │Extract │
└────────┘ └────────┘ └────────┘ └────────┘
```

## 📦 Tech Stack

### Backend
- **Python 3.8+**
- **FastAPI** - Modern async web framework
- **Groq API** - AI model inference (LLaMA 3.1)
- **SerpAPI** - Google News search
- **Newspaper3k** - Article text extraction
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

### Android Frontend
- **Kotlin**
- **Retrofit** - HTTP client
- **Coroutines** - Async operations
- **ViewModel & LiveData** - MVVM architecture
- **Material Design 3** - UI components
- **Gson** - JSON parsing

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed
2. **Android Studio** (for mobile app)
3. **Groq API Key** - [Get it free](https://console.groq.com)
4. **SerpAPI Key** - [Get it free](https://serpapi.com)

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
copy .env.template .env  # Windows
cp .env.template .env    # Mac/Linux

# Edit .env and add your API keys
# GROQ_API_KEY=your_key_here
# SERPAPI_KEY=your_key_here

# Run the server
python main.py
```

Server will start at: `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

### Android Setup

1. **Open Android Studio**
2. **Create a new project** or open existing
3. **Copy files** from `android/` to your project:
   - `api/*.kt` → `app/src/main/java/com/newsverification/api/`
   - `models/*.kt` → `app/src/main/java/com/newsverification/models/`
   - `viewmodel/*.kt` → `app/src/main/java/com/newsverification/viewmodel/`
   - `ui/*.kt` → `app/src/main/java/com/newsverification/ui/`
   - `ui/*.xml` → `app/src/main/res/layout/`

4. **Update build.gradle** with dependencies from `android/build.gradle`

5. **Update AndroidManifest.xml** with required permissions

6. **Configure backend URL** in `RetrofitClient.kt`:
   ```kotlin
   // For Android Emulator
   private const val BASE_URL = "http://10.0.2.2:8000/"
   
   // For Physical Device (same WiFi)
   private const val BASE_URL = "http://YOUR_COMPUTER_IP:8000/"
   ```

7. **Sync Gradle** and **Run** the app

## 📚 Detailed Documentation

- **Backend Setup**: See `backend/README.md`
- **Android Integration**: See `android/README.md`

## 🔍 How It Works

### Verification Flow

1. **User Input**: User submits news text or article URL
2. **Content Extraction**: If URL, extract article text using Newspaper3k
3. **Related Search**: Find 5-10 related articles via SerpAPI
4. **Article Extraction**: Extract text from each related article
5. **AI Analysis**: Send all content to Groq AI for analysis
6. **Response**: Return verdict, confidence score, summary, and evidence links

### API Endpoint

**POST /verify**

Request:
```json
{
  "content": "News text or article URL"
}
```

Response:
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

## 🧪 Testing

### Test Backend API

```bash
# Health check
curl http://localhost:8000/health

# Verify news (Windows PowerShell)
curl -X POST http://localhost:8000/verify `
  -H "Content-Type: application/json" `
  -d '{"content": "Scientists discover new planet"}'
```

### Test Android App

1. Ensure backend is running
2. Update `BASE_URL` in `RetrofitClient.kt`
3. Run app in emulator or device
4. Enter news text or URL
5. Click "Verify News"
6. View results with verdict, confidence, summary, and sources

## 📁 Project Structure

```
.
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── models.py               # Pydantic models
│   ├── groq_client.py          # Groq AI integration
│   ├── news_search.py          # SerpAPI integration
│   ├── extract.py              # Article extraction
│   ├── requirements.txt        # Python dependencies
│   ├── .env.template           # Environment variables template
│   ├── utils/
│   │   └── helpers.py          # Utility functions
│   └── README.md               # Backend documentation
│
└── android/
    ├── api/
    │   ├── NewsVerificationApi.kt
    │   ├── RetrofitClient.kt
    │   └── NewsVerificationRepository.kt
    ├── models/
    │   └── Models.kt
    ├── viewmodel/
    │   └── NewsVerificationViewModel.kt
    ├── ui/
    │   ├── MainActivity.kt
    │   └── activity_main.xml
    ├── build.gradle
    ├── AndroidManifest.xml
    └── README.md               # Android documentation
```

## 🛠️ Configuration

### Environment Variables

Create `.env` file in `backend/` directory:

```env
GROQ_API_KEY=your_groq_api_key_here
SERPAPI_KEY=your_serpapi_key_here
```

### Backend Configuration

Edit `backend/main.py` for:
- CORS settings
- Host/port configuration
- Logging level

### Android Configuration

Edit `android/api/RetrofitClient.kt` for:
- Backend URL
- Timeout settings
- Logging level

## 🐛 Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Change port in main.py or use:
uvicorn main:app --port 8001
```

**API key errors:**
- Verify `.env` file exists
- Check API keys are valid
- Ensure keys have sufficient credits

### Android Issues

**Cannot connect to backend:**
- Use `10.0.2.2` for emulator (not `localhost`)
- Use computer's IP for physical device
- Ensure both on same WiFi network
- Check firewall settings

**Cleartext traffic error:**
- Add `android:usesCleartextTraffic="true"` to manifest
- Only for development; use HTTPS in production

## 🚢 Deployment

### Backend Deployment

**Option 1: Cloud Platforms**
- Deploy to Heroku, AWS, Google Cloud, or Azure
- Use environment variables for API keys
- Enable HTTPS

**Option 2: Docker**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Android Deployment

1. Update `BASE_URL` to production URL
2. Remove `usesCleartextTraffic` from manifest
3. Enable ProGuard/R8 for release builds
4. Generate signed APK/AAB
5. Publish to Google Play Store

## 📊 API Rate Limits

- **Groq API**: Varies by plan (check console.groq.com)
- **SerpAPI**: 100 searches/month (free tier)

Consider implementing caching to reduce API calls.

## 🔐 Security Best Practices

1. **Never commit API keys** - Use `.env` files
2. **Use HTTPS** in production
3. **Implement rate limiting** on backend
4. **Validate all inputs** - Already implemented with Pydantic
5. **Use authentication** for production apps
6. **Sanitize user inputs** - Prevent injection attacks

## 🎨 Customization

### Backend
- Modify verification prompt in `groq_client.py`
- Adjust number of search results in `news_search.py`
- Add caching with Redis or similar
- Implement user authentication

### Android
- Change color scheme in `activity_main.xml`
- Add dark mode support
- Implement result caching
- Add sharing functionality
- Save verification history

## 📈 Future Enhancements

- [ ] User authentication & accounts
- [ ] Verification history
- [ ] Bookmark trusted sources
- [ ] Real-time notifications
- [ ] Multi-language support
- [ ] Fact-check database integration
- [ ] Browser extension
- [ ] iOS app
- [ ] Desktop application
- [ ] API rate limiting & quotas
- [ ] Advanced analytics dashboard
- [ ] Social media integration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - Free to use in personal and commercial projects.

## 💬 Support

For issues or questions:
1. Check documentation in `backend/README.md` and `android/README.md`
2. Review API docs at `/docs` endpoint
3. Check logs for error messages
4. Verify API keys and configuration

## 🙏 Acknowledgments

- **Groq** - AI inference platform
- **SerpAPI** - Google search API
- **Newspaper3k** - Article extraction
- **FastAPI** - Web framework
- **Retrofit** - Android HTTP client

---

**Built with ❤️ for fighting misinformation**

🌟 **Star this project if you find it useful!**
