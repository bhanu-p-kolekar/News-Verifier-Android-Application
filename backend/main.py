"""
News Verification API - Main FastAPI Application
Provides endpoint for verifying news content using AI and web search
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from models import VerifyRequest, VerifyResponse, HealthResponse
from groq_client import GroqClient
from news_search import NewsSearcher
from extract import ArticleExtractor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global instances
groq_client = None
news_searcher = None
article_extractor = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager - initialize services on startup
    """
    global groq_client, news_searcher, article_extractor
    
    logger.info("Initializing News Verification API...")
    
    try:
        # Initialize services
        groq_client = GroqClient()
        news_searcher = NewsSearcher()
        article_extractor = ArticleExtractor()
        
        logger.info("All services initialized successfully")
        yield
        
    except Exception as e:
        logger.error(f"Failed to initialize services: {str(e)}")
        raise
    finally:
        logger.info("Shutting down News Verification API...")


# Create FastAPI application
app = FastAPI(
    title="News Verification API",
    description="AI-powered news verification using Groq and web search",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=HealthResponse)
async def root():
    """
    Health check endpoint
    """
    return HealthResponse(
        status="healthy",
        message="News Verification API is running"
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Detailed health check endpoint
    """
    try:
        # Verify all services are initialized
        if not all([groq_client, news_searcher, article_extractor]):
            raise HTTPException(
                status_code=503,
                detail="Services not fully initialized"
            )
        
        return HealthResponse(
            status="healthy",
            message="All services operational"
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail=str(e))


@app.post("/verify", response_model=VerifyResponse)
async def verify_news(request: VerifyRequest):
    """
    Main endpoint to verify news content
    
    Process:
    1. Extract article text if URL is provided
    2. Search for related news articles
    3. Extract text from related articles
    4. Analyze all content using Groq AI
    5. Return verification results
    
    Args:
        request: VerifyRequest containing content (text or URL)
    
    Returns:
        VerifyResponse with verdict, confidence, summary, and evidence links
    """
    try:
        logger.info(f"Starting verification for content: {request.content[:100]}...")
        
        # Step 1: Extract main content if URL
        main_content = request.content
        is_url = request.content.startswith(('http://', 'https://'))
        extraction_failed = False
        
        if is_url:
            logger.info(f"Detected URL, extracting article with headline...")
            try:
                extracted = await article_extractor.extract_from_url(request.content)
                if extracted and len(extracted) > 50:  # Ensure meaningful content
                    main_content = extracted
                    logger.info(f"Successfully extracted {len(main_content)} characters")
                else:
                    logger.warning("Extraction returned insufficient content, will search based on URL")
                    extraction_failed = True
                    # Use URL domain and path as search query
                    from urllib.parse import urlparse
                    parsed = urlparse(request.content)
                    main_content = f"News article from {parsed.netloc} - {parsed.path.replace('/', ' ')}"
            except Exception as e:
                logger.warning(f"Failed to extract article: {str(e)}")
                extraction_failed = True
                # Use URL as search query
                from urllib.parse import urlparse
                parsed = urlparse(request.content)
                main_content = f"News from {parsed.netloc}"
        
        # Step 2: Search for related news articles
        logger.info("Searching for related news articles...")
        try:
            # Create better search query
            search_query = main_content[:500] if not extraction_failed else request.content
            
            related_articles = await news_searcher.search_related_news(
                query=search_query,
                num_results=10
            )
            logger.info(f"Found {len(related_articles)} related articles")
            
            # If extraction failed but we found articles, try to use the original URL in verification
            if extraction_failed and is_url:
                logger.info(f"Adding original URL to related articles for context")
                
        except Exception as e:
            logger.error(f"News search failed: {str(e)}")
            related_articles = []
            
            # If both extraction and search failed, return helpful error
            if extraction_failed and is_url:
                return VerifyResponse(
                    verdict="Unverified",
                    confidence=0,
                    summary=f"Unable to extract content from the URL and search for related articles failed. Please try: 1) Check if the URL is accessible, 2) Try copying the article text directly, or 3) Verify your SerpAPI key is valid. Error: {str(e)}",
                    evidence_links=[request.content]
                )
        
        # Step 3: Extract text from related articles
        logger.info("Extracting text from related articles...")
        related_contents = []
        evidence_links = []
        
        for article in related_articles:
            try:
                article_text = await article_extractor.extract_from_url(article['url'])
                if article_text:
                    related_contents.append({
                        'title': article.get('title', 'Untitled'),
                        'source': article.get('source', 'Unknown'),
                        'url': article['url'],
                        'text': article_text[:1000]  # Limit to first 1000 chars
                    })
                    evidence_links.append(article['url'])
            except Exception as e:
                logger.warning(f"Failed to extract from {article['url']}: {str(e)}")
                continue
        
        logger.info(f"Successfully extracted text from {len(related_contents)} articles")
        
        # Step 4: Analyze using Groq AI
        logger.info("Analyzing content with Groq AI...")
        try:
            analysis = await groq_client.verify_news(
                main_content=main_content,
                related_articles=related_contents,
                is_url=is_url
            )
            
            # Add evidence links to the response
            analysis['evidence_links'] = evidence_links[:5]  # Limit to top 5
            
            logger.info(f"Analysis complete. Verdict: {analysis['verdict']}")
            
            return VerifyResponse(**analysis)
            
        except Exception as e:
            logger.error(f"Groq AI analysis failed: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"AI analysis failed: {str(e)}"
            )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Verification failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Verification process failed: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
