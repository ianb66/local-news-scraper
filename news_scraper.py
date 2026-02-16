#!/usr/bin/env python3
"""
The Peak Press — RSS News Scraper v2
Full settlement list for High Peak Borough + Peak District.
Run every Monday or Tuesday before Wednesday's issue.

Output: news_digest_YYYY-MM-DD.md + news_digest_YYYY-MM-DD.json
"""

import sys
import io

# Fix Windows console encoding so Unicode characters (✓, ✗, emojis) print correctly
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import feedparser
import json
from datetime import datetime
from collections import defaultdict
import hashlib
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

# ============================================================================
# CONFIGURATION — Edit these to add/remove sources and keywords
# ============================================================================

RSS_FEEDS = {
    'Google News: High Peak':     'https://news.google.com/rss/search?q=High+Peak+Derbyshire+when:7d&hl=en-GB&gl=GB&ceid=GB:en',
    'Google News: Buxton':        'https://news.google.com/rss/search?q=Buxton+Derbyshire+when:7d&hl=en-GB&gl=GB&ceid=GB:en',
    'Google News: Glossop':       'https://news.google.com/rss/search?q=Glossop+Derbyshire+when:7d&hl=en-GB&gl=GB&ceid=GB:en',
    'Google News: Peak District': 'https://news.google.com/rss/search?q=Peak+District+when:7d&hl=en-GB&gl=GB&ceid=GB:en',
    'Google News: Whaley Bridge': 'https://news.google.com/rss/search?q=Whaley+Bridge+when:7d&hl=en-GB&gl=GB&ceid=GB:en',
    'Google News: Chapel Frith':  'https://news.google.com/rss/search?q=Chapel-en-le-Frith+when:7d&hl=en-GB&gl=GB&ceid=GB:en',
    'Google News: Hope Valley':   'https://news.google.com/rss/search?q=Hope+Valley+Derbyshire+when:7d&hl=en-GB&gl=GB&ceid=GB:en',

    # BBC — direct feeds, always reliable
    'BBC Manchester':             'https://feeds.bbci.co.uk/news/england/manchester/rss.xml',
    'BBC East Midlands':          'https://feeds.bbci.co.uk/news/england/leicester/rss.xml',
    'BBC UK News':                'https://feeds.bbci.co.uk/news/uk/rss.xml',

    # Guardian
    'The Guardian UK':            'https://www.theguardian.com/uk/rss',
}
KEYWORDS = {
    # Every settlement in High Peak Borough
    'Settlements': [
        'Ashopton',
        'Bamford',
        'Brough',
        'Shatton',
        'Buxton',
        'Buxworth',
        'Castleton',
        'Chapel-en-le-Frith',
        'Chapel en le Frith',
        'Charlesworth',
        'Chinley',
        'Chisworth',
        'Crowden',
        'Derwent',
        'Dove Holes',
        'Edale',
        'Fernilee',
        'Furness Vale',
        'Gamesley',
        'Glossop',
        'Hadfield',
        'Hayfield',
        'Hope',
        'Horwich End',
        'New Mills',
        'Old Glossop',
        'Padfield',
        'Peak Forest',
        'Peak Dale',
        'Rowarth',
        'Sparrowpit',
        'Taxal',
        'Thornhill',
        'Tintwistle',
        'Whaley Bridge',
        'Woodhead',
    ],

    # Area terms
    'Area & Landmarks': [
        'High Peak',
        'Dark Peak',
        'White Peak',
        'Peak District',
        'Peak District National Park',
        'Kinder Scout',
        'Mam Tor',
        'Odin Mine',
        'Bleaklow',
        'Stanage Edge',
        'Derwent Valley',
        'Hope Valley',
        'Goyt Valley',
        'Longdendale',
        'Snake Pass',
        'Toddbrook Reservoir',
    ],

    # Councils and authorities
    'Councils & Bodies': [
        'High Peak Borough',
        'High Peak Borough Council',
        'Derbyshire County Council',
        'Peak District National Park Authority',
        'Derbyshire Dales',
        'National Trust',
    ],

    # Key transport routes
    'Transport Routes': [
        'Snake Pass',
        'A57',
        'A6',
        'A623',
        'Hope Valley line',
        'Glossop line',
        'Buxton line',
        'Bee Network',
        'Northern Rail',
        'TransPennine',
    ],
}

