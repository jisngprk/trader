import time
import pyupbit
import datetime
import utils
import datetime
import requests

# s
# out = datetime.datetime.strptime(out, "%Y-%m-%dT%H:%M:%S")


# url = "https://api.upbit.com/v1/orderbook"
#
# headers = {"Accept": "application/json"}
# params = {'markets': ['KRW-BTC', 'KRW-ONG']}
# response = requests.request("GET", url, headers=headers, params=params)
#
# print(response.text)
# data = response.json()
#
# print(data)


out = utils.get_current_price(ticker='KRW-ONG')  # 1: 872 = x: 5000 =>  5000/872
print(5000/out)
