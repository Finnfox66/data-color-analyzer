import colorsys as cs
from data_color_analyzer.color_pipeline import ColorPipeline

def normalize_rgb(rgb):
    normalized_rgb = [rgb[0]/255, rgb[1]/255, rgb[2]/255]
    return normalized_rgb

def normalize_hls(hls):
    normalized_hls = [hls[0]/360, hls[1]/100, hls[2]/100]
    return normalized_hls

def denormalize_rgb(rgb):
    denormalized_rgb = [rgb[0]*255, rgb[1]*255, rgb[2]*255]
    return denormalized_rgb

def denormalize_hls(hls):
    denormalized_hls = [hls[0]*360, hls[1]*100, hls[2]*100]
    return denormalized_hls

# This function assumes that the code doesn't have a hashtag
def hex_to_rgb(hex):
    """
    Converts a hex into rgb.
    :param hex_code: Color hex code without a hashtag.
    """
    if len(hex) == 3:
        hex = hex[0] + hex[0] + hex[1] + hex[1] + hex[2] + hex[2]
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
    # TODO Check if these returns normalized or unnormalized rgb

def rgb_to_hex(rgb):
    """
    Converts a rgb into hex without a hashtag.
    """
    return '{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def hex_to_color_blindness_hex(hex, blindness_id, color_pipeline):
    match blindness_id:
        case 0:
            color_pipeline.set_color_blindness_levels(0, 0, 0)
        case 1:
            color_pipeline.set_color_blindness_levels(1, 0, 0)
        case 2:
            color_pipeline.set_color_blindness_levels(0, 1, 0)
        case 3:
            color_pipeline.set_color_blindness_levels(0, 0, 1)
    rgb = hex_to_rgb(hex)
    rgb = normalize_rgb(rgb)
    sim_color = color_pipeline.get_simulated_color((rgb[0], rgb[1], rgb[2]))
    denormalized_sim_color = denormalize_rgb(sim_color)
    hex = rgb_to_hex(denormalized_sim_color)
    return hex

def rgb_to_hls(rgb):
    rgb = normalize_rgb(rgb)
    hls = cs.rgb_to_hls(rgb[0], rgb[1], rgb[2])
    hls = denormalize_hls(hls)
    return hls

def hls_to_rgb(hls):
    hls = normalize_hls(hls)
    rgb = cs.hls_to_rgb(hls[0], hls[1], hls[2])
    rgb = denormalize_rgb(rgb)
    return rgb

def convert_val_to_col_scale(value, min, max):
    col1_hue = 240
    col1_lightness = 30
    col2_hue = 360
    col2_lightness = 60
    hue = round(((value - min)/(max - min)) * (col1_hue - col2_hue) + col2_hue)
    lightness = round(((value - min)/(max - min)) * (col1_lightness - col2_lightness) + col2_lightness)
    rgb = hls_to_rgb([hue, lightness, 100])
    hex = rgb_to_hex(rgb)
    return hex