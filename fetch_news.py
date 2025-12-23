import feedparser
import json
from datetime import datetime

# List of your RSS feeds
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

def fetch_and_sort():
    all_entries = []
    
    for url in RSS_URLS:
        try:
            feed = feedparser.parse(url)
            source_name = feed.feed.get('title', 'Unknown Source')
            
            for entry in feed.entries:
                # Standardizing data format
                all_entries.append({
                    "title": entry.get('title', ''),
                    "link": entry.get('link', ''),
                    "description": entry.get('summary', entry.get('description', '')),
                    "pubDate": entry.get('published', entry.get('updated', '')),
                    "source": source_name,
                    # Sortable timestamp
                    "timestamp": entry.get('published_parsed', entry.get('updated_parsed', None))
                })
        except Exception as e:
            print(f"Error fetching {url}: {e}")

    # Sort by timestamp (newest first)
    # entry.timestamp is a time.struct_time; we convert to list/tuple for comparison
    all_entries.sort(key=lambda x: x['timestamp'] if x['timestamp'] else (0,), reverse=True)

    # Clean up entry before saving (remove timestamp object which isn't JSON serializable)
    for e in all_entries:
        e.pop('timestamp', None)

    # Save to JSON
    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump(all_entries[:100], f, ensure_ascii=False, indent=4) # Keep top 100

if __name__ == "__main__":
    fetch_and_sort()
