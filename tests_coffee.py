import unittest
import coffee
import json


class CoffeeTestCase(unittest.TestCase):

    def setUp(self):
        self.app = coffee.app.test_client()

    def test_order_creation(self):
        resp = self.app.post('/orders/', data=json.dumps({"drink":"tea"}), content_type='application/json')
        resp_data = json.loads(resp.data.decode('utf-8'))
        order = {"drink":"tea", "cost":1.5, "prepared": False}
        self.assertDictEqual(resp_data, order)


if __name__ == '__main__':
    unittest.main()

