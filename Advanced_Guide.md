# Advanced Customisation Guide

**For Power Users**

---

### Scheduling Your Scraper to Run Automatically

Manually running the script is great for testing, but the real power comes from automation. Here’s how to set it up to run on a schedule.

#### On Windows (Using Task Scheduler)

1.  **Open Task Scheduler**: Search for it in the Start Menu.
2.  **Create Basic Task**: In the "Actions" pane, click "Create Basic Task".
3.  **Name Your Task**: e.g., "Daily News Scraper".
4.  **Set the Trigger**: Choose "Daily", "Weekly", etc., and set a time.
5.  **Set the Action**: Choose "Start a program".
6.  **Program/script**: Enter `python.exe`.
7.  **Add arguments (optional)**: Enter the full path to your script, e.g., `C:\Users\YourName\Desktop\peak_press_scraper.py`.
8.  **Start in (optional)**: Enter the folder path, e.g., `C:\Users\YourName\Desktop\`.
9.  **Finish**: Complete the wizard.

Your scraper will now run automatically at the time you specified.

#### On Mac/Linux (Using Cron)

Cron is a powerful, standard tool for scheduling tasks.

1.  **Open Terminal**.
2.  **Edit the crontab**: Type `crontab -e` and press Enter.
3.  **Add a new line**: To run the script every day at 8:00 AM, add:
    ```cron
    0 8 * * * /usr/bin/python3 /path/to/your/peak_press_scraper.py
    ```
    - `0 8 * * *` means at minute 0 of hour 8, every day, every month, every day of the week.
    - Replace `/path/to/your/` with the actual path to your script.
4.  **Save and Exit**: The process depends on your default editor (often Nano or Vim).

---

### Advanced Filtering: Excluding Keywords

Want to ignore certain stories? You can add a simple filter.

1.  Add an `EXCLUDE_KEYWORDS` list to your configuration:
    ```python
    EXCLUDE_KEYWORDS = ["obituary", "sponsored content", "traffic report"]
    ```
2.  In the `parse_feed` function, add a check after fetching the article text:
    ```python
    full_text = f"{title} {summary}"
    
    # Check for excluded keywords
    if any(keyword.lower() in full_text.lower() for keyword in EXCLUDE_KEYWORDS):
        continue # Skip this article
    ```

---

### Changing the Output Format

The script generates Markdown (`.md`) by default. You could change it to HTML.

1.  In the `generate_markdown_report` function, change the output to use HTML tags:
    ```python
    # From:
    report.append(f"### {settlement} ({len(articles_list)} stories)")
    report.append(f"**{article["title"]}**")
    
    # To:
    report.append(f"<h3>{settlement} ({len(articles_list)} stories)</h3>")
    report.append(f"<b>{article["title"]}</b>")
    ```
2.  Change the output filename at the end of the `main` function:
    ```python
    filename = f"/home/ubuntu/news_digest_{timestamp}.html"
    ```

---

### Integrating with Other Tools (e.g., Email)

You can have the script email the digest to you.

1.  Add this function to your script:
    ```python
    import smtplib
    from email.mime.text import MIMEText

    def send_email(subject, body, sender, recipients, password):
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = ", ".join(recipients)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())
    ```
2.  At the end of the `main` function, call it:
    ```python
    # After saving the report file
    SENDER_EMAIL = "your_email@gmail.com"
    SENDER_PASSWORD = "your_app_password" # Use a Google App Password
    RECIPIENT_EMAIL = "your_email@gmail.com"
    
    send_email(
        subject=f"News Digest - {timestamp}",
        body=report,
        sender=SENDER_EMAIL,
        recipients=[RECIPIENT_EMAIL],
        password=SENDER_PASSWORD
    )
    print("Email digest sent!")
    ```

This provides a powerful way to get your news digest delivered directly to your inbox.
