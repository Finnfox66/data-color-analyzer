from subpackage import *
mymodule = module.Module()
hello = mymodule.testfunc()
print(hello)

import tkinter as tk
from tkinter import ttk
import colorsys as cs
from pyciede2000 import ciede2000

root = tk.Tk()
root.title("Data color analyzer")
root.option_add("*tearOff", False) # This is always a good idea


### CONTROL VARIABLES ###

# Create control variables

intVar1 = tk.IntVar()
intVar2 = tk.IntVar()
stringVar1 = tk.StringVar()

# TODO how about having individual buttons as class instances?

# res = ciede2000((50.0000,2.6772,-79.7751), (50.0000,0.0000,-82.7485))
# print(res)