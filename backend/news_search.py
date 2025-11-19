"""
News Search Module using SerpAPI
Searches for related news articles to verify claims
"""

import os
import logging
from typing import List, Dict, Any
from serpapi import GoogleSearch
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class NewsSearcher:
    """
    Search for related news articles using SerpAPI
    """
    
    def __init__(self):
        """
        Initialize SerpAPI client with API key from environment
        """
        self.api_key = os.getenv("SERPAPI_KEY")
        if not self.api_key:
            raise ValueError("SERPAPI_KEY not found in environment variables")
        
        logger.info("NewsSearcher initialized successfully")
    
    async def search_related_news(
        self,
        query: str,
        num_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search for news articles related to the query
        
        Args:
            query: Search query (content to find related articles for)
            num_results: Number of results to return (default: 10)
        
        Returns:
            List of article dictionaries with title, url, source, snippet
        """
        try:
            logger.info(f"Searching for news related to: {query[:100]}...")
            
            # Prepare search query - extract key terms
            search_query = self._prepare_search_query(query)
            
            # Configure SerpAPI search
            search_params = {
                "q": search_query,
                "tbm": "nws",  # News search
                "api_key": self.api_key,
                "num": min(num_results, 10),  # SerpAPI usually returns up to 10
                "gl": "us",  # Country
                "hl": "en"   # Language
            }
            
            # Execute search
            search = GoogleSearch(search_params)
            results = search.get_dict()
            
            # Extract news results
            articles = []
            
            # Check for news results
            if "news_results" in results:
                for item in results["news_results"][:num_results]:
                    article = {
                        "title": item.get("title", ""),
                        "url": item.get("link", ""),
                        "source": item.get("source", ""),
                        "snippet": item.get("snippet", ""),
                        "published_date": item.get("date", "")
                    }
                    articles.append(article)
            
            # Also check organic results if not enough news results
            if len(articles) < num_results and "organic_results" in results:
                for item in results["organic_results"][:num_results - len(articles)]:
                    article = {
                        "title": item.get("title", ""),
                        "url": item.get("link", ""),
                        "source": item.get("displayed_link", ""),
                        "snippet": item.get("snippet", ""),
                        "published_date": ""
                    }
                    articles.append(article)
            
            logger.info(f"Found {len(articles)} related articles")
            return articles
        
        except Exception as e:
            logger.error(f"News search failed: {str(e)}", exc_info=True)
            return []
    
    def _prepare_search_query(self, content: str) -> str:
        """
        Prepare search query from content
        Extracts key terms and creates an effective search query
        
        Args:
            content: Original content text
        
        Returns:
            Optimized search query string
        """
        # Take first 200 characters and clean up
        query = content[:200].strip()
        
        # Remove URLs from query
        words = []
        for word in query.split():
            if not word.startswith(('http://', 'https://', 'www.')):
                words.append(word)
        
        query = ' '.join(words)
        
        # Limit to reasonable length
        if len(query) > 150:
            query = query[:150].rsplit(' ', 1)[0]
        
        logger.debug(f"Prepared search query: {query}")
        return query
    
    async def search_by_url(self, url: str, num_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search for articles related to a specific URL
        
        Args:
            url: URL to find related articles for
            num_results: Number of results to return
        
        Returns:
            List of related articles
        """
        try:
            # Extract domain for search
            from urllib.parse import urlparse
            domain = urlparse(url).netloc
            
            search_params = {
                "q": f"site:{domain} OR related:{url}",
                "tbm": "nws",
                "api_key": self.api_key,
                "num": num_results,
                "gl": "us",
                "hl": "en"
            }
            
            search = GoogleSearch(search_params)
            results = search.get_dict()
            
            articles = []
            if "news_results" in results:
                for item in results["news_results"]:
                    article = {
                        "title": item.get("title", ""),
                        "url": item.get("link", ""),
                        "source": item.get("source", ""),
                        "snippet": item.get("snippet", ""),
                        "published_date": item.get("date", "")
                    }
                    articles.append(article)
            
            return articles
        
        except Exception as e:
            logger.error(f"URL-based search failed: {str(e)}")
            return []
