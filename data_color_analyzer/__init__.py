import tkinter as tk
from tkinter import ttk
import colorsys as cs
from pyciede2000 import ciede2000

from data_color_analyzer.colortools import colorconvert
from data_color_analyzer.viewtools import scrollframe, ui_sections
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

    colorAmount = tk.StringVar()
    colorAmount.set("5")

    colorCodes = []
    colorToggles = []
    colorHues = []
    colorLightnesses = []
    colorSaturations = []

    minDifToOther = tk.StringVar()
    minDifToOther.set("0.15")

    compareOrd = tk.IntVar()
    compareOrd.set("1")
    compareMono= tk.IntVar()
    compareMono.set("1")
    compareDi = tk.IntVar()
    compareTri = tk.IntVar()

    # index 1, index 2, conflict text
    conflictList = []

    #-------------------------------------------------
    # STYLE

    s = ttk.Style()
    #s.configure('TFrame', background='#fff')
    s.configure('Frame1.TFrame', background='#ccc') # for inspecting frame edges with style='Frame1.TFrame'
    s.configure('Header.TLabel', font=('Segoe UI', 9, 'bold'))

    #-------------------------------------------------
    # COMPARISON CALC (maybe separate to another file)

    def getRgbFromId(colorId):
        if (colorToggles[colorId].get()):
            # hsl
            h = float(colorHues[colorId].get())
            l = float(colorLightnesses[colorId].get())
            s = float(colorSaturations[colorId].get())
            hls = [h, l, s]
            return colorconvert.hls_to_rgb(hls)
        else:
            #hex
            return colorconvert.hex_to_rgb(colorCodes[colorId].get())
    
    def singleComparison(mon, di, tri, c1NormRgb, c2NormRgb):
        colorPipeline.set_color_blindness_levels(mon, di, tri)
        return colorPipeline.get_color_difference(
            (c1NormRgb[0], c1NormRgb[1], c1NormRgb[2]),
            (c2NormRgb[0], c2NormRgb[1], c2NormRgb[2])
        )

    def compareTwoColors(id1, id2):
        c1NormRgb = colorconvert.normalize_rgb(getRgbFromId(id1))
        c2NormRgb = colorconvert.normalize_rgb(getRgbFromId(id2))
        limit = float(minDifToOther.get())

        if (compareOrd.get() == 1):
            result = singleComparison(0, 0, 0, c1NormRgb, c2NormRgb)
            if (result < limit):
                conflictList.append([id1, id2, f"ordinary {result}"])
        if (compareMono.get() == 1):
            result = singleComparison(1, 0, 0, c1NormRgb, c2NormRgb)
            if (result < limit):
                conflictList.append([id1, id2, f"mono {result}"])
        if (compareDi.get() == 1):
            result = singleComparison(0, 1, 0, c1NormRgb, c2NormRgb)
            if (result < limit):
                conflictList.append([id1, id2, f"di {result}"])
        if (compareTri.get() == 1):
            result = singleComparison(0, 0, 1, c1NormRgb, c2NormRgb)
            if (result < limit):
                conflictList.append([id1, id2, f"tri {result}"])

    #-------------------------------------------------
    # UI BUILD FUNCTIONS (maybe separate to another file)

    def createColorInputs():
        colorAmountInt = 0
        try:
            colorAmountInt = int(colorAmount.get())

            colorCodes.clear()
            colorToggles.clear()
            colorHues.clear()
            colorSaturations.clear()
            colorLightnesses.clear()

            for widget in colorFrame.winfo_children():
                widget.destroy()

            if (colorAmountInt > 0):
                i = 0
                while (i < colorAmountInt):
                    colorCodes.append(tk.StringVar())
                    colorToggles.append(tk.IntVar())
                    colorHues.append(tk.StringVar())
                    colorSaturations.append(tk.StringVar())
                    colorLightnesses.append(tk.StringVar())
                    
                    ui_sections.UiSections.create_color_section(
                        colorFrame, colorCodes[i], colorToggles[i],
                        colorHues[i], colorSaturations[i], colorLightnesses[i]
                    )
                    i += 1
        except ValueError:
            print("Generating color inputs failed")

    
    def compare():
        try:
            for widget in resultFrame.winfo_children():
                widget.destroy()

            if (len(colorCodes) > 0 and float(minDifToOther.get()) > 0):
                conflictList.clear()
                x = 0
                y = 0
                while (x < len(colorCodes)):
                    while (y < len(colorCodes)):
                        if (x != y):
                            compareTwoColors(x, y)
                        y += 1
                    y = 0
                    x += 1
                
                for conflict in conflictList:
                    col1Hex = colorconvert.rgb_to_hex(getRgbFromId(conflict[0]))
                    col2Hex = colorconvert.rgb_to_hex(getRgbFromId(conflict[1]))
                    ui_sections.UiSections.create_result_section(
                        resultFrame, windowWidth, col1Hex, col2Hex, conflict[2]
                    )
        except ValueError:
            print("Generating results failed")

    #-------------------------------------------------
    # UI

    frame1 = ttk.Frame(windowFrame.scrollable_frame)
    frame1.pack(side='top', fill='x', padx=10, pady=(10, 0))
    tk.Button(frame1, text="Info", command=helloWorld).pack(side='left')
    ttk.Label(frame1, text="Amount of colors").pack(side='left', padx=(10, 0))
    ttk.Entry(frame1, textvariable=colorAmount, width=10).pack(side='left')
    ttk.Label(frame1, text="White #").pack(side='left', padx=(10, 0))
    ttk.Entry(frame1, textvariable=stringVar1).pack(side='left')
    ttk.Label(frame1, text="Black #").pack(side='left', padx=(10, 0))
    ttk.Entry(frame1, textvariable=stringVar1).pack(side='left')
    tk.Button(frame1, text="Update", command=createColorInputs).pack(side='left', padx=(10, 0))
    #ttk.Combobox(frame1 , state="readonly", values=["Python", "C", "C++", "Java"]).pack() 

    textFrame1 = ttk.Frame(windowFrame.scrollable_frame)
    textFrame1.pack(side='top', fill='x', padx=10, pady=(5, 0))
    ttk.Label(textFrame1, text="--- Colors ---", style='Header.TLabel').pack(side='left')

    colorFrame = ttk.Frame(windowFrame.scrollable_frame)
    ttk.Label(colorFrame, text="// Define the amount of colors and press the Update-button.").pack(side='left', padx=(10, 0))
    colorFrame.pack(side='top', fill='x')

    textFrame2 = ttk.Frame(windowFrame.scrollable_frame)
    textFrame2.pack(side='top', fill='x', padx=10, pady=(5, 0))
    ttk.Label(textFrame2, text="--- Comparisons ---", style='Header.TLabel').pack(side='left')

    frame2 = ttk.Frame(windowFrame.scrollable_frame)
    frame2.pack(side='top', fill='x', padx=10, pady=(5, 0))
    ttk.Label(frame2, text="Min difference to other (0-1)").pack(side='left')
    ttk.Entry(frame2, textvariable=minDifToOther, width=10).pack(side='left')
    ttk.Label(frame2, text="Min difference to white (0-1)").pack(side='left', padx=(10, 0))
    ttk.Entry(frame2, textvariable=stringVar1, width=10).pack(side='left')
    ttk.Label(frame2, text="Min difference to black (0-1)").pack(side='left', padx=(10, 0))
    ttk.Entry(frame2, textvariable=stringVar1, width=10).pack(side='left')

    frame3 = ttk.Frame(windowFrame.scrollable_frame)
    frame3.pack(side='top', fill='x', padx=10, pady=(5, 0))
    tk.Checkbutton(frame3, text="Ordinary",variable=compareOrd, onvalue=1, offvalue=0).pack(side='left')
    tk.Checkbutton(frame3, text="Monochromatism",variable=compareMono, onvalue=1, offvalue=0).pack(side='left', padx=(10, 0))
    tk.Checkbutton(frame3, text="Dichromatism",variable=compareDi, onvalue=1, offvalue=0).pack(side='left', padx=(10, 0))
    tk.Checkbutton(frame3, text="Anomalous Trichromatism",variable=compareTri, onvalue=1, offvalue=0).pack(side='left', padx=(10, 0))

    frame4 = ttk.Frame(windowFrame.scrollable_frame)
    frame4.pack(side='top', fill='x', padx=10, pady=(5, 0))
    tk.Button(frame4, text="Review", command=compare).pack(side='left')

    textFrame3 = ttk.Frame(windowFrame.scrollable_frame)
    textFrame3.pack(side='top', fill='x', padx=10, pady=(5, 0))
    ttk.Label(textFrame3, text="--- Results ---", style='Header.TLabel').pack(side='left')

    textFrame4 = ttk.Frame(windowFrame.scrollable_frame)
    textFrame4.pack(side='top', fill='x', padx=10, pady=(5, 0))
    ttk.Label(textFrame4, text="Overall score: 0.0, Highest: 0.0, Lowest: 0.0").pack(side='left')

    resultFrame = ttk.Frame(windowFrame.scrollable_frame)
    resultFrame.pack(side='top', fill='x')

    #-------------------------------------------------
    # END

    root.mainloop()