import requests
import time
import json
import os
from datetime import datetime

base_url = "https://hacker-news.firebaseio.com/v0"
headers = {"User-Agent": "TrendPulse/1.0"}

categories = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

def get_category(title):
    title = title.lower()
    for category, keywords in categories.items():
        if any(keyword in title for keyword in keywords):
            return category
    return "other"


def fetch_top_story_ids():
    try:
        return requests.get(f"{base_url}/topstories.json", headers=headers).json()
    except Exception as e:
        print(f"Error fetching top stories: {e}")
        return []


def fetch_story(story_id):
    try:
        return requests.get(f"{base_url}/item/{story_id}.json", headers=headers).json()
    except Exception as e:
        print(f"Error fetching story {story_id}: {e}")
        return None


def main():
    story_ids = fetch_top_story_ids()
    stories = []

    for category, keywords in categories.items():
        # count = 0
        # print(f"processing category: {category}")

        for story_id in story_ids:
            story = fetch_story(story_id)
            if not story:
                continue

            title = story.get("title", "")
            detected_category = get_category(title)

            if detected_category != category:
                continue

            data = {
                "post_id": story.get("id"),
                "title": title,
                "category": category,
                "score": story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "author": story.get("by", "unknown"),
                "collected_at": datetime.now().isoformat()
            }

            stories.append(data)
            # count += 1

            print(f"{category}: {count}/25")

            if count >= 25:
                break

        # time.sleep(2)

    os.makedirs("data", exist_ok=True)
    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(stories, f, indent=2)

    print(f"\nCollected {len(stories)} stories. Saved to {filename}")


if __name__ == "__main__":
    main()