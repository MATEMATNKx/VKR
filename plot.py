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
    if type(dataset)==None:
        plot1.plot(y)
    else:
        plot1.plot(dataset, label="Изначальный временной ряд")

    plot1.set_title(dataset.columns.tolist()[0])
    plot1.set_xlabel("Временной интервал")
    print(dataset.columns)

    if root.trend:
        root.trend_values = pd.DataFrame(root.cache["tr_a"] * np.arange(dataset.shape[0]) + root.cache['tr_b'],
                                         columns=dataset.columns)
        plot1.plot(np.arange(dataset.shape[0]), root.trend_values.values, label="Тренд временного ряда")

    if root.ts_not_trend:
        root.ts_not_trend_df = pd.DataFrame([dataset.values[i] - root.trend_values.values[i] for i in range(dataset.shape[0])],
                                columns = dataset.columns)
        plot1.plot(np.arange(dataset.shape[0]), root.ts_not_trend_df.values,
                   label="Остаток временного ряда")

    if root.SMA:
        plot1.plot(np.arange(root.cache["sma_n"], dataset.shape[0]), root.SMA_list,
                   label="SMA")


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
