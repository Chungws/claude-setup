#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Fetch social media post content.

Supports: X (Twitter) via syndication API, Reddit via JSON API, Hacker News via Algolia API
Usage: python3 fetch-social.py <url>
Output: JSON to stdout
"""

from __future__ import annotations

import json
import re
import sys
import urllib.request
import urllib.error


def extract_tweet_id(url: str) -> str | None:
    m = re.search(r"/status/(\d+)", url)
    return m.group(1) if m else None


def fetch_tweet(url: str) -> dict:
    tweet_id = extract_tweet_id(url)
    if not tweet_id:
        return {"error": "cannot extract tweet ID from URL"}

    api_url = f"https://cdn.syndication.twimg.com/tweet-result?id={tweet_id}&lang=en&token=x"
    req = urllib.request.Request(
        api_url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
            "Referer": "https://platform.twitter.com/",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}", "url": url}
    except Exception as e:
        return {"error": str(e), "url": url}

    if not data:
        return {"error": "empty response", "url": url}

    user = data.get("user", {})
    # Handle note_tweet (long tweets) - text field contains full text
    text = data.get("text", "")

    # Media
    media = []
    for m in data.get("mediaDetails", []):
        if m.get("type") == "video":
            media.append({"type": "video", "poster": m.get("media_url_https", "")})
        elif m.get("type") == "photo":
            media.append({"type": "image", "url": m.get("media_url_https", "")})

    for p in data.get("photos", []):
        media.append({"type": "image", "url": p.get("url", "")})

    return {
        "platform": "x",
        "url": url,
        "author": user.get("screen_name", ""),
        "author_name": user.get("name", ""),
        "date": data.get("created_at", ""),
        "text": text,
        "likes": data.get("favorite_count", 0),
        "conversation_count": data.get("conversation_count", 0),
        "media": media,
        "is_verified": user.get("is_blue_verified", False),
    }


def fetch_reddit(url: str) -> dict:
    # Reddit JSON API: append .json
    json_url = re.sub(r"\?.*$", "", url.rstrip("/")) + ".json"

    # urllib is blocked by Reddit — use curl subprocess instead
    import subprocess

    try:
        result = subprocess.run(
            ["curl", "-sL", json_url, "-H", "User-Agent: fetch-social/1.0"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        data = json.loads(result.stdout)
    except subprocess.TimeoutExpired:
        return {"error": "timeout", "url": url}
    except (json.JSONDecodeError, Exception) as e:
        return {"error": str(e), "url": url}

    # Reddit returns [post_listing, comments_listing]
    if not isinstance(data, list) or len(data) < 2:
        return {"error": "unexpected response format", "url": url}

    post_data = data[0]["data"]["children"][0]["data"]
    comments_data = data[1]["data"]["children"]

    top_comments = []
    for c in comments_data[:5]:
        if c["kind"] == "t1":
            cd = c["data"]
            top_comments.append({
                "author": cd.get("author", ""),
                "body": cd.get("body", ""),
                "score": cd.get("score", 0),
            })

    return {
        "platform": "reddit",
        "url": url,
        "subreddit": post_data.get("subreddit", ""),
        "author": post_data.get("author", ""),
        "title": post_data.get("title", ""),
        "body": post_data.get("selftext", ""),
        "score": post_data.get("score", 0),
        "num_comments": post_data.get("num_comments", 0),
        "top_comments": top_comments,
    }


def extract_hn_id(url: str) -> str | None:
    m = re.search(r"id=(\d+)", url)
    if m:
        return m.group(1)
    m = re.search(r"news\.ycombinator\.com/item\?id=(\d+)", url)
    return m.group(1) if m else None


def fetch_hn(url: str) -> dict:
    hn_id = extract_hn_id(url)
    if not hn_id:
        return {"error": "cannot extract HN item ID from URL"}

    api_url = f"https://hn.algolia.com/api/v1/items/{hn_id}"
    req = urllib.request.Request(api_url, headers={"User-Agent": "fetch-social/1.0"})

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}", "url": url}
    except Exception as e:
        return {"error": str(e), "url": url}

    # Extract top comments (first level only)
    top_comments = []
    for child in data.get("children", [])[:5]:
        if child.get("text"):
            top_comments.append({
                "author": child.get("author", ""),
                "text": child.get("text", ""),
            })

    return {
        "platform": "hackernews",
        "url": url,
        "author": data.get("author", ""),
        "title": data.get("title", ""),
        "text": data.get("text", ""),  # for Ask HN / Show HN body text
        "link": data.get("url", ""),   # external link if any
        "points": data.get("points", 0),
        "num_comments": len(data.get("children", [])),
        "top_comments": top_comments,
    }


def main() -> None:
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: fetch-social.py <url>"}))
        sys.exit(1)

    url = sys.argv[1]

    if "x.com/" in url or "twitter.com/" in url:
        result = fetch_tweet(url)
    elif "reddit.com/" in url:
        result = fetch_reddit(url)
    elif "news.ycombinator.com" in url:
        result = fetch_hn(url)
    else:
        result = {"error": f"Unsupported platform: {url}"}
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
