import colorsys as cs

def hexToRgb(hexColorVar):
    hexColor = hexColorVar.get()
    hexColor = hexColor.lstrip('#')
    return tuple(int(hexColor[i:i+2], 16) for i in (0, 2, 4))

def rgbToHue(rgb):
    hsl = cs.rgb_to_hls(rgb[0], rgb[1], rgb[2])
    return hsl[0]
    
def rgbToLuminosity(rgb):
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