TOPICS = {
    'Planning & Development': [
        'planning permission', 'planning application', 'development',
        'housing', 'construction', 'demolition', 'listed building',
        'conservation area', 'green belt', 'planning appeal',
    ],
    'Council & Politics': [
        'council', 'councillor', 'borough', 'county', 'election',
        'consultation', 'policy', 'budget', 'cabinet', 'committee',
        'reform', 'labour', 'conservative', 'liberal democrat',
    ],
    'Transport & Roads': [
        'road', 'rail', 'bus', 'cycling', 'closure', 'diversion',
        'snake pass', 'a57', 'bee network', 'trains', 'station',
        'pothole', 'roadworks', 'traffic',
    ],
    'Community & Events': [
        'fundraising', 'volunteer', 'charity', 'community group',
        'event', 'festival', 'celebration', 'heritage', 'history',
        'market', 'show', 'fair', 'carnival',
    ],
    'Business': [
        'opening', 'closing', 'closure', 'new business', 'restaurant',
        'pub', 'shop', 'café', 'cafe', 'jobs', 'investment', 'expansion',
        'award', 'entrepreneur',
    ],
    'Environment & Nature': [
        'environment', 'nature', 'wildlife', 'flooding', 'climate',
        'renewable', 'conservation', 'national park', 'reservoir',
        'co2', 'carbon', 'pipeline', 'moorland', 'rewilding',
    ],
    'Outdoor & Leisure': [
        'walking', 'hiking', 'cycling', 'fell running', 'climbing',
        'outdoor', 'trail', 'path', 'moorland', 'reservoir',
        'rambling', 'mountain rescue', 'access land',
    ],
    'Health & Emergency': [
        'hospital', 'nhs', 'ambulance', 'fire', 'police', 'crime',
        'accident', 'incident', 'missing', 'search and rescue',
        'mountain rescue',
    ],
    'Education': [
        'school', 'college', 'pupils', 'students', 'ofsted',
        'headteacher', 'term', 'half term', 'sixth form',
    ],
    'History & Heritage': [
        'history', 'heritage', 'historic', 'listed', 'ancient',
        'archaeology', 'museum', 'memorial', 'anniversary',
        'victorian', 'industrial', 'mine', 'mill',
    ],
}

# ============================================================================
# CORE SCRAPER LOGIC — No need to edit below this line
# ============================================================================

def get_article_hash(title, link):
    content = f"{title.lower()}{link}"
    return hashlib.md5(content.encode()).hexdigest()[:12]


def detect_keywords(text, keyword_dict):
    text_lower = text.lower()
    found = []
    for category, keywords in keyword_dict.items():
        for keyword in keywords:
            if keyword.lower() in text_lower:
                found.append(keyword)
    return list(set(found))


def detect_topics(text):
    text_lower = text.lower()
    found = []
    for topic, keywords in TOPICS.items():
        for keyword in keywords:
            if keyword in text_lower:
                found.append(topic)
                break
    return found


def resolve_url(url, timeout=5):
    """Follow Google News redirects to get the real article URL."""
    if 'news.google.com' not in url:
        return url
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.url
    except Exception:
        return url  # If redirect fails, keep the original


def resolve_urls_parallel(urls, workers=10):
    """Resolve a list of URLs in parallel. Returns a dict of {original: resolved}."""
    google_urls = [u for u in urls if 'news.google.com' in u]
    other_urls = [u for u in urls if 'news.google.com' not in u]

    resolved = {u: u for u in other_urls}  # Non-Google URLs stay as-is

    if not google_urls:
        return resolved

    print(f"  Resolving {len(google_urls)} Google News URLs (10 at a time)...")
    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_url = {executor.submit(resolve_url, url): url for url in google_urls}
        for future in as_completed(future_to_url):
            original = future_to_url[future]
            try:
                resolved[original] = future.result()
            except Exception:
                resolved[original] = original

    return resolved


def parse_feed(feed_url, source_name):
    print(f"Fetching {source_name}...")
    try:
        feed = feedparser.parse(feed_url)

        # Collect all raw links first
        raw_entries = []
        for entry in feed.entries:
            raw_entries.append({
                'title':    entry.get('title', 'No title'),
                'link':     entry.get('link', ''),
                'summary':  entry.get('description', entry.get('summary', '')),
                'pub_date': entry.get('published', entry.get('updated', '')),
            })

        # Resolve all Google News URLs in parallel
        all_links = [e['link'] for e in raw_entries]
        resolved = resolve_urls_parallel(all_links)

        # Build articles with resolved links
        articles = []
        for entry in raw_entries:
            link = resolved.get(entry['link'], entry['link'])
            full_text = f"{entry['title']} {entry['summary']}"
            articles.append({
                'hash':     get_article_hash(entry['title'], link),
                'title':    entry['title'],
                'link':     link,
                'summary':  entry['summary'],
                'published': entry['pub_date'],
                'source':   source_name,
                'keywords': detect_keywords(full_text, KEYWORDS),
                'topics':   detect_topics(full_text)
            })

        print(f"  ✓ {len(articles)} articles from {source_name}")
        return articles
    except Exception as e:
        print(f"  ✗ ERROR {source_name}: {e}")
        return []


