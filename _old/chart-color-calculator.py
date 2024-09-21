import tkinter as tk
from tkinter import ttk
import colorsys as cs
import platform

# TODO
# Scale generator
# Slider foor root hue

root = tk.Tk()
root.title("Chart color test")

# set up all input variables
onOff1 = tk.IntVar()
onOff2 = tk.IntVar()
onOff3 = tk.IntVar()
rootColor = tk.StringVar()
rootColor.set('#32a852')

scaleSaturation = [0.2, 0.3, 0.4, 0.45, 0.5, 0.45, 0.4, 0.3, 0.2]
scaleLightness = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
scalesCount = 9

size = 60
gap = 10
marginLeft = 50
marginTop = 50

lightBg = '#eeeeee'
darkBg = '#111111'

canvasWidth = ((scalesCount + 1) * (size + gap)) - gap + (marginLeft * 2)
canvasHeight = (len(scaleLightness) * (size + gap)) - gap + (marginTop * 2)


#-------------------------------------------------
# VIEW

# https://blog.teclado.com/tkinter-scrollable-frames/
class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self, width=canvasWidth, height=canvasHeight)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


frame=ScrollableFrame(root)


#-------------------------------------------------
# UTILITY

def getRgbFromHex(hexColorVar):
    hexColor = hexColorVar.get()
    hexColor = hexColor.lstrip('#')
    return tuple(int(hexColor[i:i+2], 16) for i in (0, 2, 4))

def getHueFromRgb(rgb):
    hsl = cs.rgb_to_hls(rgb[0], rgb[1], rgb[2])
    return hsl[0]
    
def getLuminocityFromRgb(rgb):
    # convert to sRGB with relative luminance
    srgb = [rgb[0]/255, rgb[1]/255, rgb[2]/255]
    rgb2 = [0, 0, 0]
    
    i = 0
    for color in srgb:
        if color <= 0.03928:
            rgb2[i] = color/12.92
        else:
            rgb2[i] = ((color+0.055)/1.055)**2.4
        i += 1
    
    luminosity = (0.2126*rgb2[0] + 0.7152*rgb2[1] + 0.0722*rgb2[2])
    
    return luminosity


#-------------------------------------------------
# CONTENT

# get luminosity for canvas
# cut off the "#"
lightBgString = lightBg[1:]
darkBgString = darkBg[1:]
# convert to tuple (255, 255, 255)
lightBgTuple = tuple(int(lightBgString[i:i+2], 16) for i in (0, 2, 4))
darkBgTuple = tuple(int(darkBgString[i:i+2], 16) for i in (0, 2, 4))
# get luminosity
lightBgLum = getLuminocityFromRgb(lightBgTuple)
darkBgLum = getLuminocityFromRgb(darkBgTuple)

def createColors():
    canvas.delete("all")
    if onOff1.get() == 1:
        canvas.configure(bg=darkBg)
    else:
        canvas.configure(bg=lightBg)
    
    # get the hue from root color
    startingHue = getHueFromRgb(getRgbFromHex(rootColor))
    currentHue = startingHue
    
    # get the scaleStep from scalesCount
    hueStep = 1 - scalesCount / 100
    
    currentRowAmount = 0
    currentColAmount = 0
    
    x = 0
    while currentHue < startingHue + (hueStep * (scalesCount + 1)):
        currentRowAmount = 0

        y = 0
        while y < len(scaleLightness):
            hue = currentHue
            saturation = scaleSaturation[y]
            lightness = scaleLightness[y]
            
            hsl = {"hue": hue, "saturation": saturation, "lightness": lightness}
            rgb = cs.hls_to_rgb(hsl["hue"], hsl["lightness"], hsl["saturation"])
            r = int(rgb[0]*255)
            g = int(rgb[1]*255)
            b = int(rgb[2]*255)
            hexcol = '#%02x%02x%02x' % (r, g, b)
            rgb2 = [r, g, b]
            
            luminosity = getLuminocityFromRgb(rgb2)
            
            contrastToLight = (lightBgLum + 0.05) / (luminosity + 0.05)
            contrastToDark = (luminosity + 0.05) / (darkBgLum + 0.05)

            topLeftX = marginLeft + (currentColAmount * (size + gap))
            topLeftY = marginTop + (currentRowAmount * (size + gap))
            botRightX = topLeftX + size
            botRightY = topLeftY + size
            
            if onOff2.get() == 0:
                canvas.create_rectangle(topLeftX, topLeftY, botRightX, botRightY, fill = hexcol, width = 0)
            else:
                if onOff1.get() == 0 and contrastToLight < 3:
                    canvas.create_rectangle(topLeftX, topLeftY, botRightX, botRightY, width = 0)
                elif onOff1.get() == 1 and contrastToDark < 3:
                    canvas.create_rectangle(topLeftX, topLeftY, botRightX, botRightY, width = 0)
                else:
                    canvas.create_rectangle(topLeftX, topLeftY, botRightX, botRightY, fill = hexcol, width = 0)
            
            textColor = darkBg;
            if contrastToDark < 4.5:
                textColor = lightBg;
            
            if onOff3.get() == 0:
                canvas.create_text(topLeftX + size/2, topLeftY + size/5, text=hexcol, fill=textColor)
                canvas.create_text(topLeftX + size/2, topLeftY + size/5*2, text=round(luminosity, 1), fill=textColor)
                canvas.create_text(topLeftX + size/2, topLeftY + size/5*3, text=round(contrastToLight, 1), fill=textColor)
                canvas.create_text(topLeftX + size/2, topLeftY + size/5*4, text=round(contrastToDark, 1), fill=textColor) 
            
            currentRowAmount += 1
            y += 1
        
        currentColAmount += 1
        currentHue += hueStep
        x += 1


#-------------------------------------------------
# UI

frame1 = ttk.Frame(frame.scrollable_frame)
frame1.pack(side="top")
checkBox1 = tk.Checkbutton(frame1, text='Dark mode',variable=onOff1, onvalue=1, offvalue=0, command=createColors, height=2)
checkBox2 = tk.Checkbutton(frame1, text='Contrast only',variable=onOff2, onvalue=1, offvalue=0, command=createColors, height=2)
checkBox3 = tk.Checkbutton(frame1, text='Show text',variable=onOff3, onvalue=1, offvalue=0, command=createColors, height=2)
checkBox1.pack(side="left")
checkBox2.pack(side="left")
checkBox3.pack(side="left")
# checkBox1.grid(row=0, column=0)
# checkBox1.grid(row=0, column=1)
# checkBox1.grid(row=0, column=2)

frame2 = ttk.Frame(frame.scrollable_frame)
frame2.pack(side="top")
tk.Label(frame2, text="root color:").pack(side="left")
textBox = tk.Entry(frame2, textvariable=rootColor, width=15).pack(side="left")
tk.Button(frame2, text="Refresh", command=createColors).pack(side="left")

frame3 = ttk.Frame(frame.scrollable_frame)
frame3.pack(side="top")
canvas = tk.Canvas(frame3, width = canvasWidth, height = canvasHeight, bg=lightBg)
canvas.pack(side="left")
# canvas.grid(row=1, column=0)

createColors()

frame.pack()
root.mainloop()


