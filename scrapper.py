import requests
import sqlite3
import re
import time
import telegabot


# Create table if not created before
def create_table():
    # Create table if not created before
    cursor.execute("""CREATE TABLE IF NOT EXISTS pastebin (
        key        VARCHAR (10) PRIMARY KEY ON CONFLICT IGNORE,
        scrape_url TEXT,
        checked    INT,
        matched    INT,
        title      TEXT,
        full_url   TEXT,
        date       DATETIME,
        size       INT,
        expire     DATETIME,
        syntax     TEXT,
        user       TEXT
    )""")
    return db


# Request to API
def get_pastes():
    url = "https://scrape.pastebin.com/api_scraping.php?limit=250"
    r = requests.get(url)
    return r.json()


# Write data to database
def post_to_db():
    for i in get_pastes():
        data = (i['key'], i['scrape_url'], 0, 0, i['title'], i['full_url'], i['date'], i['size'], i['expire'], i['syntax'], i['user'])
        cursor.execute("INSERT INTO pastebin VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
    db.commit()


# Matching with patterns
def matches(content):
    found = []
    total = 0
    with open('keywords_test.txt', 'r') as f:
        patterns = f.read().splitlines()

    for pattern in patterns:
        word = pattern.replace('"', '')
        match = re.findall(r'%s' % word, content, flags=re.IGNORECASE)
        total += len(match)
        found.append({"keyword": word, "matches": len(match)})
    total_count = {"total_count": total}
    return found, total_count


def main():
    post_to_db()
    cursor.execute("SELECT * FROM pastebin WHERE checked IS 0")

    for i in cursor.fetchall():
        r = requests.get(i[1])
        match = matches(r.text)

        data = (1, match[1]['total_count'], i[0])
        cursor.execute("UPDATE pastebin SET checked = ?, matched = ? WHERE key = ?", data)
        db.commit()
        time.sleep(0.5)

        text = ""
        matched = ""

        match_title = matches(i[4])
        match_content = matches(r.text)

        if match[1]['total_count'] > 0:
            text = """*Paste:* %s\n*Matches:* %s""" % (i[5], match[1]['total_count'])

        for m in match_content[0]:
            if m['matches'] > 0:
                matched += "\n\t\t`%s: %s`" % (m['keyword'], m['matches'])

        for m in match_title[0]:
            if m['matches'] > 0:
                matched += "\n\t\t`%s: %s`" % (m['keyword'], m['matches'])

        content = text + matched
        telegabot.send_message(content)  # send to Telegram


if __name__ == "__main__":
    while True:
        # Connect to the database
        db = sqlite3.connect('pastes.db')
        cursor = db.cursor()
        create_table()

        main()
        cursor.close()
        time.sleep(120)
