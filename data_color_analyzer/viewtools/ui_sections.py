import tkinter as tk
from tkinter import ttk

class UiSections():

    def create_color_section(frame, code, toggle, hue, saturation, lightness):
        colorFrame = ttk.Frame(frame)
        colorFrame.pack(side='top', fill='x', padx=10, pady=(5, 0))
        ttk.Label(colorFrame, text="Color #").pack(side='left')
        ttk.Entry(colorFrame, textvariable=code).pack(side='left')
        tk.Checkbutton(colorFrame, text='OR',variable=toggle, onvalue=1, offvalue=0).pack(side='left', padx=(10, 0))
        ttk.Label(colorFrame, text="Hue (0-240)").pack(side='left', padx=(10, 0))
        ttk.Entry(colorFrame, textvariable=hue, width=10).pack(side='left')
        ttk.Label(colorFrame, text="Lightness %").pack(side='left', padx=(10, 0))
        ttk.Entry(colorFrame, textvariable=lightness, width=10).pack(side='left')
        ttk.Label(colorFrame, text="Saturation %").pack(side='left', padx=(10, 0))
        ttk.Entry(colorFrame, textvariable=saturation, width=10).pack(side='left')
    
    def create_result_section(frame, windowWidth, col1Hex, col2Hex, text):
        col1Hex = "#" + col1Hex
        col2Hex = "#" + col2Hex
        resultFrame = ttk.Frame(frame)
        resultFrame.pack(side='top', fill='x', pady=(5, 0))
        canvas = tk.Canvas(resultFrame, width = windowWidth, height = 60, bg='#ddd')
        canvas.create_rectangle(10, 0, 70, 60, fill = col1Hex, width = 0)
        canvas.create_rectangle(80, 0, 140, 60, fill = col2Hex, width = 0)
        canvas.create_text(150, 24, text=text, fill="black", font=('Segoe_UI 9 bold'), anchor=tk.NW)
        canvas.pack(side='left')