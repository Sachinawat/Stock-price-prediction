# import requests
# from bs4 import BeautifulSoup
# import re

# def analyze_sentiment_from_news(ticker_symbol: str) -> dict:
#     """
#     Scrapes Google News for the stock and calculates a basic Sentiment Score.
#     Returns: {'score': float (-1 to 1), 'summary': str}
#     """
#     # Clean ticker for search (Remove .NS)
#     search_term = ticker_symbol.replace(".NS", "") + " stock news india"
#     url = f"https://www.google.com/search?q={search_term}&tbm=nws&gl=IN"
    
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
#     }
    
#     try:
#         response = requests.get(url, headers=headers)
#         soup = BeautifulSoup(response.text, 'html.parser')
        
#         # Extract Headlines
#         headlines = [h.text for h in soup.find_all("div", class_="BNeawe vvjwJb AP7Wnd")[:5]]
        
#         if not headlines:
#             return {'score': 0, 'summary': "No news found via scraping."}

#         # Basic Keyword Sentiment Analysis (Since no OpenAI)
#         bullish_words = ['surge', 'jump', 'high', 'profit', 'buy', 'growth', 'gain', 'strong', 'rally']
#         bearish_words = ['drop', 'fall', 'loss', 'sell', 'weak', 'crash', 'down', 'low', 'crisis']
        
#         score = 0
#         found_keywords = []
        
#         text_blob = " ".join(headlines).lower()
        
#         for word in bullish_words:
#             if word in text_blob:
#                 score += 0.2
#                 found_keywords.append(word)
        
#         for word in bearish_words:
#             if word in text_blob:
#                 score -= 0.2
#                 found_keywords.append(word)
                
#         # Cap score between -0.5 and 0.5 (Conservative adjustment)
#         score = max(min(score, 0.5), -0.5)
        
#         return {
#             'score': score,
#             'summary': f"Found news keywords: {', '.join(found_keywords)}",
#             'headlines': headlines[:2]
#         }

#     except Exception as e:
#         return {'score': 0, 'summary': f"Scraping failed: {e}"}












import requests
from bs4 import BeautifulSoup

def analyze_sentiment_from_news(ticker_symbol: str) -> dict:
    """
    Fetches news from Google News RSS Feed (More stable than HTML scraping).
    Analyzes headlines for Bullish/Bearish sentiment.
    """
    # 1. Clean Ticker (Remove .NS for search query)
    clean_ticker = ticker_symbol.replace(".NS", "").replace(".BO", "")
    query = f"{clean_ticker} stock news"
    
    # 2. Use Google News RSS Feed (Stable XML)
    url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"
    
    try:
        response = requests.get(url, timeout=5)
        # XML Parsing
        soup = BeautifulSoup(response.content, features="xml")
        
        # Get top 10 headlines
        items = soup.findAll('item')
        headlines = [item.title.text for item in items[:10]]
        
        if not headlines:
            return {'score': 0, 'summary': "No headlines found via RSS."}

        # 3. Expanded Keyword Dictionary
        bullish_words = [
            'surge', 'jump', 'gain', 'high', 'record', 'profit', 'buy', 
            'strong', 'growth', 'rally', 'soar', 'beat', 'bull', 'upgrade',
            'positive', 'launch', 'partner', 'dividend', 'expansion'
        ]
        bearish_words = [
            'drop', 'fall', 'loss', 'miss', 'sell', 'weak', 'crash', 
            'down', 'low', 'crisis', 'bear', 'downgrade', 'negative', 
            'lawsuit', 'cut', 'debt', 'risk', 'inflation', 'war'
        ]
        
        score = 0
        found_keywords = []
        text_blob = " ".join(headlines).lower()
        
        # 4. Calculate Score
        for word in bullish_words:
            if word in text_blob:
                score += 0.05 # Add 5% sentiment per positive word
                found_keywords.append(f"+{word}")
        
        for word in bearish_words:
            if word in text_blob:
                score -= 0.05 # Subtract 5% sentiment per negative word
                found_keywords.append(f"-{word}")
                
        # Cap the score so it doesn't go crazy (Max +/- 30% impact)
        score = max(min(score, 0.3), -0.3)
        
        # 5. Create Summary
        if not found_keywords:
            summary_text = "Neutral News (No strong keywords found)."
        else:
            summary_text = f"Keywords: {', '.join(found_keywords[:5])}"

        return {
            'score': score,
            'summary': summary_text,
            'headlines': headlines[:3] # Return top 3 for display
        }

    except Exception as e:
        print(f"Scraper Error: {e}")
        return {'score': 0, 'summary': "Scraping connection failed."}