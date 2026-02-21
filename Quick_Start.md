# Quick Start: The Ultimate Local News Scraper

**Get up and running in 5 minutes.**

---

### Step 1: Install Python

1.  Go to `https://www.python.org/downloads/`
2.  Download and run the installer.
3.  **On Windows, check "Add Python to PATH"**.

---

### Step 2: Customise Your Scraper

Open `peak_press_scraper.py` in a text editor.

**A. Add RSS Feeds:**
```python
RSS_FEEDS = {
    # Add your news sources here
    # Example:
    # 'My Town News': 'https://news.google.com/rss/search?q=My+Town+UK+when:7d',
}
```

**B. Add Keywords:**
```python
KEYWORDS = {
    # Add your keywords here
    # Example:
    # 'Settlements': ['My Town', 'My Village'],
}
```

---

### Step 3: Run the Scraper

1.  Open your command line (Terminal/Command Prompt).
2.  Navigate to the scraper's folder (`cd Desktop`).
3.  Run the command:
    ```bash
    python peak_press_scraper.py
    ```

---

**Done!** Check the folder for your `news_digest_YYYY-MM-DD.md` file.
