import numpy as np
import pandas as pd


def line_trend(dataset, name , i, start = 0, end = -1):
    """
    i - по какому столбцу вычислить тренд. Индекс от 0 (счет колонок идёт с нуля)
    dataset - набор данных
    n - количество показателей, на которых будет происходить вычисление МНК
    start, end - начало и конец включительно, номер месяца как m*k, где m - месяц года, k-год
    """
    df = dataset.copy()
    if end == -1:
        df_new = df.iloc[start::]
    else:
        df_new = df.iloc[start:end+1]
    X = df_new.index.values
    y = df_new.iloc[::, i].values
    n = df_new.shape[0]
    a = n * (np.sum(X*y)) - (X.sum()*y.sum())
    a /= (n * np.sum(X*X) - X.sum()*X.sum())
    b = (y.sum() - a*X.sum())/n
    print(f'trend coefficients a: {a}, b: {b}')
    #

    return {'a': a, 'b': b}

def AR_calc(dataset, column, period=12, start = 0, end = -1):
    """
    dataset - набор данных
    n - количество показателей, на которых будет происходить вычисление МНК
    name - название столбца
    name_2 - название модели работы. Если AR - то будет вычисляться Auto Regression
        Trend - будет вычисляться тренд
    start, end - месяц, начало и конец по которому будет моделироваться AR. И потом это разбивается на X_1, X_2
    """
    df = dataset[f'{column}'].copy()
    if end == -1:
        df = df.iloc[start::]
    else:
        df = df.iloc[start:end+1]
    X_1 = df.iloc[0:period].values
    X_2 = df.iloc[period:period*2].values
    n = period
    a = n * (np.sum(X_1*X_2)) - (np.sum(X_1)*np.sum(X_2))
    a /= (n * np.sum(X_1*X_1)) - (np.sum(X_1)*np.sum(X_2))
    b = (np.sum(X_2) - a*np.sum(X_1))/n
    print(f'AR coefficients a: {a}, b: {b}')
    return {'a': a, 'b': b}

def SMA(t=None, start=None, end=None, n=None, dataset=pd.DataFrame):
    """
    n: number of observed values for calculating SMA
    :return:
    """
    return 1 / n * np.sum(dataset[end-n:end:])

def correlation(dataset: pd.DataFrame, k=[], column='id', state_size=True):
    '''
    dataset: pd.DataFrame - ожидается датасет типа pd.DataFrame
    k1 - лаги которые необходимо посчитать
    column - колонка которую необходимо считать
    state_size = [True, False] - фиксировать размер колонки. Так как при смещении
    временных данных у нас будет уменьшаться размер выборки. Размер колонки фиксируется по последнему смещению
    '''
    df = dataset.copy()
    for i in k:
        df[f'{column}-{i}'] = df[column].shift(periods=i)
    if state_size:
        df.dropna(inplace=True)
    return df.corr().iloc[0,::].tolist()