from flask import Flask, request, Response
import json

app = Flask(__name__)
orders = []


@app.route('/orders/', methods=['POST'])
def place_order():
    content = request.get_json()
    body = json.loads(content)
    new_order = {"drink": body["drink"], "cost": 1.50, "prepared": False}
    order_id = len(orders)
    orders.append(new_order)
    resp = Response(json.dumps(new_order))
    resp.headers['Location'] = request.url_root + 'orders/' + str(order_id)
    resp.status_code = 201
    return resp

