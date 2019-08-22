import json
import os
import requests

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print(json.dumps(req, indent=4))
    result = req.get("queryResult")
    action_value = result.get("action")
    print('Identified action value is', action_value)
    if action_value == 'getProductSkuMap':
        res = makeProductSku(req)
    else:
        res = makeResponse(req)
    
    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeProductSku(req):
    result = req.get("queryResult")
    parameters = result.get("parameters")
    cloud_name = parameters.get("crm-product-name")
    edition_name = parameters.get("crm-edition-name")
    if cloud_name == 'Sales Cloud' and edition_name == 'Professional':
        sku_code = '200012628'
    elif cloud_name == 'Sales Cloud' and edition_name == 'Unlimited':
        sku_code = '200012632'
    elif cloud_name == 'Sales Cloud' and edition_name == 'Enterprise':
        sku_code = '200012625'
    elif cloud_name == 'Service Cloud' and edition_name == 'Professional':
        sku_code = '200012640'
    elif cloud_name == 'Service Cloud' and edition_name == 'Unlimited':
        sku_code = '200012643'
    elif cloud_name == 'Service Cloud' and edition_name == 'Enterprise':
        sku_code = '200012637'
    elif cloud_name == 'Force.com' and edition_name == 'Professional':
        sku_code = 'No product sku available'
    elif cloud_name == 'Force.com' and edition_name == 'Unlimited':
        sku_code = '200000441'
    elif cloud_name == 'Force.com' and edition_name == 'Enterprise':
        sku_code = '200000133'
    return {
    "fulfillment_text": sku_code,
    "webhook_source": "heroku-prodsku-webhook"
    }

def makeResponse(req):
    result = req.get("queryResult")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    print("City value: ", city)
    date_value = parameters.get("date")
    if date_value is not None: 
        date = date_value.split('T')[0]
    print("Date value: ", date)
    if city is None:
        return None
    r=requests.get('http://api.openweathermap.org/data/2.5/forecast?q='+city+'&appid=06f070197b1f60e55231f8c46658d077')
    json_object = r.json()
    weather=json_object['list']
    for i in range(0,30):
        if date in weather[i]['dt_txt']:
            condition= weather[i]['weather'][0]['description']
            break
    speech = "The forecast for "+city+ " on "+date+" is "+condition
    return {
    "fulfillment_text": speech,
    "webhook_source": "heroku-weather-webhook"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
