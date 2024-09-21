import tkinter as tk
from tkinter import ttk
import colorsys as cs
from pyciede2000 import ciede2000

from colortools import pyciede, colorconvert
from viewtools import scrollframe

myPyciede = pyciede
myPyciede.test()

root = tk.Tk()
root.title('Data color analyzer')
root.option_add('*tearOff', False) # This is always a good idea

#-------------------------------------------------
# VIEW

frame = scrollframe.ScrollableFrame(root)


### CONTROL VARIABLES ###

# Create control variables

intVar1 = tk.IntVar()
intVar2 = tk.IntVar()
stringVar1 = tk.StringVar()

# TODO how about having individual buttons as class instances?

# res = ciede2000((50.0000,2.6772,-79.7751), (50.0000,0.0000,-82.7485))
# print(res)



innerFrame = ttk.Frame(frame.scrollable_frame, padding=(5, 5))
innerFrame.grid(row=1, column=0, padx=(5, 5), pady=(5, 5), sticky="nsew")

ttk.Label(innerFrame, text="test").grid(row=0, column=0, padx=0, pady=(0, 10), sticky="ew")
ttk.Entry(innerFrame, textvariable=stringVar1).grid(row=0, column=1, padx=10, pady=(0, 10), sticky="ew")

ttk.Label(innerFrame, text="test").grid(row=0, column=2, padx=0, pady=(0, 10), sticky="ew")
ttk.Entry(innerFrame, textvariable=stringVar1).grid(row=0, column=3, padx=10, pady=(0, 10), sticky="ew")

#-------------------------------------------------
# END

frame.pack()
root.mainloop()