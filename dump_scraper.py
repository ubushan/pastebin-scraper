import requests


api_url = "https://psbdmp.ws/api/v2/search/"
pastebin = "https://scrape.pastebin.com/api_scrape_item.php?i="


# Search URLs
by_general = api_url
by_domain = api_url + "domain/"
by_email = api_url + "email/"


search_word = "leaks"
r = requests.get(by_general + search_word)


print('Search :', r.json()['search'])
print('-'*20)

if r.json()['count'] > 0:
    for i in r.json()['data']:
        r = requests.get(pastebin + i['id'])
        if r.text != "Error, we cannot find this paste.":
            print(pastebin + i['id'], i['time'])