import requests
from bs4 import BeautifulSoup as bs

r = requests.get('https://pastebin.com/archive')
html = bs(r.content, 'html.parser')

table = html.find("table", attrs="maintable")

# for tr in html.find_all("tr"):
#     print(tr)