def detect_duplicates(articles):
    seen = {}
    duplicates = []
    for article in articles:
        key = article['title'].lower().strip()
        if key in seen:
            duplicates.append({'article': article, 'duplicate_of': seen[key]})
        else:
            seen[key] = article
    return duplicates


def filter_local_stories(articles):
    """Return only articles that match a High Peak keyword."""
    return [a for a in articles if a['keywords']]


def generate_markdown_report(articles, duplicates, local_only):
    report = []
    report.append("# THE PEAK PRESS — NEWS DIGEST")
    report.append(f"**Generated**: {datetime.now().strftime('%A %d %B %Y at %H:%M')}")
    report.append(f"**Total fetched**: {len(articles)} | **Local/relevant**: {len(local_only)} | **Duplicates**: {len(duplicates)}")
    report.append("")
    report.append("---")
    report.append("")
    report.append("## 📍 LOCAL STORIES")
    report.append("")
    report.append("*Stories mentioning a High Peak settlement, landmark, council, or route.*")
    report.append("")

    keyword_articles = defaultdict(list)
    for article in local_only:
        for keyword in article['keywords']:
            keyword_articles[keyword].append(article)

    for keyword, arts in sorted(keyword_articles.items(), key=lambda x: len(x[1]), reverse=True):
        report.append(f"### {keyword} ({len(arts)} {'story' if len(arts) == 1 else 'stories'})")
        report.append("")
        seen = set()
        for a in arts:
            if a['hash'] not in seen:
                seen.add(a['hash'])
                report.append(f"**{a['title']}**")
                report.append(f"- Source: {a['source']}")
                report.append(f"- Link: {a['link']}")
                if a['topics']:
                    report.append(f"- Topics: {', '.join(a['topics'])}")
                if a['summary']:
                    s = a['summary'][:200] + "..." if len(a['summary']) > 200 else a['summary']
                    report.append(f"- Summary: {s}")
                report.append("")
        report.append("")

    report.append("---")
    report.append("")
    report.append("## 📊 BY TOPIC")
    report.append("")

    topic_articles = defaultdict(list)
    for article in local_only:
        for topic in article['topics']:
            topic_articles[topic].append(article)

    for topic, arts in sorted(topic_articles.items(), key=lambda x: len(x[1]), reverse=True):
        report.append(f"**{topic}**: {len(arts)} {'story' if len(arts) == 1 else 'stories'}")

    report.append("")

    if duplicates:
        report.append("---")
        report.append("")
        report.append("## 🔄 DUPLICATES")
        report.append("")
        for dup in duplicates:
            a, o = dup['article'], dup['duplicate_of']
            report.append(f"**{a['title']}** — {a['source']} + {o['source']}")
        report.append("")

    report.append("---")
    report.append("")
    report.append("## 📰 ALL ARTICLES (unfiltered)")
    report.append("")
    for a in articles:
        report.append(f"- **{a['title']}** — {a['source']}")

    report.append("")
    report.append("---")
    report.append("*The Peak Press RSS Scraper v2*")

    return "\n".join(report)


def main():
    print("=" * 60)
    print("THE PEAK PRESS — RSS NEWS SCRAPER v2")
    print("=" * 60)
    print()

    all_articles = []
    for source_name, feed_url in RSS_FEEDS.items():
        all_articles.extend(parse_feed(feed_url, source_name))

    print()
    print(f"Total collected: {len(all_articles)}")

    duplicates = detect_duplicates(all_articles)
    local_stories = filter_local_stories(all_articles)

    print(f"Local/relevant: {len(local_stories)}")
    print(f"Duplicates: {len(duplicates)}")
    print()

    report = generate_markdown_report(all_articles, duplicates, local_stories)

    timestamp = datetime.now().strftime('%Y-%m-%d')
    md_file = f"news_digest_{timestamp}.md"
    json_file = f"news_digest_{timestamp}.json"

    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"Digest: {md_file}")

    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump({
            'generated': datetime.now().isoformat(),
            'total_articles': len(all_articles),
            'local_stories': len(local_stories),
            'articles': all_articles,
            'duplicates': [
                {'article': d['article'], 'duplicate_of_title': d['duplicate_of']['title']}
                for d in duplicates
            ]
        }, f, indent=2, ensure_ascii=False)
    print(f"Raw data: {json_file}")

    print()
    print("=" * 60)
    print("COMPLETE")
    print("=" * 60)

    return md_file


if __name__ == '__main__':
    main()
