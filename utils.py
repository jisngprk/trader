import requests
import datetime

def get_min_price(ticker, interval, count):
    if interval not in [1, 3, 5, 15, 10, 30, 60, 240]:
        raise ValueError

    url = "https://api.upbit.com/v1/candles/minutes/" + str(interval)
    querystring = {"market": ticker, "count": count}
    headers = {"Accept": "application/json"}

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()

    return data

def get_current_price(ticker):
    url = "https://api.upbit.com/v1/orderbook"

    headers = {"Accept": "application/json"}
    params = {'markets': ticker}
    response = requests.request("GET", url, headers=headers, params=params)

    data = response.json()
    data = data[0]
    current_price = data['orderbook_units'][0]['ask_price']

    return current_price


def get_start_time(ticker, interval):
    data = get_min_price(ticker=ticker, interval=interval, count=1)
    data = data[0]

    start_time = data['candle_date_time_kst']
    start_time = datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S")
    return start_time

def get_target_price(ticker, k, interval):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    data = get_min_price(ticker=ticker, interval=interval, count=2)
    cur, priv = data
    target_price = priv['trade_price'] + (priv['high_price'] - priv['low_price']) * k

    return target_price


