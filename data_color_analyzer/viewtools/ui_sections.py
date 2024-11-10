import tkinter as tk
from tkinter import ttk
from data_color_analyzer.colortools import colorconvert

class UiSections():

    def create_color_section(frame, preview, code, toggle, hue, lightness, saturation):
        # TODO add color IDs here.
        color_frame = ttk.Frame(frame)
        color_frame.pack(side='top', fill='x', padx=10, pady=(5, 0))
        canvas = tk.Canvas(color_frame, width=22, height=22)
        canvas.create_rectangle(0, 0, 22, 22, fill = preview.get(), width = 0)
        canvas.pack(side='left')
        ttk.Label(color_frame, text="Color #").pack(side='left')
        ttk.Entry(color_frame, textvariable=code).pack(side='left')
        tk.Checkbutton(color_frame, text='OR',variable=toggle, onvalue=1, offvalue=0).pack(side='left', padx=(10, 0))
        ttk.Label(color_frame, text="Hue (0-240)").pack(side='left', padx=(10, 0))
        ttk.Entry(color_frame, textvariable=hue, width=10).pack(side='left')
        ttk.Label(color_frame, text="Lightness %").pack(side='left', padx=(10, 0))
        ttk.Entry(color_frame, textvariable=lightness, width=10).pack(side='left')
        ttk.Label(color_frame, text="Saturation %").pack(side='left', padx=(10, 0))
        ttk.Entry(color_frame, textvariable=saturation, width=10).pack(side='left')

        # Update function for the color block. Could be separate for hls and hex.
        def update_col_block(var, index, mode):
            color_row_widgets = color_frame.winfo_children()
            try:
                if (toggle.get() == 0):
                    color_row_widgets[0].itemconfigure(1, fill=f"#{code.get()}")
                else:
                    rgb = colorconvert.hls_to_rgb([
                        float(hue.get()), float(lightness.get()), float(saturation.get())
                    ])
                    hex = colorconvert.rgb_to_hex(rgb)
                    color_row_widgets[0].itemconfigure(1, fill=f"#{hex}")
            except:
                color_row_widgets[0].itemconfigure(1, fill=f"#ddd")

        # Create triggers for the color block update function.
        code.trace_add('write', update_col_block)
        toggle.trace_add('write', update_col_block)
        hue.trace_add('write', update_col_block)
        lightness.trace_add('write', update_col_block)
        saturation.trace_add('write', update_col_block)
    
    def create_result_section(frame, window_width, col1_hex, col2_hex, col1_sim_hex, col2_sim_hex, text1, value, value_col):
        # TODO add color IDs here.
        col1_hex = "#" + col1_hex
        col2_hex = "#" + col2_hex
        col1_sim_hex = "#" + col1_sim_hex
        col2_sim_hex = "#" + col2_sim_hex
        value_text = f"{value}"
        value_col_text = f"#{value_col}"
        result_frame = ttk.Frame(frame)
        result_frame.pack(side='top', fill='x', pady=(5, 0))
        canvas = tk.Canvas(result_frame, width=window_width, height=60, bg='#ddd')
        canvas.create_rectangle(10, 0, 70, 60, fill=col1_hex, width=0)
        canvas.create_rectangle(80, 0, 140, 60, fill=col2_hex, width=0)
        canvas.create_rectangle(160, 0, 220, 60, fill=col1_sim_hex, width=0)
        canvas.create_rectangle(230, 0, 290, 60, fill=col2_sim_hex, width=0)
        canvas.create_text(310, 24, text=text1, fill="black", font=('Segoe_UI 9 bold'), anchor=tk.NW)
        canvas.create_text(420, 24, text=value_text, fill=value_col_text, font=('Segoe_UI 9 bold'), anchor=tk.NW)
        canvas.pack(side='left')