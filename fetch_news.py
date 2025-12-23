import feedparser
import json
import time
from datetime import datetime

RSS_URLS = [
    "https://www.ajakoartha.com/feed", "https://nagariknews.nagariknetwork.com/feed",
    "https://farakdhar.com/feed/", "https://nepalnews.com/feed/",
    "https://www.ratopati.com/feed", "https://www.corporatenepal.com/rss",
    "https://www.nepalviews.com/feed", "https://kendrabindu.com/feed/",
    "https://neplays.com/feed", "https://ukeraa.com/rss/",
    "https://ujyaaloonline.com/rss/", "https://aarthiknews.com/rss/",
    "https://www.kathmandupati.com/feed/", "https://gorkhapatraonline.com/rss",
    "https://lokaantar.com/rss/", "https://www.setopati.com/feed",
    "https://annapurnapost.com/rss/", "https://www.nepalpress.com/feed/",
    "https://arthasarokar.com/feed", "https://www.sutranews.com/feed/"
]

def get_image(entry):
    """Detects images in various common RSS formats."""
    # 1. Check Media Content
    if 'media_content' in entry:
        return entry.media_content[0]['url']
    # 2. Check Enclosures
    if 'links' in entry:
        for link in entry.links:
            if 'image' in link.get('type', ''):
                return link.get('href', '')
    # 3. Check for thumbnail
    if 'media_thumbnail' in entry:
        return entry.media_thumbnail[0]['url']
    return ""

def fetch_and_sort():
    all_entries = []
    # Use a custom user agent to avoid being blocked by news servers
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    for url in RSS_URLS:
        print(f"Fetching: {url}")
        try:
            # Parse feed with the custom agent
            feed = feedparser.parse(url, agent=headers['User-Agent'])
            source_name = feed.feed.get('title', url.split('/')[2]) # Use domain if title is missing
            
            for entry in feed.entries:
                # Get the best possible date
                pub_date_parsed = entry.get('published_parsed', entry.get('updated_parsed', None))
                
                all_entries.append({
                    "title": entry.get('title', 'No Title'),
                    "link": entry.get('link', '#'),
                    "description": entry.get('summary', entry.get('description', '')),
                    "pubDate": entry.get('published', entry.get('updated', 'Recently')),
                    "source": source_name,
                    "image": get_image(entry),
                    "timestamp": time.mktime(pub_date_parsed) if pub_date_parsed else 0
                })
        except Exception as e:
            print(f"Skipping {url} due to error: {e}")

    # SORT: Newest items first based on timestamp
    all_entries.sort(key=lambda x: x['timestamp'], reverse=True)

    # Remove internal timestamp before saving to JSON
    for e in all_entries:
        e.pop('timestamp',
