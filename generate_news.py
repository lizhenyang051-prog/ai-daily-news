#!/usr/bin/env python3
"""AI Daily News - 每日AI资讯聚合生成器"""

import json
import hashlib
from datetime import datetime, timezone, timedelta
from xml.etree import ElementTree
from urllib.request import urlopen, Request
from urllib.error import URLError
import ssl
import re

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

SOURCES = [
    {
        "name": "机器之心",
        "url": "https://www.jiqizhixin.com/rss",
        "lang": "zh",
        "category": "news"
    },
    {
        "name": "量子位",
        "url": "https://www.qbitai.com/feed",
        "lang": "zh",
        "category": "news"
    },
    {
        "name": "Hacker News",
        "url": "https://hnrss.org/frontpage?count=15",
        "lang": "en",
        "category": "discussion"
    },
    {
        "name": "Arxiv AI论文",
        "url": "http://export.arxiv.org/rss/cs.AI",
        "lang": "en",
        "category": "paper"
    },
    {
        "name": "Arxiv 机器学习",
        "url": "http://export.arxiv.org/rss/cs.LG",
        "lang": "en",
        "category": "paper"
    },
    {
        "name": "MIT Tech Review AI",
        "url": "https://www.technologyreview.com/topic/artificial-intelligence/feed/",
        "lang": "en",
        "category": "news"
    }
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


def fetch_rss(url):
    try:
        req = Request(url, headers=HEADERS)
        resp = urlopen(req, timeout=15, context=ssl_ctx)
        root = ElementTree.fromstring(resp.read())
        return root
    except Exception as e:
        print(f"  ❌ 获取失败: {e}")
        return None


def parse_date(date_str):
    formats = [
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S %Z",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d %H:%M:%S",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except (ValueError, AttributeError):
            continue
    return datetime.now(timezone.utc)


def extract_items(source, root):
    items = []
    channel = root.find("channel")
    if channel is None:
        return items
    for entry in channel.findall("item")[:20]:
        title = entry.findtext("title", "").strip()
        link = entry.findtext("link", "").strip()
        desc = entry.findtext("description", "").strip()
        pub_date = entry.findtext("pubDate", "")
        desc_clean = re.sub(r"<[^>]+>", "", desc)[:300] if desc else ""
        item_id = hashlib.md5((title + link).encode()).hexdigest()[:12]
        try:
            published = parse_date(pub_date)
        except:
            published = datetime.now(timezone.utc)
        items.append({
            "id": item_id,
            "title": title,
            "link": link,
            "summary": desc_clean,
            "source": source["name"],
            "category": source["category"],
            "lang": source["lang"],
            "published": published.strftime("%Y-%m-%d %H:%M:%S"),
            "timestamp": int(published.timestamp())
        })
    return items


def main():
    print("🤖 AI每日日报 - 开始抓取...")
    all_news = []
    for source in SOURCES:
        print(f"  📡 正在获取: {source['name']}...")
        root = fetch_rss(source["url"])
        if root is not None:
            items = extract_items(source, root)
            all_news.extend(items)
            print(f"     ✅ 获取到 {len(items)} 条")
    all_news.sort(key=lambda x: x["timestamp"], reverse=True)
    output = {
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        "articles": all_news
    }
    with open("news_data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 抓取完成！共获取 {len(all_news)} 条新闻")
    print(f"📁 已保存到 news_data.json")


if __name__ == "__main__":
    main()
