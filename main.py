from flask import Flask
from flask import jsonify
from flask import request
import requests
import json
import re

from keys import *

from flask_sslify import SSLify

app = Flask(__name__)
sslify = SSLify(app)

URL = f'https://api.telegram.org/bot{telegram_token}/'


def write_json(data, filename='answer.json'):
    with open(filename, 'w', encoding='UTF-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def send_message(chat_id, text='bla-bla-bla'):
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=answer)
    return r.json()


def parse_text(text):
    pattern = r'/\w+'
    crypto = re.search(pattern, text).group()
    return crypto[1:]


def get_price(crypto):
    url = 'https://pro-api.coinmarketcap.com/v1/exchange/assets'
    parameters = {
        'id': '270',
        # 'start': '1',
        # 'limit': '5000',
        # 'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': coin_token,
    }

    r = requests.get(url, params=parameters, headers=headers).json()
    write_json(r, filename='price.json')
    # return r['data'][47]['currency']['price_usd']
    for i in r['data']:
        if i['currency']['name'].lower() == crypto.lower():
            try:
                return (i['currency']['price_usd'])
            except:
                pass
    return 'Currency not found'


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        write_json(r)
        try:
            chat_id = r['message']['chat']['id']
            message = r['message']['text']
            pattern = r'/\w+'
            if re.search(pattern, message):
                price = get_price(parse_text(message))
                send_message(chat_id, text=price)
            else:
                send_message(chat_id, text='Currency not found')
            return jsonify(r)
        except:
            pass
    return '<h1>HELLO bot</h1>'


if __name__ == '__main__':
    app.run()
