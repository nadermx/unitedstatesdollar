from flask import Flask, render_template, request
import requests
import redis
from datetime import datetime
import json

app = Flask(__name__)
app.config.from_object('config')
r = redis.StrictRedis(host='localhost', port=6379, db=0)
@app.route('/')
def index():
    currency = r.get('currency_new')
    if not currency:
        end_of_day = datetime.utcnow().replace(hour=23, minute=59, second=59, microsecond=999)
        currency = requests.get('https://free.currencyconverterapi.com/api/v6/currencies')
        currency = currency.json()['results']
        for c in currency:
            price = requests.get('https://free.currencyconverterapi.com/api/v6/convert?q=USD_%s' % c)
            currency[c]['price'] = price.json()['results']['USD_%s' % c.upper()]['val']
        currency = json.dumps(currency)
        r.set('currency_new', currency)
        r.expireat('currency_new', end_of_day)
    print(json.loads(currency))
    return render_template('index.html', currency=json.loads(currency))

if __name__ == '__main__':
    app.run(debug=True)