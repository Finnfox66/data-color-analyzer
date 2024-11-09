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
    print ('Hello world')

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
    color_pipeline = ColorPipeline('Schmitz2015', 'ciede2000')

    #-------------------------------------------------
    # WINDOW

    root = tk.Tk()
    root.title('Data color analyzer')
    root.option_add('*tearOff', False) # This is always a good idea
    root.resizable(False, False) # the scrollable frame will look weird when resizing the window

    window_width = 800
    window_height = 600
    window_frame = scrollframe.ScrollableFrame(root, width = window_width, height = window_height)
    window_frame.pack()

    #-------------------------------------------------
    # CONTROL VARIABLES

    color_amount = tk.StringVar()
    color_amount.set('5')

    color_white = tk.StringVar()
    color_white.set('ffffff')
    color_black = tk.StringVar()
    color_black.set('000000')

    color_previews = []
    color_codes = []
    color_toggles = []
    color_hues = []
    color_lightnesses = []
    color_saturations = []

    min_dif = tk.StringVar()
    min_dif.set('0.15')
    min_dif_to_white = tk.StringVar()
    min_dif_to_black = tk.StringVar()

    compare_ord = tk.IntVar()
    compare_ord.set('1')
    compare_mono= tk.IntVar()
    compare_mono.set('1')
    compare_di = tk.IntVar()
    compare_tri = tk.IntVar()

    # index 1, index 2, conflict text
    conflict_list = []
    failure_list = []

    #-------------------------------------------------
    # STYLE

    s = ttk.Style()
    #s.configure('TFrame', background='#fff')
    s.configure('Frame1.TFrame', background='#ccc') # for inspecting frame edges with style='Frame1.TFrame'
    s.configure('Header.TLabel', font=('Segoe UI', 9, 'bold'))

    #-------------------------------------------------
    # COMPARISON CALC (maybe separate to another file)

    def get_rgb_from_id(color_id):
        if (color_toggles[color_id].get()):
            # hsl
            # TODO CHECK IF NONE OF THESE IS ''
            h = float(color_hues[color_id].get())
            l = float(color_lightnesses[color_id].get())
            s = float(color_saturations[color_id].get())
            hls = [h, l, s]
            return colorconvert.hls_to_rgb(hls)
        else:
            #hex
            # TODO CHECK IF NONE OF THESE IS ''
            return colorconvert.hex_to_rgb(color_codes[color_id].get())
    
    def single_comparison(mon, di, tri, c1_norm_rgb, c2_norm_rgb):
        color_pipeline.set_color_blindness_levels(mon, di, tri)
        result = color_pipeline.get_color_difference(
            (c1_norm_rgb[0], c1_norm_rgb[1], c1_norm_rgb[2]),
            (c2_norm_rgb[0], c2_norm_rgb[1], c2_norm_rgb[2])
        )
        result = round(result, 2)
        return result

    def compare_two_colors(id1, id2):
        try:
            c1_norm_rgb = colorconvert.normalize_rgb(get_rgb_from_id(id1))
            # Handle white and black separately from colors
            c2_norm_rgb = None
            if id2 == -1:
                white_rgb = colorconvert.hex_to_rgb(color_white.get())
                c2_norm_rgb = colorconvert.normalize_rgb(white_rgb)
            elif id2 == -2:
                black_rgb = colorconvert.hex_to_rgb(color_black.get())
                c2_norm_rgb = colorconvert.normalize_rgb(black_rgb)
            else:

                c2_norm_rgb = colorconvert.normalize_rgb(get_rgb_from_id(id2))
            limit = float(min_dif.get())
            # Use white and black specific difference limits if those are set
            if id2 == -1 and min_dif_to_white.get() != '':
                limit = float(min_dif_to_white.get())
            if id2 == -2 and min_dif_to_black.get() != '':
                limit = float(min_dif_to_black.get())

            if (compare_ord.get() == 1):
                result = single_comparison(0, 0, 0, c1_norm_rgb, c2_norm_rgb)
                if (result < limit):
                    result_text_col = colorconvert.convert_val_to_col_scale(result, 0, limit)
                    conflict_list.append([id1, id2, f'-', result, result_text_col])
            if (compare_mono.get() == 1):
                result = single_comparison(1, 0, 0, c1_norm_rgb, c2_norm_rgb)
                if (result < limit):
                    result_text_col = colorconvert.convert_val_to_col_scale(result, 0, limit)
                    # TODO function that provides the color code also for the color blindness versions
                    conflict_list.append([id1, id2, f'Protanopia', result, result_text_col])
            if (compare_di.get() == 1):
                result = single_comparison(0, 1, 0, c1_norm_rgb, c2_norm_rgb)
                if (result < limit):
                    result_text_col = colorconvert.convert_val_to_col_scale(result, 0, limit)
                    conflict_list.append([id1, id2, f'Deutranopia', result, result_text_col])
            if (compare_tri.get() == 1):
                result = single_comparison(0, 0, 1, c1_norm_rgb, c2_norm_rgb)
                if (result < limit):
                    result_text_col = colorconvert.convert_val_to_col_scale(result, 0, limit)
                    conflict_list.append([id1, id2, f'Tritanopia', result, result_text_col])
        except:
            failure_list.append([id1,id2])

    #-------------------------------------------------
    # UI BUILD FUNCTIONS (maybe separate to another file)

    def create_color_inputs():
        # TODO Include color block for all color deficiencies
        # TODO Needs function that stores old values first and restores them from old copies after.
        color_amount_int = int(color_amount.get())

        color_previews.clear()
        color_codes.clear()
        color_toggles.clear()
        color_hues.clear()
        color_saturations.clear()
        color_lightnesses.clear()

        for widget in color_frame.winfo_children():
            widget.destroy()

        if (color_amount_int > 0):
            i = 0
            while (i < color_amount_int):
                color_previews.append(tk.StringVar())
                color_previews[i].set('#ddd')
                color_codes.append(tk.StringVar())
                color_toggles.append(tk.IntVar())
                color_hues.append(tk.StringVar())
                color_saturations.append(tk.StringVar())
                color_lightnesses.append(tk.StringVar())
                
                ui_sections.UiSections.create_color_section(
                    color_frame, color_previews[i], color_codes[i], color_toggles[i],
                    color_hues[i], color_lightnesses[i], color_saturations[i]
                )
                i += 1
    
    def populate_hexes():
        for color_code in color_codes:
            if color_code.get() == '':
                color = f'{random.randint(0, 0xFFFFFF):06x}'
                color_code.set(color)

    def compare():
        for widget in result_frame.winfo_children():
            widget.destroy()

        if (len(color_codes) > 0 and float(min_dif.get()) > 0):
            conflict_list.clear()
            failure_list.clear()
            # Compare all colors and find conflicts
            x = 0
            y = 0
            while (x < len(color_codes)):
                while (y < len(color_codes)):
                    if (x != y):
                        compare_two_colors(x, y)
                    y += 1
                compare_two_colors(x, -1)
                compare_two_colors(x, -2)
                x += 1
                # Set y so that same comparisons are not repeated.
                y = x
            
            # Sort the list of conflicts
            sorting_list = []
            for conflict in conflict_list:
                sorting_list.append(conflict[3])
            sorted_conflict_list = [x for _,x in sorted(zip(sorting_list,conflict_list))]
            
            # Create the list of conflicts
            for conflict in sorted_conflict_list:
                col1_hex = colorconvert.rgb_to_hex(get_rgb_from_id(conflict[0]))
                # Handle white and black separately from colors
                col2_hex = None
                if conflict[1] == -1:
                    col2_hex = color_white.get()
                elif conflict[1] == -2:
                    col2_hex = color_black.get()
                else:
                    col2_hex = colorconvert.rgb_to_hex(get_rgb_from_id(conflict[1]))
                ui_sections.UiSections.create_result_section(
                    result_frame, window_width, col1_hex, col2_hex, conflict[2], conflict[3], conflict[4]
                )
            
            # Print failed comparisons
            if failure_list != []:
                print(f'List of failed comparisons: {failure_list}')

    #-------------------------------------------------
    # UI

    #infoFrame = ttk.Frame(windowFrame.scrollable_frame)
    #infoFrame.pack(side='top', fill='x', padx=10, pady=(10, 0))
    #tk.OptionMenu(infoFrame, algorithm, 'Vienot1999', 'Schmitz2015').pack(side='left')
    #tk.Button(infoFrame, text='Info', command=helloWorld).pack(side='left')

    text_frame1 = ttk.Frame(window_frame.scrollable_frame)
    text_frame1.pack(side='top', fill='x', padx=10, pady=(5, 0))
    ttk.Label(text_frame1, text='--- Colors ---', style='Header.TLabel').pack(side='left')

    frame1 = ttk.Frame(window_frame.scrollable_frame)
    frame1.pack(side='top', fill='x', padx=10, pady=(10, 0))
    ttk.Label(frame1, text='Amount of colors').pack(side='left')
    ttk.Entry(frame1, textvariable=color_amount, width=10).pack(side='left')
    tk.Button(frame1, text='Reset', command=create_color_inputs).pack(side='left', padx=(10, 0))
    tk.Button(frame1, text='Populate', command=populate_hexes).pack(side='left', padx=(10, 0))
    ttk.Label(frame1, text='White #').pack(side='left', padx=(10, 0))
    ttk.Entry(frame1, textvariable=color_white).pack(side='left')
    ttk.Label(frame1, text='Black #').pack(side='left', padx=(10, 0))
    ttk.Entry(frame1, textvariable=color_black).pack(side='left')
    #ttk.Combobox(frame1 , state='readonly', values=['Python', 'C', 'C++', 'Java']).pack() 

    color_frame = ttk.Frame(window_frame.scrollable_frame)
    color_frame.pack(side='top', fill='x')

    text_frame2 = ttk.Frame(window_frame.scrollable_frame)
    text_frame2.pack(side='top', fill='x', padx=10, pady=(5, 0))
    ttk.Label(text_frame2, text='--- Comparisons ---', style='Header.TLabel').pack(side='left')

    frame2 = ttk.Frame(window_frame.scrollable_frame)
    frame2.pack(side='top', fill='x', padx=10, pady=(5, 0))
    ttk.Label(frame2, text='Min difference (0-1)').pack(side='left')
    ttk.Entry(frame2, textvariable=min_dif, width=10).pack(side='left')
    ttk.Label(frame2, text='Min difference to white (0-1)').pack(side='left', padx=(10, 0))
    ttk.Entry(frame2, textvariable=min_dif_to_white, width=10).pack(side='left')
    ttk.Label(frame2, text='Min difference to black (0-1)').pack(side='left', padx=(10, 0))
    ttk.Entry(frame2, textvariable=min_dif_to_black, width=10).pack(side='left')

    frame3 = ttk.Frame(window_frame.scrollable_frame)
    frame3.pack(side='top', fill='x', padx=10, pady=(5, 0))
    tk.Checkbutton(frame3, text='Ordinary',variable=compare_ord, onvalue=1, offvalue=0).pack(side='left')
    tk.Checkbutton(frame3, text='Protanopia',variable=compare_mono, onvalue=1, offvalue=0).pack(side='left', padx=(10, 0))
    tk.Checkbutton(frame3, text='Deutranopia',variable=compare_di, onvalue=1, offvalue=0).pack(side='left', padx=(10, 0))
    tk.Checkbutton(frame3, text='Tritanopia',variable=compare_tri, onvalue=1, offvalue=0).pack(side='left', padx=(10, 0))

    frame4 = ttk.Frame(window_frame.scrollable_frame)
    frame4.pack(side='top', fill='x', padx=10, pady=(5, 0))
    tk.Button(frame4, text='Review', command=compare).pack(side='left')

    text_frame3 = ttk.Frame(window_frame.scrollable_frame)
    text_frame3.pack(side='top', fill='x', padx=10, pady=(5, 0))
    ttk.Label(text_frame3, text='--- Results ---', style='Header.TLabel').pack(side='left')

    text_frame4 = ttk.Frame(window_frame.scrollable_frame)
    text_frame4.pack(side='top', fill='x', padx=10, pady=(5, 0))
    ttk.Label(text_frame4, text='Overall score: 0.0, Highest: 0.0, Lowest: 0.0').pack(side='left')

    result_frame = ttk.Frame(window_frame.scrollable_frame)
    result_frame.pack(side='top', fill='x')

    #-------------------------------------------------
    # END

    create_color_inputs()

    root.mainloop()