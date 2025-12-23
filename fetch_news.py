import feedparser
import json
import time
import socket
import os
import re
import concurrent.futures

# Increase timeout to 20 seconds to give slow Nepali servers time to respond
socket.setdefaulttimeout(20)

RSS_URLS = [
    "https://www.ratopati.com/feed", 
    "https://www.setopati.com/feed", 
    "https://nepalnews.com/feed/",
    "https://www.nepalpress.com/feed/", 
    "https://annapurnapost.com/rss/",
    "https://lokaantar.com/rss/", 
    "https://ujyaaloonline.com/rss/",
    "https://baahrakhari.com/feed/", 
    "https://newsofnepal.com/feed/",
    "https://farakdhar.com/feed/", 
    "https://www.nepalviews.com/feed/",
    "https://techpana.com/feed/", 
    "https://english.onlinekhabar.com/feed/",
    "https://neplays.com/feed/", 
    "https://www.ajakoartha.com/feed/"
]

def extract_thumbnail(entry):
    """Deep search for images in description, media tags, or content."""
    if 'media_content' in entry:
        return entry.media_content[0]['url']
    
    # Search for <img> tags in description (Common for Ratopati/Setopati)
    content = entry.get('description', '') + entry.get('summary', '')
    if 'content' in entry:
        content += entry.content[0].value
    
    img_match = re.search(r'<img [^>]*src=["\']([^"\']+)["\']', content)
    if img_match:
        return img_match.group(1)
    
    return ""

def fetch_single_feed(url):
    entries = []
    # Realistic Headers to bypass firewalls
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/xml,application/xml,application/xhtml+xml'
    }
    
    try:
        # Use the requests-style agent via feedparser
        feed = feedparser.parse(url, agent=headers['User-Agent'])
        
        if not feed.entries:
            print(f"⚠️ No entries found for: {url} (Site might be blocking request)")
            return []

        source_name = feed.feed.get('title', url.split('/')[2]).split(' - ')[0].split(' : ')[0].strip()
        
        for entry in feed.entries[:20]: # Fetch up to 20 per site
            # Strictly use Source Time
            parsed_time = entry.get('published_parsed') or entry.get('updated_parsed')
            
            if parsed_time:
                sort_ts = time.mktime(parsed_time)
                
                # Clean HTML tags from description
                desc = entry.get('summary', entry.get('description', ''))
                clean_desc = re.sub('<[^<]+?>', '', desc).replace('&nbsp;', ' ').strip()

                entries.append({
                    "title": entry.get('title', 'No Title'),
                    "link": entry.get('link', '#'),
                    "description": clean_desc[:250], # Limit length for 'shorts'
                    "pubDate": entry.get('published', entry.get('updated', '')),
                    "source": source_name,
                    "image": extract_thumbnail(entry),
                    "sort_ts": sort_ts
                })
    except Exception as e:
        print(f"❌ Error fetching {url}: {e}")
    return entries

def fetch_and_sort():
    # 1. Load Existing Local Data for 3-day history
    existing_data = []
    if os.path.exists('news.json'):
        with open('news.json', 'r', encoding='utf-8') as f:
            try:
                existing_data = json.load(f)
                # Re-calculate sort_ts for existing items based on their pubDate
                for item in existing_data:
                    if 'sort_ts' not in item:
                        try:
                            # Try parsing standard RSS date string
                            dt = item['pubDate']
                            item['sort_ts'] = time.mktime(time.strptime(dt, '%a, %d %b %Y %H:%M:%S %Z'))
                        except:
                            item['sort_ts'] = 0
            except:
                existing_data = []

    # 2. Fetch New Data (Parallel)
    print("Starting multi-threaded fetch...")
    new_entries = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(RSS_URLS)) as executor:
        results = list(executor.map(fetch_single_feed, RSS_URLS))
        for res in results:
            new_entries.extend(res)

    # 3. Merge & Deduplicate (URL is the unique key)
    combined_dict = {item['link']: item for item in existing_data}
    for item in new_entries:
        combined_dict[item['link']] = item 

    # 4. Filter: Keep only last 3 days
    now_ts = time.time()
    three_days_ago = now_ts - (3 * 24 * 60 * 60)
    
    filtered_list = [
        item for item in combined_dict.values() 
        if item.get('sort_ts', 0) > three_days_ago
    ]

    # 5. SORT: Strictly Newest (Source Time) First
    sorted_list = sorted(filtered_list, key=lambda x: x['sort_ts'], reverse=True)

    # 6. Cleanup: Remove sort_ts before saving
    for item in sorted_list:
        item.pop('sort_ts', None)

    # 7. Final Save
    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump(sorted_list, f, ensure_ascii=False, indent=4)
    
    print(f"✅ Success! Total {len(sorted_list)} articles saved. Newest at the top.")

if __name__ == "__main__":
    fetch_and_sort()
