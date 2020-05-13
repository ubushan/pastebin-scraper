import requests
from html.parser import HTMLParser
import time
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:75.0) Gecko/20100101 Firefox/75.0',
}


class LinkParser(HTMLParser):
    def __init__(self):
        self.links = []
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr in attrs:
                if attr[0] == "href":
                    self.links.append(attr[1])


def matches(keyword, content):
    word = keyword.replace('"', '')
    match = re.findall(r'%s' % word, content, flags=re.IGNORECASE)
    return len(match)


def get_paste_raw(paste_id):
    r = requests.get("https://pastebin.com/raw" + paste_id, headers=headers)
    return r.text


def get_pub_pastes():
    r = requests.get("https://pastebin.com/archive", headers=headers)
    lp = LinkParser()
    lp.feed(r.text)
    for link in lp.links:
        if len(link) == 9:
            print("Paste:", "https://pastebin.com" + link,
                  "\tMatches:", matches("kaspersky", get_paste_raw(link)))
            time.sleep(3)


if __name__ == "__main__":
    get_pub_pastes()