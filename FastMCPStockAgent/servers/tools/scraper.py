import requests
from bs4 import BeautifulSoup
import re

def analyze_sentiment_from_news(ticker_symbol: str) -> dict:
    """
    Scrapes Google News for the stock and calculates a basic Sentiment Score.
    Returns: {'score': float (-1 to 1), 'summary': str}
    """
    # Clean ticker for search (Remove .NS)
    search_term = ticker_symbol.replace(".NS", "") + " stock news india"
    url = f"https://www.google.com/search?q={search_term}&tbm=nws&gl=IN"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract Headlines
        headlines = [h.text for h in soup.find_all("div", class_="BNeawe vvjwJb AP7Wnd")[:5]]
        
        if not headlines:
            return {'score': 0, 'summary': "No news found via scraping."}

        # Basic Keyword Sentiment Analysis (Since no OpenAI)
        bullish_words = ['surge', 'jump', 'high', 'profit', 'buy', 'growth', 'gain', 'strong', 'rally']
        bearish_words = ['drop', 'fall', 'loss', 'sell', 'weak', 'crash', 'down', 'low', 'crisis']
        
        score = 0
        found_keywords = []
        
        text_blob = " ".join(headlines).lower()
        
        for word in bullish_words:
            if word in text_blob:
                score += 0.2
                found_keywords.append(word)
        
        for word in bearish_words:
            if word in text_blob:
                score -= 0.2
                found_keywords.append(word)
                
        # Cap score between -0.5 and 0.5 (Conservative adjustment)
        score = max(min(score, 0.5), -0.5)
        
        return {
            'score': score,
            'summary': f"Found news keywords: {', '.join(found_keywords)}",
            'headlines': headlines[:2]
        }

    except Exception as e:
        return {'score': 0, 'summary': f"Scraping failed: {e}"}