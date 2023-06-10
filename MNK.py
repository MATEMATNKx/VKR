import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from statsmodels.graphics.tsaplots import plot_acf
from utils import AR_calc
from utils import line_trend
# read csv
df = pd.read_csv("Sales-02.csv")
df["Год"] = pd.date_range("2010-01-01", periods=df.shape[0], freq="M")
df = df.iloc[::, [i for i in range(40) if i not in [13, 23, 24, 33, 35, 36, 37, 38]]]


# calculate salary from percent
S = 1*df.iloc[0, 1]/100
S_ = [S]
for i in range(1, df.shape[0]):
    S_.append(S_[i-1] * df.iloc[i, 1]/100)

# Dataset plot
plt.plot(S_[:-12])
plt.grid()


start = 5 * 12
df_1 = pd.DataFrame(S_)
df_1["t"] = df_1[0]

df_1 = df_1.iloc[start::]
df_1.reset_index(drop=True, inplace=True)

# calculate correlation
_ = df_1.iloc[:12, [-1]]
_['t-12'] = df_1.iloc[12:24, -1].values
_['t-24'] = df_1.iloc[24:36, -1].values
_['t-36'] = df_1.iloc[36:48, -1].values
print(f'Current correlation: \n{_.corr()}')


# call MNK for trend
s = 0
n = 84# 143
for i in range(1):
    trend_coefficient = line_trend(df_1, df_1.columns[i+1], i+1, start=s, end=n)
    df_1[f"{df_1.columns[i+1]}-Trend"] = trend_coefficient['a'] * np.arange(0, df_1.shape[0]) + trend_coefficient['b']
    df_1[f'{df_1.columns[i+1]}-minus'] = df_1[df_1.columns[i+1]] - df_1[f'{df_1.columns[i+1]}-Trend']
df_1.iloc[:n, 1:].plot()
plt.grid()



acf = plot_acf(df_1['t-minus'], lags=np.arange(df_1.shape[0]), zero=False)
plt.title("")
plt.xticks(np.arange(int(df_1.shape[0]) + 2), [""+str(i)*(i % 12 == 0) for i in range((df_1.shape[0]) + 2)])
plt.grid()
plt.show()

s = 60# 120
n = 84# 144
print(df_1.shape)
print(df_1[s:n:])
print(df_1[s:n].shape)
value = AR_calc(df_1[s:n], 't-minus')
real = df_1['t'][s:n]
model = value['a'] * df_1['t-minus'][s+12:n] + value['b']
model_tr = model + trend_coefficient['a'] * np.arange(s+12, n) + trend_coefficient['b']
plt.plot(np.arange(s+12, n), model_tr, label='Моделируемые значения')
plt.plot(np.arange(0, n+12), df_1['t'][:n+12], label='Настоящие значения')

forecast = value['a'] * model + value['b'] + trend_coefficient['a'] * np.arange(s+12+12, n+12) + trend_coefficient['b']
plt.plot(np.arange(s+12+12, n+12), forecast.values, label='Предсказанные значения')
plt.legend()
plt.grid()
plt.show()
print(f"MAPE for each model points:")
point = 0
erro = 0
for x in zip(df_1['t'][s+12:n], model_tr):
    erro += round(abs(x[0] - x[1]) / x[0], 4)
    print(f'{point}: {round(x[0], 4)}, {round(x[1], 4)}, {round(abs(x[0]-x[1]) / x[0], 4)}')
    point+=1
print(erro/point)
print(f"MAPE for each forecasted points:")
point = 0
erro = 0
for x in zip(df_1['t'][s+12+12:n+12], forecast):
    erro +=round(abs(x[0]-x[1]) / x[0], 4)
    print(f'{point}: {round(x[0], 4)}, {round(x[1], 4)}, {round(abs(x[0]-x[1]) / x[0], 4)}')
    point+=1
print(erro/point)

