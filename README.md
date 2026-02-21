# Local News Scraper

**Automated RSS news monitoring for local journalists**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

---

## Overview

The Local News Scraper is a powerful, customisable tool that automates news gathering for local journalists. It monitors multiple RSS feeds, filters stories by keywords, detects duplicates, and generates organised digests—saving you hours of manual research every day.

Built by a journalist, for journalists.

## Features

✅ **Monitor Unlimited Sources** - Track any news website with an RSS feed  
✅ **Smart Filtering** - Find stories about specific towns, people, or topics  
✅ **Duplicate Detection** - Automatically flags the same story from different sources  
✅ **Clean Digests** - Generates organised Markdown reports  
✅ **Automated Scheduling** - Set it and forget it  
✅ **100% Free** - No subscriptions, no hidden costs

## Quick Start

### 1. Install Python

Download Python 3.7+ from [python.org](https://www.python.org/downloads/)

**Windows users**: Check "Add Python to PATH" during installation

### 2. Install Dependencies

```bash
pip install feedparser
```

### 3. Customise the Scraper

Edit `news_scraper.py` and add your RSS feeds and keywords:

```python
RSS_FEEDS = {
    'Google News: My Town': 'https://news.google.com/rss/search?q=My+Town+UK+when:7d',
    'BBC Local': 'https://feeds.bbci.co.uk/news/england/your_region/rss.xml',
}

KEYWORDS = {
    'Settlements': ['My Town', 'My Village'],
    'Topics': ['Council', 'Planning'],
}
```

### 4. Run It

```bash
python news_scraper.py
```

Your digest will be saved as `news_digest_YYYY-MM-DD.md`

## Documentation

- **[Quick Start Guide](Quick_Start.md)** - Get running in 5 minutes
- **[Complete Guide](Complete_Guide.md)** - Detailed instructions
- **[Advanced Customisation](Advanced_Guide.md)** - Scheduling, filtering, and more

## Example Output

```markdown
# LOCAL NEWS DIGEST
**Generated**: 16 February 2026
**Total Articles**: 68 | **Duplicates**: 5

## 📍 LOCAL STORIES

### Glossop (12 stories)

**Council approves new development**
- Source: Local Times
- Link: https://...
- Topics: Planning, Council
```

## Use Cases

- **Local Newsletters** - Automate news gathering for weekly/daily newsletters
- **Community Journalism** - Track stories across multiple towns
- **Issue Monitoring** - Follow specific topics (planning, environment, etc.)
- **Competitive Intelligence** - See what other outlets are covering

## About

This tool was created by **Ian Barwell**, founder of [The Peak Press](https://thepeakpress.com), a local newsletter serving the High Peak and surrounding areas.

After building this for my own newsletter and seeing how much time it saved, I decided to share it with the journalism community.

## License

MIT License - Free to use, modify, and distribute with attribution.

## Contributing

Contributions welcome! Please open an issue or submit a pull request.

## Support

- **Issues**: [GitHub Issues](https://github.com/ianb66/local-news-scraper/issues)
- **Questions**: Open a discussion or contact via The Peak Press

---

**Made with ❤️ for local journalism**
