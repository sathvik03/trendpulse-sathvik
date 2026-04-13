# Task 1 - Fetch Data from HackerNews API
# Collect trending stories and group into categories

import requests
import time
import json
import os
from datetime import datetime

# base API url
base_url = "https://hacker-news.firebaseio.com/v0"

# required header
headers = {"User-Agent": "TrendPulse/1.0"}

# keywords for category matching
categories = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# function to detect category from title
def get_category(title):
    title = title.lower()
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in title:
                return category
    return None


def main():
    print("Fetching top story IDs...")

    # step 1 - fetch first 500 story ids
    try:
        response = requests.get(f"{base_url}/topstories.json", headers=headers)
        story_ids = response.json()[:500]
    except Exception as e:
        print("Error fetching IDs:", e)
        return

    stories = []

    # loop through each category
    for category in categories.keys():
        print(f"\nProcessing category: {category}")
        count = 0

        for story_id in story_ids:
            try:
                story = requests.get(
                    f"{base_url}/item/{story_id}.json",
                    headers=headers
                ).json()
            except Exception:
                print(f"Failed to fetch story {story_id}")
                continue

            # skip if no title
            if not story or "title" not in story:
                continue

            title = story["title"]
            detected_category = get_category(title)

            # match only current category
            if detected_category != category:
                continue

            # extract required fields
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
            count += 1

            print(f"{category}: {count}/25")

            # collect max 25 per category
            if count == 25:
                break

        # sleep after each category (as per instructions)
        time.sleep(2)

    # create data folder if not exists
    os.makedirs("data", exist_ok=True)

    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    # save json file
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(stories, f, indent=2)

    print(f"\nCollected {len(stories)} stories. Saved to {filename}")


if __name__ == "__main__":
    main()