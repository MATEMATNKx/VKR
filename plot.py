from matplotlib.figure import Figure
from tkinter.ttk import Frame
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
import pandas as pd
import numpy as np
def plot(root, dataset):
    # the figure that will contain the plot
    fig = Figure(figsize=(10, 5),
                 dpi=100)

    # list of squares
    y = [i ** 32 for i in range(101)]

    # adding the subplot
    plot1 = fig.add_subplot(111)

    # plotting the graph
    plot1.plot(dataset, label="Изначальный временной ряд")
    plot1.set_title(dataset.columns.tolist()[0])
    plot1.set_xlabel("Временной интервал")
    print(dataset.columns)

    if root.trend:
        trend = root.cache["tr_a"] * np.arange(dataset.shape[0]) + root.cache['tr_b']
        plot1.plot(np.arange(dataset.shape[0]), trend, label="Тренд временного ряда")

    print(root.ts_not_trend)
    if root.ts_not_trend:
        plot1.plot(np.arange(dataset.shape[0]), [dataset.values[i] - trend[i] for i in range(dataset.shape[0])],
                   label="Остаток временного ряда")

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
