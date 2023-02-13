import unittest
import requests


class TestAPI(unittest.TestCase):
    URL = "http://127.0.0.1:5001/v1/investor/mammad"
    URL1 = "http://127.0.0.1:5001/v1/investor"
    data = {"user_id": "mammad", "api_key": "ghazan", "exchange": "rexa", "sub_level": 1, "expire_date": "2023"
            }

    data1 = {"user_id": "mammad", "api_key": "gh", "exchange": "rexa", "sub_level": 1, "expire_date": "2023"
            }

    def test_1(self):
        resp = requests.get(self.URL)
        self.assertEqual(resp.status_code, 200)
        print('test 1 completed')

    def test_2(self):
        resp = requests.post(self.URL1, json=self.data)
        self.assertEqual(resp.status_code, 200)
        print('test 2 completed')

    def test_3(self):
        resp = requests.put(self.URL1, json=self.data1)
        self.assertEqual(resp.status_code, 200)
        print('test 3 completed')

if __name__ == "__main__":
    tester = TestAPI()

    tester.test_1()
    tester.test_2()
    tester.test_3()

# import pytest
#
# from flask import Flask
# from dotenv import dotenv_values
#
# from blueprint import v1_blueprint
#
# from swagger import swagger
# from log import log
#
#
# def test_gets():
#     app = Flask('investor')
#     config = dotenv_values(".env")
#     swagger.run_swagger(app)
#     log.setup_logger()
#     app.register_blueprint(v1_blueprint)
#     app.run(host=config["HOST"], port=config["PORT"], debug=config["DEBUG"])
#
#     with app.test_client() as test_client:
#         response = test_client.get('/investor/mammad')
#         assert response.status_code == 200
