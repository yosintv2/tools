import feedparser
import json
import os

# Configuration
RSS_URL = "https://www.gsmarena.com/rss-news-reviews.php3"
OUTPUT_FILE = "gsmarena.json"

def update_feed():
    # Fetch and parse the RSS feed
    feed = feedparser.parse(RSS_URL)
    news_list = []

    for entry in feed.entries:
        # Extract basic data
        item = {
            "title": entry.title,
            "link": entry.link,
            "pubDate": entry.published,
            "description": entry.description, # GSMArena includes the <img> here
            "category": entry.get("category", "News")
        }
        news_list.append(item)

    # Save as gsmarena.json
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(news_list, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Successfully updated {OUTPUT_FILE}")

if __name__ == "__main__":
    update_feed()
