"""
Groq API Client for AI-powered news verification
Uses LLaMA 3.1 or Mixtral for content analysis
"""

import os
import json
import logging
from typing import Dict, List, Any
from groq import AsyncGroq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class GroqClient:
    """
    Client for interacting with Groq API for news verification
    """
    
    def __init__(self):
        """
        Initialize Groq client with API key from environment
        """
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.client = AsyncGroq(api_key=self.api_key)
        
        # Model selection - use current supported models
        self.models = [
            "llama-3.3-70b-versatile",  # Latest LLaMA 3.3
            "llama-3.1-8b-instant",
            "mixtral-8x7b-32768"
        ]
        self.current_model = self.models[0]
        
        logger.info(f"Groq client initialized with model: {self.current_model}")
    
    def _create_verification_prompt(
        self,
        main_content: str,
        related_articles: List[Dict[str, str]],
        is_url: bool = False
    ) -> str:
        """
        Create a detailed prompt for news verification
        
        Args:
            main_content: Main news content to verify
            related_articles: List of related article data
            is_url: Whether the content came from a URL
        
        Returns:
            Formatted prompt string
        """
        
        # Extract headline if present
        headline = ""
        content_body = main_content
        if main_content.startswith("HEADLINE:"):
            lines = main_content.split('\n', 2)
            headline = lines[0].replace("HEADLINE:", "").strip()
            content_body = lines[2] if len(lines) > 2 else lines[1] if len(lines) > 1 else ""
        
        prompt = f"""You are an expert fact-checker and news analyst. Your task is to verify news content by analyzing it against credible sources.

{'=' * 80}
ARTICLE TO VERIFY:
{'=' * 80}"""

        if headline:
            prompt += f"""
HEADLINE: {headline}
"""
        
        prompt += f"""
CONTENT:
{content_body[:2500]}

{'=' * 80}
RELATED NEWS SOURCES FOR VERIFICATION:
{'=' * 80}
"""
        
        for idx, article in enumerate(related_articles[:5], 1):
            prompt += f"""
━━━ Source {idx} ━━━
Title: {article.get('title', 'Untitled')}
Publisher: {article.get('source', 'Unknown')}
URL: {article.get('url', 'N/A')}
Content Preview: {article.get('text', '')[:500]}
━━━━━━━━━━━━━━━━━━━
"""
        
        prompt += f"""

{'=' * 80}
VERIFICATION TASK:
{'=' * 80}

1. ANALYZE THE HEADLINE (if present):
   - Is it sensationalized or clickbait?
   - Does it accurately represent the content?
   - Is it making extraordinary claims?

2. VERIFY THE CONTENT:
   - Cross-reference with the related sources above
   - Check if key facts match credible sources
   - Identify any contradictions or inconsistencies
   - Look for evidence of manipulation or misinformation

3. DETERMINE VERDICT:
   - **True**: Verified by multiple credible sources, facts are accurate
   - **False**: Contradicted by credible sources, contains false information
   - **Misleading**: Partially true but missing critical context or exaggerated
   - **Unverified**: Insufficient credible sources to confirm or deny

4. PROVIDE:
   - A verdict (EXACTLY one of: True, False, Misleading, Unverified)
   - A confidence score (0-100) based on source quality and consistency
   - A clear, detailed summary explaining:
     * What the article claims
     * What you found in credible sources
     * Why you reached this verdict
     * Any important context or caveats

{'=' * 80}
RESPOND ONLY WITH VALID JSON - NO OTHER TEXT:
{'=' * 80}

{{
    "verdict": "True|False|Misleading|Unverified",
    "confidence": 0-100,
    "summary": "Detailed explanation of your analysis, including what the headline/content claims and what you found in credible sources"
}}

CRITICAL: Output ONLY the JSON object above. No markdown, no code blocks, no additional text."""
        
        return prompt
    
    async def verify_news(
        self,
        main_content: str,
        related_articles: List[Dict[str, str]],
        is_url: bool = False
    ) -> Dict[str, Any]:
        """
        Verify news content using Groq AI
        
        Args:
            main_content: Main content to verify
            related_articles: Related articles for context
            is_url: Whether the content came from a URL
        
        Returns:
            Dictionary with verdict, confidence, summary, and evidence_links
        """
        try:
            # Create verification prompt
            prompt = self._create_verification_prompt(main_content, related_articles, is_url)
            
            logger.info(f"Sending verification request to Groq ({self.current_model})...")
            
            # Call Groq API
            chat_completion = await self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional fact-checker and news analyst. Analyze news content critically and verify against credible sources. Always respond with valid JSON only."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.current_model,
                temperature=0.2,  # Lower temperature for more consistent, factual output
                max_tokens=1500,
                top_p=0.9
            )
            
            # Extract response
            response_text = chat_completion.choices[0].message.content.strip()
            logger.info(f"Received response from Groq: {len(response_text)} characters")
            
            # Parse JSON response
            try:
                # Try to extract JSON if wrapped in markdown code blocks
                if "```json" in response_text:
                    response_text = response_text.split("```json")[1].split("```")[0].strip()
                elif "```" in response_text:
                    response_text = response_text.split("```")[1].split("```")[0].strip()
                
                result = json.loads(response_text)
                
                # Validate required fields
                required_fields = ["verdict", "confidence", "summary"]
                for field in required_fields:
                    if field not in result:
                        raise ValueError(f"Missing required field: {field}")
                
                # Ensure confidence is an integer
                result["confidence"] = int(result["confidence"])
                
                # Ensure confidence is within bounds
                result["confidence"] = max(0, min(100, result["confidence"]))
                
                # Initialize evidence_links (will be added by main.py)
                if "evidence_links" not in result:
                    result["evidence_links"] = []
                
                logger.info(f"Successfully parsed verification result: {result['verdict']}")
                return result
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {str(e)}")
                logger.error(f"Response text: {response_text}")
                
                # Return a fallback response
                return {
                    "verdict": "Unverified",
                    "confidence": 0,
                    "summary": "Unable to verify: AI response parsing failed",
                    "evidence_links": []
                }
        
        except Exception as e:
            logger.error(f"Groq API call failed: {str(e)}", exc_info=True)
            
            # Return error response
            return {
                "verdict": "Unverified",
                "confidence": 0,
                "summary": f"Verification failed due to technical error: {str(e)}",
                "evidence_links": []
            }
    
    async def test_connection(self) -> bool:
        """
        Test Groq API connection
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            chat_completion = await self.client.chat.completions.create(
                messages=[{"role": "user", "content": "Hello"}],
                model=self.current_model,
                max_tokens=10
            )
            logger.info("Groq API connection test successful")
            return True
        except Exception as e:
            logger.error(f"Groq API connection test failed: {str(e)}")
            return False
