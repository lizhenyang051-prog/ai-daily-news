#!/usr/bin/env python3
"""AI Daily News - \u5c0f\u767d\u53cb\u597d\u7248"""
import json, hashlib, time, re, ssl
from datetime import datetime, timezone
from xml.etree import ElementTree
from urllib.request import urlopen, Request

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE
SOURCE_TIMEOUT = 20

SOURCES = [
    {"name":"\u91cf\u5b50\u4f4d","url":"https://www.qbitai.com/feed","lang":"zh"},
    {"name":"\u673a\u5668\u4e4b\u5fc3","url":"https://www.jiqizhixin.com/rss","lang":"zh"},
    {"name":"\u5c11\u6570\u6d3e","url":"https://sspai.com/feed","lang":"zh"},
    {"name":"Hacker News","url":"https://hnrss.org/frontpage?count=20","lang":"en"},
    {"name":"MIT Tech Review","url":"https://www.technologyreview.com/topic/artificial-intelligence/feed/","lang":"en"},
]

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# 5 types: tool(??), product(??), case(??), knowledge(??), vertical(??)
CATEGORIES = {
    "tool": {"label":"AI\u5de5\u5177\u63a8\u8350","kw":["\u5de5\u5177","\u514d\u8d39","ChatGPT","\u8c46\u5305","\u6587\u5fc3\u4e00\u8a00","\u901a\u4e49\u5343\u95ee","Kimi","Claude","Gemini","Copilot","Notion","\u529f\u80fd\u66f4\u65b0","\u65b0\u529f\u80fd","\u4e0a\u624b","\u4f53\u9a8c","\u5b9e\u6d4b","\u6559\u7a0b","\u6307\u5357","prompt","\u63d0\u793a\u8bcd","\u795e\u5668","\u6548\u7387\u5de5\u5177","\u53d1\u5e03","\u63a8\u51fa","\u4e0a\u7ebf"]},
    "product": {"label":"\u4ea7\u54c1\u52a8\u6001","kw":["OpenAI","Google","Meta","\u5fae\u8f6f","\u82f9\u679c","\u767e\u5ea6","\u963f\u91cc","\u817e\u8baf","\u5b57\u8282","\u534e\u4e3a","GPT-4","GPT-5","Sora","\u591a\u6a21\u6001","\u89c6\u9891\u751f\u6210","Agent","\u5347\u7ea7","\u66f4\u65b0","\u65b0\u7248\u672c","\u91cd\u78c5","\u9996\u53d1","\u5f00\u6e90","Apple Intelligence"]},
    "case": {"label":"\u5b9e\u64cd\u6848\u4f8b","kw":["\u526f\u4e1a","\u53d8\u73b0","\u6548\u7387","\u81ea\u52a8\u5316","\u5de5\u4f5c\u6d41","\u7528AI","\u5b9e\u6218","\u6848\u4f8b","\u7ecf\u9a8c","\u5206\u4eab","\u5b9e\u64cd","\u843d\u5730","\u63d0\u6548","\u521b\u4f5c","\u5185\u5bb9","\u964d\u672c\u589e\u6548","\u601d\u8def","\u65b9\u6cd5","\u6b65\u9aa4","\u624b\u628a\u624b","\u6559\u4f60","\u4e00\u952e\u751f\u6210"]},
    "knowledge": {"label":"\u8ba4\u77e5\u00b7\u907f\u5751","kw":["AI\u5e7b\u89c9","\u667a\u5546\u7a0e","\u7248\u6743","\u9a97\u5c40","\u9020\u5047","\u9274\u522b","\u8bef\u533a","\u79d1\u666e","\u5165\u95e8","\u57fa\u7840","\u539f\u7406","\u907f\u5751","\u8b66\u60d5","\u5e38\u8bc6","\u4e00\u6587\u8bfb\u61c2"]},
    "vertical": {"label":"\u5782\u76f4\u5e94\u7528","kw":["\u5b66\u4e60","\u82f1\u8bed","\u6559\u80b2","\u7f16\u7a0b","\u8bbe\u8ba1","\u8fd0\u8425","\u8425\u9500","\u81ea\u5a92\u4f53","\u76f4\u64ad","\u7535\u5546","\u5ba2\u670d","\u529e\u516c","Excel","\u6587\u6863","\u603b\u7ed3","\u4f1a\u8bae","\u7ffb\u8bd1","\u6570\u636e\u5206\u6790","\u62a5\u544a","\u804c\u573a","\u6253\u5de5\u4eba"]}
}

SKIP_WORDS = ["\u878d\u8d44","\u80a1\u4ef7","\u6536\u8d2d","\u6295\u8d44","IPO","\u4e0a\u5e02","\u8d22\u62a5","\u4eba\u4e8b\u53d8\u52a8","\u79bb\u804c","\u4efb\u547d","\u664b\u5347","\u4f30\u503c"]

def fetch(url):
    for a in range(2):
        try:
            req = Request(url, headers=HEADERS)
            resp = urlopen(req, timeout=SOURCE_TIMEOUT, context=ssl_ctx)
            return ElementTree.fromstring(resp.read())
        except Exception as e:
            print(f"  [{a+1}] {e}")
            if a == 0: time.sleep(2)
    return None

def pdate(s):
    for fmt in ["%a, %d %b %Y %H:%M:%S %z","%a, %d %b %Y %H:%M:%S %Z","%Y-%m-%dT%H:%M:%S%z","%Y-%m-%dT%H:%M:%SZ","%Y-%m-%d %H:%M:%S","%Y-%m-%dT%H:%M:%S"]:
        try: return datetime.strptime(s.strip(), fmt)
        except: continue
    return datetime.now(timezone.utc)

def classify(title, summary):
    text = (title + " " + summary).lower()
    scores = {}
    for cid, cinfo in CATEGORIES.items():
        s = 0
        for kw in cinfo["kw"]:
            if kw.lower() in text:
                s += 1 + (1 if kw.lower() in title.lower() else 0)
        if s > 0: scores[cid] = s
    return max(scores, key=scores.get) if scores else "tool"

def skip_article(title, summary):
    t = (title + " " + summary).lower()
    return any(w.lower() in t for w in SKIP_WORDS)

def extract(src, root):
    items = []
    ch = root.find("channel")
    if ch is None: return items
    for entry in ch.findall("item")[:20]:
        title = entry.findtext("title","").strip()
        link = entry.findtext("link","").strip()
        desc = re.sub(r"<[^>]+>","",entry.findtext("description",""))[:300]
        if skip_article(title, desc): continue
        items.append({
            "id": hashlib.md5((title+link).encode()).hexdigest()[:12],
            "title": title, "link": link, "summary": desc,
            "source": src["name"], "category": classify(title, desc),
            "lang": src["lang"],
            "published": pdate(entry.findtext("pubDate","")).strftime("%Y-%m-%d %H:%M:%S"),
            "timestamp": int(pdate(entry.findtext("pubDate","")).timestamp())
        })
    return items

def main():
    print("Starting AI Daily News (Beginner Edition)...")
    news = []
    for src in SOURCES:
        print(f"  {src['name']}...", end=" ", flush=True)
        root = fetch(src["url"])
        if root:
            items = extract(src, root)
            news.extend(items)
            print(f"[OK {len(items)}]")
        else:
            print("[SKIP]")
    news.sort(key=lambda x: x["timestamp"], reverse=True)
    with open("news_data.json","w",encoding="utf-8") as f:
        json.dump({"updated_at":datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),"articles":news}, f, ensure_ascii=False, indent=2)
    print(f"Done! Total: {len(news)}")

if __name__ == "__main__":
    main()
