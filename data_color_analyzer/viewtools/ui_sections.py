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
        ttk.Label(colorFrame, text="Saturation %").pack(side='left', padx=(10, 0))
        ttk.Entry(colorFrame, textvariable=saturation, width=10).pack(side='left')
        ttk.Label(colorFrame, text="Lightness %").pack(side='left', padx=(10, 0))
        ttk.Entry(colorFrame, textvariable=lightness, width=10).pack(side='left')