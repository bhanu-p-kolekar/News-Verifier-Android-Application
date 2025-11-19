"""
Article Text Extraction Module
Uses Newspaper3k to extract clean text from article URLs
"""

import logging
from typing import Optional, List, Dict
from newspaper import Article
import asyncio
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)


class ArticleExtractor:
    """
    Extract article text from URLs using Newspaper3k
    """
    
    def __init__(self):
        """
        Initialize article extractor with thread pool for async operations
        """
        self.executor = ThreadPoolExecutor(max_workers=5)
        logger.info("ArticleExtractor initialized successfully")
    
    async def extract_from_url(self, url: str) -> Optional[str]:
        """
        Extract article text from URL asynchronously
        
        Args:
            url: Article URL to extract text from
        
        Returns:
            Extracted article text or None if extraction fails
        """
        try:
            logger.info(f"Extracting article from: {url}")
            
            # Run newspaper3k in thread pool (it's synchronous)
            loop = asyncio.get_event_loop()
            article_data = await loop.run_in_executor(
                self.executor,
                self._extract_sync,
                url
            )
            
            if article_data:
                logger.info(f"Successfully extracted {len(article_data)} characters from {url}")
                return article_data
            else:
                logger.warning(f"No text extracted from {url}")
                return None
        
        except Exception as e:
            logger.error(f"Failed to extract article from {url}: {str(e)}")
            return None
    
    async def extract_with_metadata(self, url: str) -> Optional[Dict[str, str]]:
        """
        Extract article with full metadata including headline, author, date
        
        Args:
            url: Article URL to extract from
        
        Returns:
            Dictionary with title, text, authors, publish_date, or None
        """
        try:
            logger.info(f"Extracting article with metadata from: {url}")
            
            loop = asyncio.get_event_loop()
            metadata = await loop.run_in_executor(
                self.executor,
                self._extract_metadata_sync,
                url
            )
            
            if metadata:
                logger.info(f"Successfully extracted article: '{metadata.get('title', 'No title')}'")
                return metadata
            else:
                logger.warning(f"No metadata extracted from {url}")
                return None
        
        except Exception as e:
            logger.error(f"Failed to extract metadata from {url}: {str(e)}")
            return None
    
    def _extract_sync(self, url: str) -> Optional[str]:
        """
        Synchronous article extraction (runs in thread pool)
        
        Args:
            url: Article URL
        
        Returns:
            Extracted text with headline or None
        """
        try:
            # Create article object
            article = Article(url)
            
            # Download and parse
            article.download()
            article.parse()
            
            # Get text
            text = article.text
            
            # Include headline at the top
            if article.title:
                text = f"HEADLINE: {article.title}\n\n{text}"
            
            return text.strip() if text else None
        
        except Exception as e:
            logger.error(f"Sync extraction failed for {url}: {str(e)}")
            return None
    
    def _extract_metadata_sync(self, url: str) -> Optional[Dict[str, str]]:
        """
        Synchronous article extraction with full metadata
        
        Args:
            url: Article URL
        
        Returns:
            Dictionary with article metadata or None
        """
        try:
            # Create article object
            article = Article(url)
            
            # Download and parse
            article.download()
            article.parse()
            
            # Extract all metadata
            metadata = {
                'url': url,
                'title': article.title or 'No title',
                'text': article.text or '',
                'authors': ', '.join(article.authors) if article.authors else 'Unknown',
                'publish_date': str(article.publish_date) if article.publish_date else 'Unknown',
                'top_image': article.top_image or '',
                'summary': article.summary if hasattr(article, 'summary') else ''
            }
            
            return metadata if metadata['text'] else None
        
        except Exception as e:
            logger.error(f"Metadata extraction failed for {url}: {str(e)}")
            return None
    
    async def extract_multiple(self, urls: List[str]) -> Dict[str, Optional[str]]:
        """
        Extract text from multiple URLs concurrently
        
        Args:
            urls: List of URLs to extract from
        
        Returns:
            Dictionary mapping URLs to extracted text
        """
        try:
            logger.info(f"Extracting text from {len(urls)} URLs...")
            
            # Create tasks for all URLs
            tasks = [self.extract_from_url(url) for url in urls]
            
            # Run concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Map results back to URLs
            url_to_text = {}
            for url, result in zip(urls, results):
                if isinstance(result, Exception):
                    logger.error(f"Exception extracting {url}: {str(result)}")
                    url_to_text[url] = None
                else:
                    url_to_text[url] = result
            
            successful = sum(1 for v in url_to_text.values() if v is not None)
            logger.info(f"Successfully extracted {successful}/{len(urls)} articles")
            
            return url_to_text
        
        except Exception as e:
            logger.error(f"Batch extraction failed: {str(e)}")
            return {url: None for url in urls}
    
    def __del__(self):
        """
        Cleanup thread pool on deletion
        """
        if hasattr(self, 'executor'):
            self.executor.shutdown(wait=False)
