from flask import Flask, render_template, request
import requests
import redis
from datetime import datetime, timedelta
import json

app = Flask(__name__)
app.config.from_object('config')
r = redis.StrictRedis(host='localhost', port=6379, db=0)


@app.route('/')
def index():
    currency = r.get('currency')
    if not currency:
        end_of_day = datetime.utcnow().replace(hour=23, minute=59, second=59, microsecond=999)
        yesterday = end_of_day - timedelta(1)
        currency = requests.get('https://free.currencyconverterapi.com/api/v6/currencies')
        currency = currency.json()['results']
        for c in currency:
            price = requests.get('https://free.currencyconverterapi.com/api/v6/convert?q=USD_%s' % c)
            price_yesterday = requests.get(
                'https://free.currencyconverterapi.com/api/v6/convert?q=USD_%s&compact=ultra&date=%s-%s-%s' % (c, yesterday.year, yesterday.month, yesterday.day))
            currency[c]['price'] = price.json()['results']['USD_%s' % c.upper()]['val']
            currency[c]['price_yesterday'] = list(price_yesterday.json()['USD_%s' % c.upper()].values())[0]
        currency = json.dumps(currency)
        r.set('currency', currency)
        r.expireat('currency', end_of_day)
    return render_template('index.html', currency=json.loads(currency))


if __name__ == '__main__':
    app.run(debug=True)
