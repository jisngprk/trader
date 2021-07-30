import pandas as pd
import pyupbit
import numpy as np

pd.set_option('display.max_columns', None)
# open, high, low, close, volume
# df = pyupbit.get_ohlcv("KRW-ONG", count=300)
df = pyupbit.get_ohlcv("KRW-ONG", interval="minute20", count=1000)
df['range'] = (df['high'] - df['low']) * 0.3
df['target'] = df['open'] + df['range'].shift(1)
print(df)

#
#
# print(df['high'] > df['target'])
fee = 0.001  # 0.0032
df['ror'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'] - fee,
                     1)
df['ror_nofee'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'],
                     1)
# print(df)
df['hpr'] = df['ror'].cumprod()
df['hpr_nofee'] = df['ror_nofee'].cumprod()

df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
df['dd_nofee'] = (df['hpr_nofee'].cummax() - df['hpr_nofee']) / df['hpr_nofee'].cummax() * 100

print("MDD(%): ", df['dd'].max())
print("CUM HPR(%): ", df['hpr'].iloc[-1])

print("MDD(%) nofee: ", df['dd_nofee'].max())
print("CUM HPR(%) nofee: ", df['hpr_nofee'].iloc[-1])

df.to_excel("dd.xlsx")