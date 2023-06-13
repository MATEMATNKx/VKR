from tkinter import Tk, BOTH
from tkinter.ttk import Frame, Button, Style, Label, Entry
from tkinter import Text,  NSEW
from plot import plot
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
import os
from utils import modern, line_trend, correlation, line_trend_minus, SMA_calc, shape_of_df, AR_calc
import json

class Example(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title("Визуализатор")
        self.pack(fill=BOTH, expand=1)
        self.centerWindow()
        self.modern_status = False
        self.cache = {}
        self.trend = False
        self.trend_settings = []
        self.ts_not_trend = False
        self.SMA = False
        self.trend_values = None
        self.ts_not_trend_df = None
        self.SMA_list = []
        self.df_reserv = None #Запоминаем датасет
        self.AR = False
    def centerWindow(self):
        w = 1000
        h = 800

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

        choose_csv_button = Button(self, text="Выбрать файл", command=self.choose_file)
        choose_csv_button.grid(row=2, column=0)

        modern_ts_button = Button(self, text="Преобразовать временной ряд", command=lambda: modern(entity=self))
        modern_ts_button.grid(row=3, column=0)

        trend_ts_button = Button(self, text='Построить линейный тренд',
                                 command=lambda:
                                 line_trend(entity=self, label=info_label, start=int(trend_from.get()), end=int(trend_to.get())))
        trend_ts_button.grid(row=4, column=0)



        trend_from = Entry(self)
        trend_from.grid(row=6, column=0)
        trend_to = Entry(self)
        trend_to.grid(row=7, column=0)

        label_trend = Label(self, text="Промежуток вычисления тренда по примеру [от:до]\n[0:-1] - на всём промежутке")
        label_trend.grid(row=5,column=0)



        trend_ts_minus_button = Button(self, text='Построить временной ряд без тренда',
                                       command=lambda: line_trend_minus(entity=self, info_label=info_label,
                                                                        btn=trend_ts_minus_button))
        trend_ts_minus_button.grid(row=8, column=0)



        info_label = Label(self, text=f"Информация о временном ряде:")
        info_label.grid(row=1, column=3)

        corr_to = Entry(self)
        corr_to.grid(row=1, column=2)
        button_corr = Button(self, text="Вычислить корреляцию для k",
                             command=lambda: correlation(entity=self,k=[i for i in range(1, int(corr_to.get())+1)],
                                                 state_size=True,label=info_label))
        button_corr.grid(row=2, column=2)

        button_sma = Button(self, text= "Построить SMA для изначального ряда",
                            command= lambda: SMA_calc(entity=self, n=int(n_SMA.get()), info_label=info_label))
        button_sma.grid(row=3, column=2)
        button_sma_ost = Button(self, text="Построить SMA для остатка",
                            command=lambda: SMA_calc(entity=self, n=int(n_SMA.get()),
                                                     info_label=info_label, not_trend=True))
        button_sma_ost.grid(row=4, column=2)

        n_SMA_label = Label(self, text="Количество периодов для построения SMA")
        n_SMA_label.grid(row=5, column=2)
        n_SMA = Entry(self)
        n_SMA.grid(row=6, column=2)
        button_shape_of_df = Button(self, text='Рассмотреть промежуток временного ряда',
                                    command=lambda : shape_of_df(self, start=int(shape_from.get()),
                                                                 end=int(shape_to.get()), info_label=info_label))
        button_shape_of_df.grid(row=7, column=2)
        shape_from = Entry(self)
        shape_from.grid(row=8, column=2)
        shape_to = Entry(self)
        shape_to.grid(row=9, column=2)

        AR_period_label = Label(self, text="Количество периодов для построения AR")
        AR_period_label.grid(row=2,column=3)
        AR_period = Entry(self)
        AR_period.grid(row=4, column=3)
        AR_period_label = Label(self, text="Промежуток построения и прогноза модели AR")
        AR_period_label.grid(row=5, column=3)
        AR_start = Entry(self)
        AR_start.grid(row=6, column=3)
        AR_end = Entry(self)
        AR_end.grid(row=7, column=3)
        button_AR = Button(self, text="Построить AR",
                            command=lambda: AR_calc(entity=self,
                                                    period=int(AR_period.get()),
                                                    start=int(AR_start.get()),
                                                    end=int(AR_end.get()),
                                                    info_label=info_label))
        button_AR.grid(row=8, column=3)


    def choose_file(self, event=None):
        filename = filedialog.askopenfilename()
        if filename.endswith('csv'):
            self.parent.title(os.path.split(filename)[1])
            self.df = pd.read_csv(filename)
            plot(self, dataset=self.df)
    def set_df(self, df):
        if self.modern_status != True:
            self.df = df
            plot(self, dataset=self.df)
            self.update()
            self.modern_status = True
        else:
            pass
    def set_cache(self, cache, info_label):
        self.cache = cache
        if self.cache['tr_a'] and self.cache['tr_b']:
            self.trend = True
        info_label['text'] = "Информация о временном ряде:\n" + str(json.dumps(self.cache, default=lambda o: o.__dict__, indent=4))
        plot(self, dataset=self.df)
        self.update()
        print(self.cache)


def main():
    root = Tk()
    ex = Example(root)
    root.mainloop()


if __name__ == '__main__':
    main()