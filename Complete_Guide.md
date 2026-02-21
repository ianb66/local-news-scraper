# The Ultimate Local News Scraper

## Your Personalised, Automated News-Gathering Assistant

**A FREE TOOLKIT FROM THE PEAK PRESS**

**Creator**: Ian Barwell  
**Version**: 2.0  
**Date**: 16 February 2026

---

### Introduction: Stop Searching, Start Analysing

In local journalism, speed and relevance are everything. You can spend hours every day manually checking dozens of websites, blogs, and news portals, or you can spend that time doing what you do best: **writing great stories**.

This toolkit automates the most time-consuming part of your day. It’s a powerful, customisable news scraper that acts as your personal assistant, monitoring hundreds of news sources 24/7 and delivering a perfectly organised digest of the stories that matter to you.

Built by a journalist, for journalists. And now, it's yours to use, for free.

> **A Note from the Creator, Ian Barwell:**
> I built this tool for my own local newsletter, *The Peak Press*. It saved me so much time that I felt I had to share it. My hope is that it empowers other independent journalists to compete with larger outlets by focusing on what truly matters: quality reporting. This isn't just a piece of code; it's a force multiplier for local news.

---

## What This Tool Does For You

- **Monitors Unlimited Sources**: Tracks any news website, blog, or portal with an RSS feed.
- **Finds What Matters**: Uses keyword filtering to find stories about specific towns, people, or topics.
- **Eliminates Noise**: Automatically detects and flags duplicate stories from different sources.
- **Delivers a Perfect Digest**: Generates a clean, organised report in Markdown format, ready for your review.
- **Runs Automatically**: Can be scheduled to run daily or weekly, so the news is waiting for you.
- **Costs Nothing**: It's 100% free. No subscriptions, no hidden fees. It runs on your own computer.

---

## Getting Started: The 5-Minute Setup

This guide will walk you through the three simple steps to get your news scraper running.

### Step 1: Install Python (If You Don't Have It)

This tool is a Python script, a powerful but easy-to-learn programming language. If you've never used it, don't worry. Installation is simple.

1.  **Visit the Official Python Website**: Go to `https://www.python.org/downloads/`.
2.  **Download the Installer**: The website will automatically detect if you're on Windows or Mac and suggest the correct version.
3.  **Run the Installer**: 
    - **On Windows**: **Crucially, check the box that says "Add Python to PATH"** during installation. This makes it much easier to run scripts.
    - **On Mac**: The installer will handle everything for you.

To check it's installed, open your computer's command line tool (Terminal on Mac, Command Prompt or PowerShell on Windows) and type `python --version`. If it shows a version number, you're all set!

### Step 2: Customise Your Scraper

This is where you tell the scraper **what to look for**. Open the `peak_press_scraper.py` file in a simple text editor (like Notepad on Windows or TextEdit on Mac).

You only need to edit the **CONFIGURATION** section at the top.

#### A. Add Your News Sources

Find the `RSS_FEEDS` section. This is where you list the websites you want to monitor. You can find RSS feeds for most news sites by searching for "[website name] RSS feed" on Google.

**Example:**
```python
RSS_FEEDS = {
    'Google News: My Town': 'https://news.google.com/rss/search?q=My+Town+UK+when:7d',
    'BBC Local News':      'https://feeds.bbci.co.uk/news/england/your_region/rss.xml',
    'Local Newspaper':     'https://www.localpaper.co.uk/news/feed/',
}
```

#### B. Add Your Keywords

Find the `KEYWORDS` section. This is the most important part. List all the specific names, places, and topics you want to track.

**Example for a fictional town, "Northwood":**
```python
KEYWORDS = {
    'Settlements': [
        'Northwood',
        'Southwood',
        'Eastwood Village',
    ],
    'People': [
        'Mayor Jane Smith',
        'Councillor Bob Jones',
    ],
    'Topics': [
        'Northwood Council',
        'High Street Regeneration',
    ],
}
```

**Pro Tip**: Be specific! Broad keywords like "news" will return too much. Use exact names of towns, councils, and projects.

### Step 3: Run Your Scraper

1.  Save the `peak_press_scraper.py` file after customising it.
2.  Open your command line tool (Terminal or Command Prompt).
3.  Navigate to the folder where you saved the file. For example, if it's on your Desktop, you might type `cd Desktop`.
4.  Run the script by typing:
    ```bash
    python peak_press_scraper.py
    ```

The scraper will now fetch, analyse, and organise the news for you. It will create two files in the same folder:

-   `news_digest_YYYY-MM-DD.md`: Your beautifully formatted news report.
-   `news_digest_YYYY-MM-DD.json`: The raw data for archiving or advanced use.

---

## Understanding Your News Digest

The generated `.md` file is designed for quick reading.

-   **Summary Header**: Shows total articles found and duplicates detected.
-   **Local Stories**: Articles that match your specific keywords.
-   **Grouped by Keyword**: Stories are organised under the keywords they matched (e.g., all stories about "Northwood" are grouped together).
-   **Clear & Concise**: Each entry shows the title, source, and a direct link.

---

## The Philosophy of Sharing

This tool was created in the spirit of open knowledge and mutual support. Local journalism is the bedrock of a healthy community, and independent journalists need every advantage they can get. By sharing this tool, we hope to strengthen the entire ecosystem of local news.

If you find it useful, the best way to say thanks is to **pay it forward**: share it with another journalist who could benefit from it.

---

**Disclaimer**: This tool is provided free of charge and without warranty. While it has been built to be robust and reliable, it relies on third-party RSS feeds that can change without notice. Always verify information from the original source.
