import unittest
import coffee
import json


class CoffeeTestCase(unittest.TestCase):

    def setUp(self):
        self.app = coffee.app.test_client()
        self.order = {"drink":"tea", "cost":1.5, "prepared": False}
        self.payment = {"cost":1.5, "amount":1.5, "paid":True}

    def test_order_creation(self):
        resp = self.app.post('/orders/', data=json.dumps({"drink":"tea"}), content_type='application/json')
        resp_data = json.loads(resp.data.decode('utf-8'))
        self.assertDictEqual(resp_data, self.order)
        self.assertEqual(resp.headers['Location'], "http://localhost/orders/0")
        self.assertEqual(resp.status_code, 201)

    def test_order_creation_fail(self):
        resp =self.app.post('/orders/', data=json.dumps({"hello":"world"}), content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    def test_order_read(self):
        resp = self.app.get('/orders/0')
        resp_data = json.loads(resp.data.decode('utf-8'))
        self.assertDictEqual(resp_data, self.order)
        self.assertEqual(resp.status_code, 200)

    def test_order_update(self):
        resp = self.app.put('/orders/0', data=json.dumps({"drink":"expresso"}), content_type='application/json')
        resp_data = json.loads(resp.data.decode('utf-8'))
        self.order["drink"] = "expresso"
        self.assertDictEqual(resp_data, self.order)
        self.assertEqual(resp.status_code, 200)

    def test_payment(self):
        resp = self.app.put('/payment/orders/0', data=json.dumps({"amount":1.50}), content_type='application/json')
        resp_data = json.loads(resp.data.decode('utf-8'))
        self.assertDictEqual(resp_data, self.payment)
        self.assertEqual(resp.status_code, 201)

    def test_queue_orders(self):
        resp = self.app.get('/orders/')
        resp_data = json.loads(resp.data.decode('utf-8'))
        self.order["drink"] = "expresso"
        self.assertSequenceEqual(resp_data, [self.order])
        self.assertEqual(resp.status_code, 200)

    def test_payment_read(self):
        resp = self.app.get('/payment/orders/0')
        resp_data = json.loads(resp.data.decode('utf-8'))
        self.assertDictEqual(resp_data, self.payment)
        self.assertEqual(resp.status_code, 200)



if __name__ == '__main__':
    unittest.main()

