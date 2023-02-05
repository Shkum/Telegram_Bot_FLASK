from flask import Flask
import requests


app = Flask(__name__)

URL = 'https://api.telegram.org/bot5433931992:AAG7ykhximKcgFz-SY6-zjNenTVQ7X4h0dQ/'


def main():
    r = requests.get(URL + 'getMe')
    print(r.json())

if __name__ == '__main__':
    main()