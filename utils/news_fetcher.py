import feedparser
import requests
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_news(rss_url):
    """
    Fetch news from RSS feed
    
    Args:
        rss_url (str): URL of the RSS feed
        
    Returns:
        list: List of dictionaries containing news items
    """
    try:
        # Parse the RSS feed
        feed = feedparser.parse(rss_url)
        
        # Check if feed parsed successfully
        if feed.get('bozo_exception'):
            logger.error(f"Error parsing feed: {feed.bozo_exception}")
            return []
        
        # Extract and process entries
        news_items = []
        for entry in feed.entries:
            # Extract required fields
            item = {
                'title': entry.get('title', 'No title'),
                'link': entry.get('link', '#'),
                'description': clean_html(entry.get('description', entry.get('summary', 'No description'))),
                'published': entry.get('published', 'No date')
            }
            
            # Try to fetch full content if description is too short
            if len(item['description']) < 100 and 'link' in item:
                try:
                    item['description'] = fetch_article_content(item['link'])
                except Exception as e:
                    logger.warning(f"Failed to fetch full content: {e}")
            
            news_items.append(item)
        
        return news_items
    
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        return []

def clean_html(html_text):
    """
    Remove HTML tags from text
    
    Args:
        html_text (str): HTML text
        
    Returns:
        str: Clean text
    """
    try:
        soup = BeautifulSoup(html_text, 'html.parser')
        return soup.get_text(separator=' ', strip=True)
    except Exception as e:
        logger.error(f"Error cleaning HTML: {e}")
        return html_text

def fetch_article_content(url, max_length=1000):
    """
    Fetch article content from URL
    
    Args:
        url (str): URL of the article
        max_length (int): Maximum length of content to return
        
    Returns:
        str: Article content
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try to find the main content
        # This is a simple approach and might need adjustment for specific sites
        content = ''
        
        # Look for article tags
        article = soup.find('article')
        if article:
            content = article.get_text(separator=' ', strip=True)
        
        # If no article tag, look for main tag
        if not content:
            main = soup.find('main')
            if main:
                content = main.get_text(separator=' ', strip=True)
        
        # If still no content, look for div with common content class names
        if not content:
            for div in soup.find_all('div', class_=['content', 'article-content', 'story-content', 'entry-content']):
                content = div.get_text(separator=' ', strip=True)
                if content:
                    break
        
        # If still no content, use body
        if not content:
            content = soup.body.get_text(separator=' ', strip=True)
        
        # Limit content length
        return content[:max_length]
    
    except Exception as e:
        logger.error(f"Error fetching article content: {e}")
        return "Content not available" 