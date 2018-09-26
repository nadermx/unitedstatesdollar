from flask import Flask, render_template, request
import requests
import redis

app = Flask(__name__)
app.config.from_object('config')

@app.route('/')
def index():
    currency = requests.get('https://free.currencyconverterapi.com/api/v6/currencies')
    for c in currency.json()['results']:
        price = requests.get('https://free.currencyconverterapi.com/api/v6/convert?q=USD_%s' % c)
        print(price.json()['results']['USD_%s' % c.upper()]['id'], price.json()['results']['USD_%s' % c.upper()]['val'])
        break
    return 'ok'
    # return render_template('index.html', currency=currency.json())


if __name__ == '__main__':
    app.run(debug=True)