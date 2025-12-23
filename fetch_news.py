import feedparser
import json
import time
import socket
import os
import concurrent.futures

# Set global timeout
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
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        feed = feedparser.parse(url, agent=headers['User-Agent'])
        # Clean source name
        source_name = feed.feed.get('title', url.split('/')[2]).split(' - ')[0].split(' : ')[0].strip()
        
        for entry in feed.entries:
            # We ONLY take the time provided by the original source
            parsed_time = entry.get('published_parsed') or entry.get('updated_parsed')
            
            if parsed_time:
                # Convert source time to a numeric timestamp just for internal sorting
                sort_ts = time.mktime(parsed_time)
                
                entries.append({
                    "title": entry.get('title', 'No Title'),
                    "link": entry.get('link', '#'),
                    "description": entry.get('summary', entry.get('description', '')).replace('\n', ' '),
                    "pubDate": entry.get('published') or entry.get('updated'),
                    "source": source_name,
                    "sort_ts": sort_ts # We use this to ensure NEWEST is on TOP
                })
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return entries

def fetch_and_sort():
    # 1. Load Existing Data
    existing_data = []
    if os.path.exists('news.json'):
        with open('news.json', 'r', encoding='utf-8') as f:
            try:
                existing_data = json.load(f)
            except:
                existing_data = []

    # 2. Fetch New Data
    new_entries = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(fetch_single_feed, RSS_URLS))
        for res in results:
            new_entries.extend(res)

    # 3. Merge by Link (Prevents duplicates, keeps source data)
    combined_dict = {item['link']: item for item in existing_data}
    for item in new_entries:
        combined_dict[item['link']] = item 

    # 4. Filter: Keep only last 3 days (259200 seconds)
    three_days_ago = time.time() - 259200
    filtered_list = [
        item for item in combined_dict.values() 
        if item.get('sort_ts', 0) > three_days_ago
    ]

    # 5. SORT: Newest Source Time First
    # This ensures "New Data should show in first"
    sorted_list = sorted(filtered_list, key=lambda x: x['sort_ts'], reverse=True)

    # 6. Cleanup: Remove the internal sort_ts before saving so users don't see it
    for item in sorted_list:
        if 'sort_ts' in item:
            del item['sort_ts']

    # 7. Save
    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump(sorted_list, f, ensure_ascii=False, indent=4)
    
    print(f"Update Successful. Newest news is at the top.")

if __name__ == "__main__":
    fetch_and_sort()
