import feedparser
import json
import time
import socket
import os
import re
import concurrent.futures

# Set global timeout 
# "________", "______",
socket.setdefaulttimeout(15)

RSS_URLS = [
    "https://www.ratopati.com/feed", 
    "https://www.setopati.com/feed", "https://nepalnews.com/feed",
    "https://www.nepalpress.com/feed", "https://annapurnapost.com/rss",
    "https://lokaantar.com/rss/", "https://ujyaaloonline.com/rss",
    "https://baahrakhari.com/feed", "https://newsofnepal.com/feed/",
    "https://farakdhar.com/rss/", "https://www.nepalviews.com/rss",
    "https://techpana.com/rss", "https://english.onlinekhabar.com/feed",
    "https://neplays.com/feed", "https://www.ajakoartha.com/feed"
]

def extract_thumbnail(entry):
    """Deep search for thumbnails in various RSS tags and HTML content."""
    # 1. Check standard media tags
    if 'media_content' in entry:
        return entry.media_content[0]['url']
    if 'media_thumbnail' in entry:
        return entry.media_thumbnail[0]['url']
    
    # 2. Check for <img> tag inside description or summary (Common in Nepal News)
    content = entry.get('description', '') + entry.get('summary', '')
    if 'content' in entry:
        content += entry.content[0].value
        
    img_match = re.search(r'<img [^>]*src=["\']([^"\']+)["\']', content)
    if img_match:
        return img_match.group(1)
        
    # 3. Check enclosures
    if 'links' in entry:
        for link in entry.links:
            if 'image' in link.get('type', ''):
                return link.get('href', '')
    return ""

def fetch_single_feed(url):
    entries = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        feed = feedparser.parse(url, agent=headers['User-Agent'])
        source_name = feed.feed.get('title', url.split('/')[2]).split(' - ')[0].split(' : ')[0].strip()
        
        for entry in feed.entries:
            parsed_time = entry.get('published_parsed') or entry.get('updated_parsed')
            
            if parsed_time:
                # Numeric timestamp ONLY for sorting purposes
                sort_ts = time.mktime(parsed_time)
                
                # Clean description of HTML tags
                clean_desc = re.sub('<[^<]+?>', '', entry.get('summary', entry.get('description', '')))
                
                entries.append({
                    "title": entry.get('title', 'No Title'),
                    "link": entry.get('link', '#'),
                    "description": clean_desc.strip()[:200],
                    "pubDate": entry.get('published') or entry.get('updated'),
                    "source": source_name,
                    "image": extract_thumbnail(entry),
                    "sort_ts": sort_ts
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
                # Ensure existing items have sort_ts for re-sorting
                for item in existing_data:
                    if 'sort_ts' not in item and 'pubDate' in item:
                        try:
                            item['sort_ts'] = time.mktime(time.strptime(item['pubDate'], '%a, %d %b %Y %H:%M:%S %Z'))
                        except: item['sort_ts'] = 0
            except: pass

    # 2. Fetch New Data
    new_entries = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(fetch_single_feed, RSS_URLS))
        for res in results: new_entries.extend(res)

    # 3. Merge and De-duplicate
    combined_dict = {item['link']: item for item in existing_data}
    for item in new_entries:
        combined_dict[item['link']] = item 

    # 4. Filter: Only news from last 3 days
    three_days_ago = time.time() - (3 * 24 * 60 * 60)
    filtered = [i for i in combined_dict.values() if i.get('sort_ts', 0) > three_days_ago]

    # 5. SORT: Newest Source Time First (This puts fresh updates at top)
    sorted_list = sorted(filtered, key=lambda x: x['sort_ts'], reverse=True)

    # 6. Final cleanup before saving
    for item in sorted_list:
        if 'sort_ts' in item: del item['sort_ts']

    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump(sorted_list, f, ensure_ascii=False, indent=4)
    
    print(f"Saved {len(sorted_list)} items. Newest is at the top.")

if __name__ == "__main__":
    fetch_and_sort()
