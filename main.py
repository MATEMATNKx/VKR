from tkinter import Tk, BOTH
from tkinter.ttk import Frame, Button, Style
from plot import plot
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
import os

class Example(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title("Визуализатор")
        self.pack(fill=BOTH, expand=1)
        self.centerWindow()

    def centerWindow(self):
        w = 500
        h = 300

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))
        #plot(self, dataset=None)
        quitButton = Button(self, text="Закрыть окно", command=self.quit)
        choose_csv = Button(self, text="Выбрать файл", command=self.choose_file)
        choose_csv.grid(row=2, column=0)
        #quitButton.grid(row=2, column=0)
    def choose_file(self, event=None):
        filename = filedialog.askopenfilename()
        if filename.endswith('csv'):
            self.parent.title(os.path.split(filename)[1])
            df = pd.read_csv(filename)
            plot(self, dataset=df)
            #self.update()
        print('Selected:', df)
def main():
    root = Tk()
    ex = Example(root)
    root.mainloop()


if __name__ == '__main__':
    main()