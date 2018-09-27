import requests
import redis
from datetime import datetime, timedelta
import json
import config

r = redis.StrictRedis(host='localhost', port=6379, db=0)

end_of_day = datetime.utcnow().replace(hour=23, minute=59, second=59, microsecond=999)
yesterday = end_of_day - timedelta(1)
currency = requests.get('https://api.currencyconverterapi.com/api/v6/currencies?apiKey=%s' % config.API_KEY)
currency = currency.json()['results']
for c in currency:
    price = requests.get(
        'https://api.currencyconverterapi.com/api/v6/convert?q=USD_%s&apiKey=%s' % (c, config.API_KEY))
    price_yesterday = requests.get(
        'https://api.currencyconverterapi.com/api/v6/convert?q=USD_%s&compact=ultra&date=%s-%s-%s&apiKey=%s' % (
        c, yesterday.year, yesterday.month, yesterday.day, config.API_KEY))
    currency[c]['price'] = price.json()['results']['USD_%s' % c.upper()]['val']
    currency[c]['price_yesterday'] = list(price_yesterday.json()['USD_%s' % c.upper()].values())[0]
currency = json.dumps(currency)
r.set('currency', currency)
r.expireat('currency', end_of_day)