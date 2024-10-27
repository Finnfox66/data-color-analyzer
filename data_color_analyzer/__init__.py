import sys
import numpy as np
import tkinter as tk
from tkinter import ttk
import colorsys as cs
from pyciede2000 import ciede2000
import random

from data_color_analyzer.colortools import colorconvert
from data_color_analyzer.viewtools import scrollframe, ui_sections
from data_color_analyzer.color_pipeline import ColorPipeline
from data_color_analyzer.color_generator import ColorGenerator

def helloWorld():
    print ("Hello world")

def generate():
    if len(sys.argv) <= 2:
        print('Not enough arguments. Command:\n')
        print ('\tpoetry run generate <generate_count> <initial_color_hex_1> [<inital_color_hex_2> ...]')
        print('\nExamples:\n')
        print ('\tpoetry run generate 3 "#0352fc"')
        print ('\tpoetry run generate 12 "#0352fc" "#fc03f0" "#39fc03"')
        print()
        return

    generate_count = int(sys.argv[1])
    initial_colors = []
    for idx in range(2, len(sys.argv)):
        h = sys.argv[idx].lstrip('#')
        initial_colors.append(tuple(int(h[i:i+2], 16) for i in (0, 2, 4)))

    print(f"Generate count: {generate_count}")
    print(f"Initial RGB colors: {initial_colors}")

    normalized_colors = list(map(lambda x: tuple(np.array(x)/255), initial_colors))
    print(f"Normalized RGB colors: {normalized_colors}")

    color_pipeline = ColorPipeline('Schmitz2015', 'ciede2000')
    color_generator = ColorGenerator(color_pipeline)

    colors = color_generator.generate_colors(normalized_colors, generate_count)

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

    testStringVar1 = tk.StringVar()

    colorAmount = tk.StringVar()
    colorAmount.set("5")

    colorPreviews = []
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
            # TODO CHECK IF NONE OF THESE IS ""
            h = float(colorHues[colorId].get())
            l = float(colorLightnesses[colorId].get())
            s = float(colorSaturations[colorId].get())
            hls = [h, l, s]
            return colorconvert.hls_to_rgb(hls)
        else:
            #hex
            # TODO CHECK IF NONE OF THESE IS ""
            return colorconvert.hex_to_rgb(colorCodes[colorId].get())
    
    def singleComparison(mon, di, tri, c1NormRgb, c2NormRgb):
        colorPipeline.set_color_blindness_levels(mon, di, tri)
        result = colorPipeline.get_color_difference(
            (c1NormRgb[0], c1NormRgb[1], c1NormRgb[2]),
            (c2NormRgb[0], c2NormRgb[1], c2NormRgb[2])
        )
        result = round(result, 2)
        return result

    def compareTwoColors(id1, id2):
        c1NormRgb = colorconvert.normalize_rgb(getRgbFromId(id1))
        c2NormRgb = colorconvert.normalize_rgb(getRgbFromId(id2))
        limit = float(minDifToOther.get())

        if (compareOrd.get() == 1):
            result = singleComparison(0, 0, 0, c1NormRgb, c2NormRgb)
            if (result < limit):
                result_text_col = colorconvert.convert_val_to_col_scale(result, 0, limit)
                conflictList.append([id1, id2, f"-", result, result_text_col])
        if (compareMono.get() == 1):
            result = singleComparison(1, 0, 0, c1NormRgb, c2NormRgb)
            if (result < limit):
                result_text_col = colorconvert.convert_val_to_col_scale(result, 0, limit)
                conflictList.append([id1, id2, f"Protanopia", result, result_text_col])
        if (compareDi.get() == 1):
            result = singleComparison(0, 1, 0, c1NormRgb, c2NormRgb)
            if (result < limit):
                result_text_col = colorconvert.convert_val_to_col_scale(result, 0, limit)
                conflictList.append([id1, id2, f"Deutranopia", result, result_text_col])
        if (compareTri.get() == 1):
            result = singleComparison(0, 0, 1, c1NormRgb, c2NormRgb)
            if (result < limit):
                result_text_col = colorconvert.convert_val_to_col_scale(result, 0, limit)
                conflictList.append([id1, id2, f"Tritanopia", result, result_text_col])

    #-------------------------------------------------
    # UI BUILD FUNCTIONS (maybe separate to another file)

    def createColorInputs():
        # TODO Include color block for all color deficiencies
        # TODO Needs function that stores old values first and restores them from old copies after.
        colorAmountInt = int(colorAmount.get())

        colorPreviews.clear()
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
                colorPreviews.append(tk.StringVar())
                colorPreviews[i].set("#ddd")
                colorCodes.append(tk.StringVar())
                colorToggles.append(tk.IntVar())
                colorHues.append(tk.StringVar())
                colorSaturations.append(tk.StringVar())
                colorLightnesses.append(tk.StringVar())
                
                ui_sections.UiSections.create_color_section(
                    colorFrame, colorPreviews[i], colorCodes[i], colorToggles[i],
                    colorHues[i], colorLightnesses[i], colorSaturations[i]
                )
                i += 1
    
    def populateHexes():
        for colorCode in colorCodes:
            if colorCode.get() == "":
                color = f"{random.randint(0, 0xFFFFFF):06x}"
                colorCode.set(color)

    def compare():
        for widget in resultFrame.winfo_children():
            widget.destroy()

        if (len(colorCodes) > 0 and float(minDifToOther.get()) > 0):
            conflictList.clear()
            # Compare all colors and find conflicts
            x = 0
            y = 0
            while (x < len(colorCodes)):
                while (y < len(colorCodes)):
                    if (x != y):
                        compareTwoColors(x, y)
                    y += 1
                x += 1
                # Set y so that same comparisons are not repeated.
                y = x
            
            # Sort the list of conflicts
            sortingList = []
            for conflict in conflictList:
                sortingList.append(conflict[3])
            sortedConflictList = [x for _,x in sorted(zip(sortingList,conflictList))]
            
            # Create the list of conflicts
            for conflict in sortedConflictList:
                col1Hex = colorconvert.rgb_to_hex(getRgbFromId(conflict[0]))
                col2Hex = colorconvert.rgb_to_hex(getRgbFromId(conflict[1]))
                ui_sections.UiSections.create_result_section(
                    resultFrame, windowWidth, col1Hex, col2Hex, conflict[2], conflict[3], conflict[4]
                )

    #-------------------------------------------------
    # UI

    infoFrame = ttk.Frame(windowFrame.scrollable_frame)
    infoFrame.pack(side='top', fill='x', padx=10, pady=(10, 0))
    tk.Button(infoFrame, text="Info", command=helloWorld).pack(side='left')

    textFrame1 = ttk.Frame(windowFrame.scrollable_frame)
    textFrame1.pack(side='top', fill='x', padx=10, pady=(5, 0))
    ttk.Label(textFrame1, text="--- Colors ---", style='Header.TLabel').pack(side='left')

    frame1 = ttk.Frame(windowFrame.scrollable_frame)
    frame1.pack(side='top', fill='x', padx=10, pady=(10, 0))
    ttk.Label(frame1, text="Amount of colors").pack(side='left')
    ttk.Entry(frame1, textvariable=colorAmount, width=10).pack(side='left')
    tk.Button(frame1, text="Reset", command=createColorInputs).pack(side='left', padx=(10, 0))
    tk.Button(frame1, text="Populate", command=populateHexes).pack(side='left', padx=(10, 0))
    ttk.Label(frame1, text="White #").pack(side='left', padx=(10, 0))
    ttk.Entry(frame1, textvariable=testStringVar1).pack(side='left')
    ttk.Label(frame1, text="Black #").pack(side='left', padx=(10, 0))
    ttk.Entry(frame1, textvariable=testStringVar1).pack(side='left')
    #ttk.Combobox(frame1 , state="readonly", values=["Python", "C", "C++", "Java"]).pack() 

    colorFrame = ttk.Frame(windowFrame.scrollable_frame)
    colorFrame.pack(side='top', fill='x')

    textFrame2 = ttk.Frame(windowFrame.scrollable_frame)
    textFrame2.pack(side='top', fill='x', padx=10, pady=(5, 0))
    ttk.Label(textFrame2, text="--- Comparisons ---", style='Header.TLabel').pack(side='left')

    frame2 = ttk.Frame(windowFrame.scrollable_frame)
    frame2.pack(side='top', fill='x', padx=10, pady=(5, 0))
    ttk.Label(frame2, text="Min difference to other (0-1)").pack(side='left')
    ttk.Entry(frame2, textvariable=minDifToOther, width=10).pack(side='left')
    ttk.Label(frame2, text="Min difference to white (0-1)").pack(side='left', padx=(10, 0))
    ttk.Entry(frame2, textvariable=testStringVar1, width=10).pack(side='left')
    ttk.Label(frame2, text="Min difference to black (0-1)").pack(side='left', padx=(10, 0))
    ttk.Entry(frame2, textvariable=testStringVar1, width=10).pack(side='left')

    frame3 = ttk.Frame(windowFrame.scrollable_frame)
    frame3.pack(side='top', fill='x', padx=10, pady=(5, 0))
    tk.Checkbutton(frame3, text="Ordinary",variable=compareOrd, onvalue=1, offvalue=0).pack(side='left')
    tk.Checkbutton(frame3, text="Protanopia",variable=compareMono, onvalue=1, offvalue=0).pack(side='left', padx=(10, 0))
    tk.Checkbutton(frame3, text="Deutranopia",variable=compareDi, onvalue=1, offvalue=0).pack(side='left', padx=(10, 0))
    tk.Checkbutton(frame3, text="Tritanopia",variable=compareTri, onvalue=1, offvalue=0).pack(side='left', padx=(10, 0))

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

    createColorInputs()

    root.mainloop()