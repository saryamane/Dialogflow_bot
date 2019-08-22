import json
import os
import requests
import random

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


# noinspection SpellCheckingInspection
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print(json.dumps(req, indent=4))
    result = req.get("queryResult")
    action = result.get("action")
    if action == 'fetchWeatherForecast':
        res = makeWeatherResponse(req)
    elif action == 'reddit.TellAJokeOrFact':
        res = makeRedditResponse(req)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


# TODO create a function for the bot to retrieve the joke or TIL of the day from reddit

def makeRedditResponse(req):
    result = req.get("queryResult")
    parameters = result.get("parameters")
    content_type = parameters.get("say-content")
    print("Content - Type Entity is: ", content_type)
    i_rand = random.randrange(20)
    print("Random number between 0 and 10 : ", i_rand)
    if content_type is None:
        return None

    if content_type == 'fact':
        # invoke the Reddit api to parse the JSON for TIL
        r = requests.get('https://www.reddit.com/r/todayILearned/top.json?sort=top&t=day')
        json_object = r.json()
        til_data = json_object['data']['children']
        til_content = til_data[i_rand]['data']['title']

        return {
            "fulfillment_text": til_content,
            "webhook_source": "reddit-til-subreddit"
        }
    elif content_type == 'joke':
        # TODO invoke the Reddit api for parsing the joke JSON.
        r = requests.get('https://www.reddit.com/r/jokes/top.json?sort=top&t=day')
        json_object = r.json()
        joke_data = json_object['data']['children']
        joke_content = joke_data[i_rand]['data']['selftext']

        return {
            "fulfillment_text": joke_content,
            "webhook_source": "reddit-joke-subreddit"
        }


# TODO create a function to retrieve the latest product name from product table based on SKU_Code and vice versa

# noinspection PyPep8Naming
def makeWeatherResponse(req):
    result = req.get("queryResult")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    print("City value: ", city)
    date_value = parameters.get("date")
    date = date_value.split('T')[0]
    print("Date value: ", date)
    if city is None:
        return None
    r = requests.get(
        'http://api.openweathermap.org/data/2.5/forecast?q=' + city + '&appid=06f070197b1f60e55231f8c46658d077')
    json_object = r.json()
    weather = json_object['list']
    for i in range(0, 30):
        if date in weather[i]['dt_txt']:
            condition = weather[i]['weather'][0]['description']
            break
    speech = "The forecast for " + city + " on " + date + " is " + condition
    # noinspection SpellCheckingInspection
    return {
        "fulfillment_text": speech,
        "webhook_source": "heroku-weather-webhook"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
