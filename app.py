from flask import Flask, render_template, request
import redis
import json

app = Flask(__name__)
app.config.from_object('config')
r = redis.StrictRedis(host='localhost', port=6379, db=0)

@app.route('/')
def index():
    currency = r.get('currency')
    return render_template('index.html', currency=json.loads(currency))


if __name__ == '__main__':
    app.run(debug=True)
