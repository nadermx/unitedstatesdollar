import requests
import redis
from datetime import datetime, timedelta
import json
import config

r = redis.StrictRedis(host='localhost', port=6379, db=0)

end_of_day = datetime.utcnow().replace(hour=23, minute=59, second=59, microsecond=999)
yesterday = end_of_day - timedelta(1)
seven_days_ago = end_of_day - timedelta(7)
currency = requests.get('https://api.currencyconverterapi.com/api/v6/currencies?apiKey=%s' % config.API_KEY)
currency = currency.json()['results']
for c in currency:
    price = requests.get(
        'https://api.currencyconverterapi.com/api/v6/convert?q=USD_%s&apiKey=%s' % (c, config.API_KEY))
    price_yesterday = requests.get(
        'https://api.currencyconverterapi.com/api/v6/convert?q=USD_%s&compact=ultra&date=%s-%s-%s&apiKey=%s' % (
            c, yesterday.year, yesterday.month, yesterday.day, config.API_KEY))
    seven_day_price = requests.get(
        'https://api.currencyconverterapi.com/api/v6/convert?q=USD_%s&compact=ultra&date=%s-%s-%s&endDate=%s-%s-%s&apiKey=%s' % (
            c, seven_days_ago.year, seven_days_ago.month, seven_days_ago.day, end_of_day.year, end_of_day.month,
            end_of_day.day,
            config.API_KEY))
    currency[c]['price'] = price.json()['results']['USD_%s' % c.upper()]['val']
    currency[c]['price_yesterday'] = list(price_yesterday.json()['USD_%s' % c.upper()].values())[0]
    currency[c]['seven_days_price'] = seven_day_price.json()['USD_%s' % c.upper()]
currency = json.dumps(currency)
r.set('currency', currency)
r.expireat('currency', end_of_day)
