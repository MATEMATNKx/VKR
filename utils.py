import numpy as np
import pandas as pd
from plot import plot

def modern(entity):
    dataset = entity.df.copy()
    S = 1 * dataset.iloc[0, 0] / 100
    S_ = [S]
    for i in range(1, dataset.shape[0]):
        S_.append(S_[i - 1] * dataset.iloc[i, 0] / 100)
    entity.set_df(pd.DataFrame(S_, columns=dataset.columns))
    #print(pd.Series(S_)



def line_trend(entity, dataset=None, name=0 , i=0, start = 0, end = -1, label = None):
    """
    i - по какому столбцу вычислить тренд. Индекс от 0 (счет колонок идёт с нуля)
    dataset - набор данных
    n - количество показателей, на которых будет происходить вычисление МНК
    start, end - начало и конец включительно, номер месяца как m*k, где m - месяц года, k-год
    """
    if dataset ==None:
        df = entity.df.copy()
    else:
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
    cache = entity.cache.copy()
    cache['tr_a'] = a
    cache['tr_b'] = b
    entity.set_cache(cache=cache, info_label=label)
    entity.trend=True
    #return {'a': a, 'b': b}
def line_trend_minus(entity, info_label, btn):
    if entity.ts_not_trend:
        entity.ts_not_trend = False
        btn['text'] = "Построить остаток временного ряда"
    else:
        entity.ts_not_trend = True
        btn['text'] = "Убрать остаток временного ряда"
    entity.set_cache(entity.cache, info_label=info_label)
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
    return 1 / n * np.sum(dataset.values[t-n:t:])

def SMA_calc(entity, n, info_label, not_trend = False):
    """
    not_trend = True - взять датасет без тренда и построить на нём SMA
    Аналогично и на оборот
    ----
    v2 версия (В будущем)
    SMA для изначального ряда будет вычисляться  как SMA для остатка + trend
    ----
    """
    if not_trend:
        df = entity.ts_not_trend_df.copy()
    else:
        df = entity.df.copy()
    sma_list = []
    if entity.SMA:
        entity.SMA = False
    else:
        entity.SMA = True
    for i in range(n, df.shape[0]):
        sma_list.append(SMA(t=i, n=n, dataset=df))
    entity.SMA_list = sma_list
    cache = entity.cache.copy()
    cache["sma_n"] = int(n)
    entity.set_cache(cache, info_label=info_label)

def correlation(entity, k=[], column=None, state_size=True, label = None):
    '''
    dataset: pd.DataFrame - ожидается датасет типа pd.DataFrame
    k1 - лаги которые необходимо посчитать
    column - колонка которую необходимо считать
    state_size = [True, False] - фиксировать размер колонки. Так как при смещении
    временных данных у нас будет уменьшаться размер выборки. Размер колонки фиксируется по последнему смещению
    '''
    df = entity.df.copy()
    if column ==None:
        column=df.columns.tolist()[0]
    for i in k:
        df[f'{column}-{i}'] = df[column].shift(periods=i)
    if state_size:
        df.dropna(inplace=True)

    cache = entity.cache.copy()
    correl_vac = {}
    _ = df.corr().iloc[0,::].tolist()
    for i in range(1, len(_)):
        correl_vac[f'k_{i}'] = _[i]
    cache["correlation_info"] = correl_vac
    cache["best_correlation"] = list(correl_vac.keys())[list(correl_vac.values()).index(max(_[1::]))]
    entity.set_cache(cache=cache, info_label=label)