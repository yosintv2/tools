import feedparser
import json
import time
import socket
import os
import concurrent.futures
from datetime import datetime

# Set a global timeout for feed fetching
socket.setdefaulttimeout(15)

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

def fetch_single_feed(url):
    entries = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    try:
        feed = feedparser.parse(url, agent=headers['User-Agent'])
        source_name = feed.feed.get('title', url.split('/')[2].replace('www.', '')).split(' - ')[0].split(' : ')[0].strip()
        
        for entry in feed.entries[:15]:
            pub_date_parsed = entry.get('published_parsed', entry.get('updated_parsed', None))
            # Use parsed time or current time as fallback
            ts = time.mktime(pub_date_parsed) if pub_date_parsed else time.time()
            
            entries.append({
                "title": entry.get('title', 'No Title'),
                "link": entry.get('link', '#'),
                "description": entry.get('summary', entry.get('description', '')).replace('\n', ' '),
                "pubDate": entry.get('published', entry.get('updated', 'Recently')),
                "source": source_name,
                "timestamp": ts 
            })
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return entries

def fetch_and_sort():
    # 1. Load Existing Data
    existing_data = []
    if os.path.exists('news.json'):
        try:
            with open('news.json', 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        except Exception as e:
            print(f"Error loading existing news.json: {e}")

    # 2. Fetch New Data in Parallel
    new_entries = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(fetch_single_feed, RSS_URLS))
        for res in results:
            new_entries.extend(res)

    # 3. Combine and De-duplicate
    combined_dict = {item['link']: item for item in existing_data}
    for item in new_entries:
        combined_dict[item['link']] = item 

    # 4. Filter for Last 3 Days Only
    # 3 days = 3 * 24 * 60 * 60 seconds
    three_days_ago = time.time() - (3 * 24 * 60 * 60)
    
    filtered_list = [
        item for item in combined_dict.values() 
        if item.get('timestamp', 0) > three_days_ago
    ]

    # 5. Sort by Timestamp (Latest first)
    sorted_list = sorted(filtered_list, key=lambda x: x['timestamp'], reverse=True)

    # 6. Save back to news.json
    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump(sorted_list, f, ensure_ascii=False, indent=4)
    
    print(f"Clean-up complete. Kept {len(sorted_list)} articles from the last 3 days.")

if __name__ == "__main__":
    fetch_and_sort()
