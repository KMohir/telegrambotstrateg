import os
import requests

SCRAPECREATORS_API_KEY = os.getenv("SCRAPECREATORS_API_KEY")

async def get_trend_videos(keyword: str):
    """
    Fetch trending Instagram reels based on keyword using ScrapeCreators API
    """
    url = "https://api.scrapecreators.com/v1/instagram/reels/search"
    
    headers = {
        "x-api-key": SCRAPECREATORS_API_KEY
    }
    
    params = {
        "query": keyword,
        "amount": 20  # Get 20 results to sort and filter
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        print(f"API Response: {data}")  # Debug logging
        
        # Parse the response and format it for our bot
        results = []
        
        # Handle different possible response structures
        reels_data = []
        if isinstance(data, dict):
            if 'data' in data:
                reels_data = data['data']
            elif 'reels' in data:
                reels_data = data['reels']
            elif 'items' in data:
                reels_data = data['items']
            elif 'results' in data:
                reels_data = data['results']
        elif isinstance(data, list):
            reels_data = data
        
        for reel in reels_data[:10]:  # Limit to 10 results
            # Extract relevant information with flexible field names
            username = reel.get("username") or reel.get("owner", {}).get("username", "Unknown")
            shortcode = reel.get("code") or reel.get("shortcode") or reel.get("id", "")
            
            result = {
                "username": username,
                "url": reel.get("url") or reel.get("link") or f"https://instagram.com/reel/{shortcode}",
                "views": reel.get("video_view_count") or reel.get("play_count") or reel.get("views") or reel.get("view_count", 0),
                "likes": reel.get("like_count") or reel.get("likes", 0),
                "comments": reel.get("comment_count") or reel.get("comments", 0),
                "caption": reel.get("caption", ""),
                "shortcode": shortcode
            }
            
            # Only add if we have valid data
            if result["url"]:
                results.append(result)
        
        # Sort by views (highest first) and return top 10
        results.sort(key=lambda x: x.get('views', 0), reverse=True)
        return results[:10]
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching trends from ScrapeCreators API: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response body: {e.response.text}")
        return []
    except Exception as e:
        print(f"Error parsing ScrapeCreators API response: {e}")
        import traceback
        traceback.print_exc()
        return []
