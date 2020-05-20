import requests
import config


def send_message(text):
    url = config.url
    token = config.token
    chat_id = config.chat_id
    parse_mode = config.parse_mode
    req_api = '%s%s/sendMessage?chat_id=%s&text=%s&parse_mode=%s' % (url, token, chat_id, text, parse_mode)
    r = requests.get(req_api)
    return r.json()
