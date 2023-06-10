from matplotlib.figure import Figure
from tkinter.ttk import Frame
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
import pandas as pd

def plot(root, dataset):
    # the figure that will contain the plot
    fig = Figure(figsize=(10, 5),
                 dpi=100)

    # list of squares
    y = [i ** 32 for i in range(101)]

    # adding the subplot
    plot1 = fig.add_subplot(111)

    # plotting the graph
    plot1.plot(dataset)
    '''
    print(type(dataset))
    if type(dataset) == "<class 'pandas.core.frame.DataFrame'>":
        plot1.plot(dataset)
    else:
        plot1.plot(y)
    '''
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
