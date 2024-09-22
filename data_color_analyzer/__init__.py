import tkinter as tk
from tkinter import ttk
import colorsys as cs
from pyciede2000 import ciede2000

from data_color_analyzer.colortools import colorconvert
from data_color_analyzer.viewtools import scrollframe
from data_color_analyzer.color_pipeline import ColorPipeline

def helloWorld():
    print ("Hello world")

def main():
    colorPipeline = ColorPipeline('Schmitz2015', 'ciede2000')

    #-------------------------------------------------
    # WINDOW

    root = tk.Tk()
    root.title('Data color analyzer')
    root.option_add('*tearOff', False) # This is always a good idea
    root.resizable(False, False) # the scrollable frame will look weird when resizing the window

    windowWidth = 800
    windowHeight = 600
    windowFrame = scrollframe.ScrollableFrame(root, width = windowWidth, height = windowHeight)
    windowFrame.pack()

    #-------------------------------------------------
    # CONTROL VARIABLES

    intVar1 = tk.IntVar()
    intVar2 = tk.IntVar()
    stringVar1 = tk.StringVar()
    onOff1 = tk.IntVar()
    onOff2 = tk.IntVar()
    onOff3 = tk.IntVar()

    #-------------------------------------------------
    # VIEW

    # TODO how about having individual buttons as class instances?

    s = ttk.Style()
    #s.configure('TFrame', background='#fff')
    s.configure('Frame1.TFrame', background='#ccc') # for inspecting frame edges with style='Frame1.TFrame'
    s.configure('Header.TLabel', font=('Segoe UI', 9, 'bold'))

    frame1 = ttk.Frame(windowFrame.scrollable_frame)
    frame1.pack(side='top', fill='x', padx=10, pady=(10, 0))
    tk.Button(frame1, text="Info", command=helloWorld).pack(side='left')
    ttk.Label(frame1, text="Amount of colors").pack(side='left', padx=(10, 0))
    ttk.Entry(frame1, textvariable=stringVar1, width=10).pack(side='left')
    ttk.Label(frame1, text="White #").pack(side='left', padx=(10, 0))
    ttk.Entry(frame1, textvariable=stringVar1).pack(side='left')
    ttk.Label(frame1, text="Black #").pack(side='left', padx=(10, 0))
    ttk.Entry(frame1, textvariable=stringVar1).pack(side='left')

    textFrame1 = ttk.Frame(windowFrame.scrollable_frame)
    textFrame1.pack(side='top', fill='x', padx=10, pady=(5, 0))
    ttk.Label(textFrame1, text="--- Colors ---", style='Header.TLabel').pack(side='left')

    colorFrame = ttk.Frame(windowFrame.scrollable_frame)
    colorFrame.pack(side='top', fill='x', padx=10, pady=(5, 0))
    ttk.Label(colorFrame, text="Color #").pack(side='left')
    ttk.Entry(colorFrame, textvariable=stringVar1).pack(side='left')
    tk.Checkbutton(colorFrame, text='OR',variable=onOff1, onvalue=1, offvalue=0, command=helloWorld).pack(side='left', padx=(10, 0))
    ttk.Label(colorFrame, text="Hue (0-240)").pack(side='left', padx=(10, 0))
    ttk.Entry(colorFrame, textvariable=stringVar1, width=10).pack(side='left')
    ttk.Label(colorFrame, text="Saturation %").pack(side='left', padx=(10, 0))
    ttk.Entry(colorFrame, textvariable=stringVar1, width=10).pack(side='left')
    ttk.Label(colorFrame, text="Lightness %").pack(side='left', padx=(10, 0))
    ttk.Entry(colorFrame, textvariable=stringVar1, width=10).pack(side='left')

    colorFrame = ttk.Frame(windowFrame.scrollable_frame)
    colorFrame.pack(side='top', fill='x', padx=10, pady=(5, 0))
    ttk.Label(colorFrame, text="Color #").pack(side='left')
    ttk.Entry(colorFrame, textvariable=stringVar1).pack(side='left')
    tk.Checkbutton(colorFrame, text='OR',variable=onOff1, onvalue=1, offvalue=0, command=helloWorld).pack(side='left', padx=(10, 0))
    ttk.Label(colorFrame, text="Hue (0-240)").pack(side='left', padx=(10, 0))
    ttk.Entry(colorFrame, textvariable=stringVar1, width=10).pack(side='left')
    ttk.Label(colorFrame, text="Saturation %").pack(side='left', padx=(10, 0))
    ttk.Entry(colorFrame, textvariable=stringVar1, width=10).pack(side='left')
    ttk.Label(colorFrame, text="Lightness %").pack(side='left', padx=(10, 0))
    ttk.Entry(colorFrame, textvariable=stringVar1, width=10).pack(side='left')

    textFrame2 = ttk.Frame(windowFrame.scrollable_frame)
    textFrame2.pack(side='top', fill='x', padx=10, pady=(5, 0))
    ttk.Label(textFrame2, text="--- Comparisons ---", style='Header.TLabel').pack(side='left')

    frame2 = ttk.Frame(windowFrame.scrollable_frame)
    frame2.pack(side='top', fill='x', padx=10, pady=(5, 0))
    ttk.Label(frame2, text="Min difference to generated").pack(side='left')
    ttk.Entry(frame2, textvariable=stringVar1, width=10).pack(side='left')
    ttk.Label(frame2, text="Min difference to white").pack(side='left', padx=(10, 0))
    ttk.Entry(frame2, textvariable=stringVar1, width=10).pack(side='left')
    ttk.Label(frame2, text="Min difference to black").pack(side='left', padx=(10, 0))
    ttk.Entry(frame2, textvariable=stringVar1, width=10).pack(side='left')

    frame3 = ttk.Frame(windowFrame.scrollable_frame)
    frame3.pack(side='top', fill='x', padx=10, pady=(5, 0))
    tk.Checkbutton(frame3, text="Ordinary",variable=onOff1, onvalue=1, offvalue=0, command=helloWorld).pack(side='left')
    tk.Checkbutton(frame3, text="Monochromatism",variable=onOff1, onvalue=1, offvalue=0, command=helloWorld).pack(side='left', padx=(10, 0))
    tk.Checkbutton(frame3, text="Dichromatism",variable=onOff1, onvalue=1, offvalue=0, command=helloWorld).pack(side='left', padx=(10, 0))
    tk.Checkbutton(frame3, text="Anomalous Trichromatism",variable=onOff1, onvalue=1, offvalue=0, command=helloWorld).pack(side='left', padx=(10, 0))

    frame4 = ttk.Frame(windowFrame.scrollable_frame)
    frame4.pack(side='top', fill='x', padx=10, pady=(5, 0))
    tk.Button(frame4, text="Review", command=helloWorld).pack(side='left')

    textFrame3 = ttk.Frame(windowFrame.scrollable_frame)
    textFrame3.pack(side='top', fill='x', padx=10, pady=(5, 0))
    ttk.Label(textFrame3, text="--- Results ---", style='Header.TLabel').pack(side='left')

    textFrame4 = ttk.Frame(windowFrame.scrollable_frame)
    textFrame4.pack(side='top', fill='x', padx=10, pady=(5, 0))
    ttk.Label(textFrame4, text="Overall score: 0.0, Highest: 0.0, Lowest: 0.0").pack(side='left')

    canvasFrame = ttk.Frame(windowFrame.scrollable_frame)
    canvasFrame.pack(side='top', fill='x', pady=(5, 0))
    canvas = tk.Canvas(canvasFrame, width = windowWidth, height = 60, bg='#ddd')
    canvas.create_rectangle(10, 0, 70, 60, fill = "#ccc", width = 0)
    canvas.create_rectangle(80, 0, 140, 60, fill = "#ccc", width = 0)
    canvas.pack(side='left')

    canvasFrame = ttk.Frame(windowFrame.scrollable_frame)
    canvasFrame.pack(side='top', pady=(5, 0))
    canvas = tk.Canvas(canvasFrame, width = windowWidth, height = 60, bg='#ddd')
    canvas.create_rectangle(10, 0, 70, 60, fill = "#ccc", width = 0)
    canvas.create_rectangle(80, 0, 140, 60, fill = "#ccc", width = 0)
    canvas.pack(side='left')

    #-------------------------------------------------
    # END

    root.mainloop()