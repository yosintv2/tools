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
        
        for entry in feed.entries[:15]: # Fetch more to ensure we don't miss any
            pub_date_parsed = entry.get('published_parsed', entry.get('updated_parsed', None))
            ts = time.mktime(pub_date_parsed) if pub_date_parsed else time.time()
            
            entries.append({
                "title": entry.get('title', 'No Title'),
                "link": entry.get('link', '#'),
                "description": entry.get('summary', entry.get('description', '')).replace('\n', ' '),
                "pubDate": entry.get('published', entry.get('updated', 'Recently')),
                "source": source_name,
                "timestamp": ts # Keep this for sorting
            })
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return entries

def fetch_and_sort():
    # 1. Load Existing Data from news.json if it exists
    existing_data = []
    if os.path.exists('news.json'):
        try:
            with open('news.json', 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
                # Re-add timestamp for sorting (convert pubDate back to ts if needed, 
                # but better to store ts in news.json temporarily or parse pubDate)
                for item in existing_data:
                    if 'timestamp' not in item:
                        try:
                            item['timestamp'] = time.mktime(time.strptime(item['pubDate'], '%a, %d %b %Y %H:%M:%S %Z'))
                        except:
                            item['timestamp'] = 0
        except Exception as e:
            print(f"Error loading existing news.json: {e}")

    # 2. Fetch New Data in Parallel
    new_entries = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(fetch_single_feed, RSS_URLS))
        for res in results:
            new_entries.extend(res)

    # 3. Combine and De-duplicate (using Link as the unique key)
    combined_dict = {item['link']: item for item in existing_data}
    for item in new_entries:
        combined_dict[item['link']] = item # New items overwrite or add to dict

    # 4. Sort by Timestamp (Latest first)
    sorted_list = sorted(combined_dict.values(), key=lambda x: x['timestamp'], reverse=True)

    # 5. Final Cleanup: Keep top 200 items and remove internal timestamp
    final_output = []
    for e in sorted_list[:200]:
        # We keep the timestamp inside news.json this time so future runs 
        # know exactly when the old news was published. 
        # If you want it removed for a cleaner frontend, comment out the line below.
        # e.pop('timestamp', None) 
        final_output.append(e)

    # 6. Save back to news.json
    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump(final_output, f, ensure_ascii=False, indent=4)
    
    print(f"Update Complete. Total stories: {len(final_output)}. Latest: {final_output[0]['title']}")

if __name__ == "__main__":
    fetch_and_sort()
