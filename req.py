import requests
import json

body = json.dumps({'drink':'tea'})
url = 'http://127.0.0.1:5000/orders/'

def send():
    return requests.post(url, json=body)

