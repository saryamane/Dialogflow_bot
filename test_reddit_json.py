import json
import os
import requests
import random

from flask import Flask
from flask import request
from flask import make_response

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

req = """{
  "responseId": "4237d9fc-96c5-4864-ac8c-d0ddf1e64fd5-5e314962",
  "queryResult": {
    "queryText": "tell me a joke",
    "action": "reddit.TellAJokeOrFact",
    "parameters": {
      "say-content": "joke"
    },
    "allRequiredParamsPresent": true,
    "fulfillmentText": "Here's a joke",
    "fulfillmentMessages": [
      {
        "text": {
          "text": [
            "Here's a joke"
          ]
        }
      }
    ],
    "intent": {
      "name": "projects/tripplanner-kxiomr/agent/intents/461c7c31-6b69-4c02-9820-8ffeddff3296",
      "displayName": "Joke_Intent"
    },
    "intentDetectionConfidence": 1,
    "diagnosticInfo": {
      "webhook_latency_ms": 193
    },
    "languageCode": "en"
  },
  "webhookStatus": {
    "code": 13,
    "message": "Webhook call failed. Error: 500 Internal Server Error."
  }
}
"""

makeRedditResponse(req)
