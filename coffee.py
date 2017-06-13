from flask import Flask, request, Response
import json

app = Flask(__name__)
orders = []
payments = {}

@app.route('/orders/', methods=['POST'])
def place_order():
    body = request.get_json()
    
    # Add new order to orders list
    new_order = {"drink": body["drink"], "cost": 1.50, "prepared": False}
    order_id = len(orders)
    orders.append(new_order)
    
    # Generate response
    resp = Response(json.dumps(new_order))
    resp.headers['Location'] = request.url_root + 'orders/' + str(order_id)
    resp.status_code = 201
    return resp


@app.route('/orders/<int:order_id>', methods=['GET','PUT'])
def order(order_id):
    order = orders[order_id]
    if request.method == 'PUT':
        # Check if order is modifiable
        if order['prepared']:
            code = 409
        else:
            body = request.get_json()
            order["drink"] = body["drink"]
            code = 200
    else:
        code = 200
    # Return the response
    resp = Response(json.dumps(order))
    resp.status_code = code
    return resp

@app.route('/payment/orders/<int:order_id>', methods=['PUT'])
def pay(order_id):
    order = orders[order_id]
    body = request.get_json()
    payment = {"amount": body["amount"], "cost": order["cost"], "paid": body["amount"] >= order["cost"]}
    payments[order_id] = payment
    resp = Response(json.dumps(payment))
    resp.status_code = 201
    return resp
    
