from flask import Flask, request, Response
import json

app = Flask(__name__)
orders = []
payments = {}

@app.route('/orders/', methods=['GET', 'POST'])
def list_orders():
    if request.method == 'GET':
        resp = Response(json.dumps(orders))
        resp.status_code = 200
    else:
        body = request.get_json()
        
        # Verify user input
        if not "drink" in body:
            resp = Response(json.dumps({"status":400, "message": "Your order must contain a 'drink' choice"}))
            resp.status_code = 400
            return resp

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
    
    # Verify order existence
    if not order_id < len(orders):
        resp = Response(json.dumps({"status":404, "message": "This order does not exist."}))
        resp.status_code = 404
        return resp

    order = orders[order_id]

    if request.method == 'PUT':
        body = request.get_json()
        if not "drink" in body:
            resp = Response(json.dumps({"status":400, "message": "Your order must contain a 'drink' choice"}))
            resp.status_code = 400
            return resp

        # Check if order is modifiable
        if order['prepared']:
            code = 409
        else:
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
    # Verify order existence
    if not order_id < len(orders):
        resp = Response(json.dumps({"status":404, "message": "This order does not exist."}))
        resp.status_code = 404
        return resp

    order = orders[order_id]
    body = request.get_json()
    if not "amount" in body:
            resp = Response(json.dumps({"status":400, "message": "Your payment must contain an 'amount' field."}))
            resp.status_code = 400
            return resp

    payment = {"amount": body["amount"], "cost": order["cost"], "paid": body["amount"] >= order["cost"]}
    payments[order_id] = payment
    resp = Response(json.dumps(payment))
    resp.status_code = 201
    return resp
    
