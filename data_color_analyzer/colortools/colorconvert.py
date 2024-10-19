import colorsys as cs

#def hex_var_to_rgb(hex_color_var):
#    hex_color = hex_color_var.get()
#    hex_color = hex_color.lstrip('#')
#    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# This function assumes that the code doesn't have a hashtag
def hex_to_rgb(hex):
    """
    Converts a hex into rgb.
    :param hex_code: Color hex code without a hashtag.
    """
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    """
    Converts a rgb into hex without a hashtag.
    """
    return '{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

def rgb_to_hls(rgb):
    hsl = cs.rgb_to_hls(rgb[0], rgb[1], rgb[2])
    return hsl

def hls_to_rgb(hls):
    rgb = cs.hls_to_rgb(hls[0], hls[1], hls[2])
    return rgb

def normalize_rgb(rgb):
    normalized_rgb = [rgb[0]/255, rgb[1]/255, rgb[2]/255]
    return normalized_rgb
    
def rgb_to_luminosity(rgb):
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