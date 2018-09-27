from flask import Flask, render_template, request
import redis
import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)
app.config.from_object('config')
r = redis.StrictRedis(host='localhost', port=6379, db=0)

@app.route('/')
def index():
    currency = r.get('currency')
    currency[c]['seven_days_price']
    days = []
    values = []
    for k, v in currency[c]['seven_days_price'].items():
        days.append(k)
        values.append(v)
    plt.plot_date(x=days, y=values, fmt="r-")
    plt.ylabel(c)
    plt.savefig('static/%s.png' % c)
    return render_template('index.html', currency=json.loads(currency))



@app.route('/plot')
def plot():
    currency = json.loads(r.get('currency'))
    for c in currency:
        currency[c]['seven_days_price']
        days = []
        values = []
        for k, v in currency[c]['seven_days_price'].items():
            days.append(k)
            values.append(v)
        plt.plot_date(x=days, y=values, fmt="r-")
        plt.ylabel(c)
        plt.savefig('static/%s.png' % c)
        break
    return "ok"


if __name__ == '__main__':
    app.run(debug=True)
