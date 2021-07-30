import time
import pyupbit
import datetime
import utils
import pytz
from secret_key import access, secret

def get_balance(upbit, ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0


BASE = "KRW"
TICKER = "ONG"
BASE_TICKER = BASE + '-' + TICKER

INTERVAL_MIN = 240
K_RATIO = 0.2
MIN_PRICE = 5000


upbit = pyupbit.Upbit(access, secret)
# KST = datetime.timezone(datetime.timedelta(hours=9))
KST = pytz.timezone('Asia/Seoul')

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now(pytz.timezone('Asia/Seoul'))
        now = now.replace(tzinfo=None)
        start_time = utils.get_start_time(BASE_TICKER, interval=INTERVAL_MIN)
        end_time = start_time + datetime.timedelta(minutes=INTERVAL_MIN)
        print("try buy", start_time, end_time, now)
        if start_time + datetime.timedelta(seconds=10) < now < end_time - datetime.timedelta(seconds=10):
            target_price = utils.get_target_price(ticker=BASE_TICKER, k=K_RATIO, interval=INTERVAL_MIN)
            current_price = utils.get_current_price(ticker=BASE_TICKER)
            print("current, target: %s, %s" %(current_price, target_price))
            if target_price < current_price:
                krw = get_balance(upbit=upbit, ticker=BASE)
                if krw > MIN_PRICE:
                    print('target_price: %f' % target_price)
                    print('current_price: %f' % current_price)
                    print('BUY %f' % krw)
                    upbit.buy_market_order(BASE_TICKER, krw*0.9995)
        else:
            currency = get_balance(upbit=upbit, ticker=TICKER)
            current_price = utils.get_current_price(ticker=BASE_TICKER)
            if currency > (MIN_PRICE/current_price):
                res = upbit.sell_market_order(BASE_TICKER, currency*0.9995)
                print('SELL %f' % currency)
                print('Result %s' % res)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
