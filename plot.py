from matplotlib.figure import Figure
from tkinter.ttk import Frame
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
import pandas as pd
import numpy as np
def plot(root, dataset=None):
    # the figure that will contain the plot
    fig = Figure(figsize=(10, 5),
                 dpi=100)

    # list of squares
    y = [i ** 32 for i in range(101)]

    # adding the subplot
    plot1 = fig.add_subplot(111)

    # plotting the graph
    if type(dataset)!=pd.DataFrame:
        plot1.plot(y)
    else:
        plot1.plot(np.arange(dataset.shape[0]), dataset.values, label="Изначальный временной ряд")

    plot1.set_title(dataset.columns.tolist()[0])
    plot1.set_xlabel("Временной интервал")

    if root.trend:
        root.trend_values = pd.DataFrame(root.cache["tr_a"] * np.arange(dataset.shape[0]) + root.cache['tr_b'],
                                         columns=dataset.columns)
        plot1.plot(np.arange(dataset.shape[0]), root.trend_values.values, label="Тренд временного ряда")
    if root.ts_not_trend:
        root.ts_not_trend_df = pd.DataFrame([dataset.values[i].tolist()[0] - root.trend_values.values[i].tolist()[0] for i in range(dataset.shape[0])],
                                columns = dataset.columns)
        plot1.plot(np.arange(dataset.shape[0]), root.ts_not_trend_df.values,
                   label="Ряд остатков")

    if root.SMA:
        plot1.plot(np.arange(root.cache["sma_n"], dataset.shape[0]), root.SMA_list,
                   label="SMA")
    if root.AR:
        model = pd.DataFrame(
            root.cache["AR_a"] * root.ts_not_trend_df[
                                 root.cache["AR_start"] + root.cache["AR_period"]:root.cache["AR_end"]].values +
            root.cache["AR_b"],
            columns=dataset.columns)

        model_tr = model.values.ravel() + root.cache["tr_a"] * np.arange(
            root.cache["AR_start"] + root.cache["AR_period"],
            root.cache["AR_end"]) + root.cache["tr_b"]

        plot1.plot(np.arange(root.cache["AR_start"] + root.cache["AR_period"],
                             root.cache["AR_end"]),
                   model_tr, label='Моделируемые значения')

        forecast = root.cache["AR_a"] * model.values.ravel()+\
                   root.cache["AR_b"] + \
                   root.cache['tr_a'] * np.arange(root.cache["AR_start"]+root.cache["AR_period"]+\
                                                  root.cache["AR_period"],
                                                  root.cache["AR_end"] + root.cache["AR_period"]) +root.cache['tr_b']
        plot1.plot(np.arange(root.cache["AR_start"]+root.cache["AR_period"]+\
                                                  root.cache["AR_period"],
                                                  root.cache["AR_end"] + root.cache["AR_period"]),
                   forecast, label="Предсказанные значения")

    plot1.legend()

    plot1.grid()
    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig,
                               master=root)
    canvas.draw()
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().grid(row=2, column=0)
    frame = Frame(root)
    frame.grid(row=0, column=1)
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas,
                                   frame)
    toolbar.update()

    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().grid(row=1, column=0)
