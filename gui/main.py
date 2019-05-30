from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from tkinter.ttk import *
from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import itertools
import math

WIDTH = 1000
HEIGHT = 600

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.tab_control = Notebook(self.master)
        self.fontSizes = itertools.cycle([8, 16, 24, 32])
        self.s = Style()
        self.s.configure('TNotebook.Tab', font=('URW Gothic L','11'))
        self.init_window()

    def init_window(self):
        self.master.title('Antenna & Propagation')
        self.tab1 = Frame(self.tab_control)
        self.tab2 = Frame(self.tab_control)
        self.tab3 = Frame(self.tab_control)

        # Tab 1

        self.plot_free_space()
        self.radio = IntVar()
        optionHata = Radiobutton(self.tab1, text="Hata Model", value=2, variable=self.radio, bg='white', command=self.set_calculation_mode)
        optionFreeSpace = Radiobutton(self.tab1, text="Free Space", value=1, variable=self.radio, bg='white', command=self.set_calculation_mode)

        distanceLabel = Label(self.tab1, text="Distance", bg='white')
        self.distanceInput = Entry(master=self.tab1)
        distanceMetricLabel = Label(self.tab1, text=" Km", bg='white')

        frequencyLabel = Label(self.tab1, text="Carrier Frequency", bg='white')
        self.frequencyInput = Entry(master=self.tab1)
        frequencyMetricLabel = Label(self.tab1, text=" MHz", bg='white')

        antenna1Label = Label(self.tab1, text="Antenna 1 Height", bg='white')
        self.antenna1Input = Entry(master=self.tab1)
        antenna1MetricLabel = Label(self.tab1, text=" meters", bg='white')

        antenna2Label = Label(self.tab1, text="Antenna 2 Height", bg='white')
        self.antenna2Input = Entry(master=self.tab1)
        antenna2MetricLabel = Label(self.tab1, text=" meters", bg='white')

        self.plotButton = Button(self.tab1, text="Plot", state=DISABLED, command=lambda:self.plot())

        self.hataWidgets = [antenna1Label, self.antenna1Input, antenna1MetricLabel, antenna2Label, self.antenna2Input, antenna2MetricLabel]
        self.defaultWidgets = [optionHata, optionFreeSpace, distanceLabel, self.distanceInput, distanceMetricLabel, frequencyLabel, frequencyInput, frequencyMetricLabel, self.plotButton]
        self.widgetsGrid = {distanceLabel: (3, 3), self.distanceInput: (3, 4), distanceMetricLabel: (3, 5),
                            frequencyLabel: (4, 3), self.frequencyInput: (4, 4), frequencyMetricLabel: (4, 5),
                            antenna1Label: (5, 3), self.antenna1Input: (5, 4), antenna1MetricLabel: (5, 5),
                            antenna2Label: (6, 3), self.antenna2Input: (6, 4), antenna2MetricLabel: (6, 5),
                            self.plotButton: (6, 4), optionHata: (2, 4), optionFreeSpace: (2, 3)
        }

        self.show_widgets(self.defaultWidgets)

        # Tab 2
        
        fig = Figure(figsize=(4, 5), dpi=100)
        fig.add_subplot(111).plot(self.get_results_tab_2())

        canvas = FigureCanvasTkAgg(fig, master=self.tab2)
        canvas.draw()
        canvas.get_tk_widget().pack(side=LEFT, fill=BOTH, expand=1)

        # Tab 3

        t1 = np.arange(0.0, 5.0, 0.1)
        t2 = np.arange(0.0, 5.0, 0.02)
        t3 = np.arange(0.0, 2.0, 0.01)

        fig3, axs3 = plt.subplots(2, 1, constrained_layout=True)
        axs3[0].plot(t1, self.function(t1), 'o', t2, self.function(t2), '-')
        axs3[0].set_title('subplot 1')
        axs3[0].set_xlabel('distance (m)')
        axs3[0].set_ylabel('Damped oscillation')
        fig3.suptitle('Non models:', fontsize=16)

        axs3[1].plot(t3, np.cos(2 * np.pi * t3), '--')
        axs3[1].set_xlabel('time (s)')
        axs3[1].set_title('subplot 2')
        axs3[1].set_ylabel('Undamped')

        canvas3 = FigureCanvasTkAgg(fig3, master=self.tab3)
        canvas3.draw()
        canvas3.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        self.tab_control.add(self.tab1, text=' Outdoor Models ')
        self.tab_control.add(self.tab2, text=' Indoor Models ')
        self.tab_control.add(self.tab3, text=' About ')

        self.tab_control.pack(expand=1, fill='both')
        self.tab1.configure(bg='white')
        self.tab2.configure(bg='white')
        self.tab3.configure(bg='white')

    def get_results_tab_2(self):
        d = np.array([1, 2, 3, 4, 5])
        hb = 30
        hm = 2
        fc = 900
        W = 15
        b = 30
        phi = 90
        hr = 30
        dellhm = hr - hm
        Lf= 32.4 + 20 * np.log10(d) + 20 * np.log10(fc)
        L0= 4 - 0.114 * (phi - 55)
        Lrts = -16.9 - 10 * math.log10(W) + 10 * math.log10(fc) + 20 * math.log10(dellhm) + L0
        Lbsh = -18 * math.log10(11)
        ka =54 - 0.8 * hb
        dellhb = hb - hr
        kd= 18 - 15 * dellhb / dellhm
        kf = 4 + 0.7 * (fc / 925 - 1)
        Lms = Lbsh + ka + kd * np.log10(d) + kf * np.log10(fc) - 9 * np.log10(b)
        L50 = np.array([0, 0, 0, 0, 0])
        L50 = Lf + Lrts + Lms
        return L50

    def plot_hata(self, frequency=None, distance=None, antenna1=None, antenna2=None):
        pass

    def plot_free_space(self, frequency=None, distance=None):
        fig2, axs2 = plt.subplots(1, 1)

        if frequency and distance:
            arrayFree, L50 = self.get_results_free_space(int(frequency), int(distance))
            axs2.plot(arrayFree, L50)
            axs2.set_title('Free Space loss')
            axs2.set_xlabel('Distance (km)')
            axs2.set_ylabel('Path Loss (db)')
            axs2.grid(True)
            fig2.suptitle('Outdoor Propagation models:', fontsize=14)
        else:
            axs2.plot()

        canvas = FigureCanvasTkAgg(fig2, master=self.tab1)
        canvas.get_tk_widget().grid(row=0, column=0, columnspan=3, rowspan=20)
        canvas.draw()

    def get_results_free_space(self, frequency, distance):
        arrayFree = []
        step = 1 if int(distance * 0.1) < 1 else int(distance * 0.1)

        for i in range(distance - 3 * step, distance + 4 * step, step):
            arrayFree.append(i)
        arrayFree = np.array(arrayFree)

        factor1 = 20 * np.log10(arrayFree)
        factor2 = 20 * math.log10(frequency)
        factor3 = 32.45
        L50 = -factor1 - factor2 - factor3

        return arrayFree, L50

    def hide_widgets(self, widgets):
        for widget in widgets:
            self.hide_widget(widget)

    def hide_widget(self, widget):
        widget.grid_forget()

    def show_widgets(self, widgets):
        for widget in widgets:
            self.show_widget(widget)

    def show_widget(self, widget):
        row_num, col_num = self.widgetsGrid[widget]
        widget.grid(row=row_num, column=col_num)

    def function(self, t):
        s1 = np.cos(2 * np.pi * t)
        e1 = np.exp(-t)
        return s1 * e1

    def set_calculation_mode(self):
        switcher = {
            1: 'free space',
            2: 'hata'
        }

        self.calculation_mode = switcher.get(self.radio.get(), None)

        if self.calculation_mode:
            self.plotButton.config(state='normal')

            if self.calculation_mode == 'hata':
                self.show_widgets(self.hataWidgets)
                self.plotButton.grid(row=8, column=4)
                self.widgetsGrid[self.plotButton] = (8, 4)
            else:
                self.hide_widgets(self.hataWidgets)
                self.plotButton.grid(row=6, column=4)
                self.widgetsGrid[self.plotButton] = (6, 4)

    def plot(self):
        if self.calculation_mode == 'hata':
            self.plot_hata(self.frequencyInput.get(), self.distanceInput.get(), self.antenna1Input.get(), self.antenna2Input.get())
        else:
            self.plot_free_space(self.frequencyInput.get(), self.distanceInput.get())
    
root = Tk()
root.geometry(f'{WIDTH}x{HEIGHT}')
app = Window(root)
root.mainloop()
