import requests
from html.parser import HTMLParser
import time
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:75.0) Gecko/20100101 Firefox/75.0',
}

keywords = [
    "kaspersky",
    "kaspersky-lab",
    "@kaspersky.com",
    "@kaspersky",
    "MyKaspersky",
    "avp.ru",
    "hqproxyusr.avp.ru",
    "hqproxyusr",
    "proxyusr.avp.ru",
    "KLDFS",
    "KLSRL",
    "KLBox",
    "KL Box",
    "safekids"
]


class LinkParser(HTMLParser):
    def __init__(self):
        self.links = []
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr in attrs:
                if attr[0] == "href":
                    self.links.append(attr[1])


def matches(content):
    found = []
    for keyword in keywords:
        word = keyword.replace('"', '')
        match = re.findall(r'%s' % word, content, flags=re.IGNORECASE)
        found.append({"keyword": word, "matches": len(match)})
    return found


def get_paste_raw(paste_id):
    r = requests.get("https://pastebin.com/raw" + paste_id, headers=headers)
    return r.text


def get_pub_pastes():
    r = requests.get("https://pastebin.com/archive", headers=headers)
    lp = LinkParser()
    lp.feed(r.text)
    for link in lp.links:
        if len(link) == 9:
            print("\nPaste:", "https://pastebin.com" + link)
            print("Matches:")
            for match in matches(get_paste_raw(link)):
                print("\t", match["keyword"], match["matches"])
            time.sleep(3)


if __name__ == "__main__":
    get_pub_pastes()