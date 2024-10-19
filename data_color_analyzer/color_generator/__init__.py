import numpy as np
import colorsys

from data_color_analyzer.color_pipeline import ColorPipeline

class ColorGenerator:
    def __init__(self, color_pipeline: ColorPipeline) -> None:
        self.color_pipeline = color_pipeline
        self.min_contrast_ratio = 1
        self.log_filename = None

    def log(self, message):
        if self.log_filename is not None:
            # TODO: Log the message to a file
            pass
        else:
            print(message)

    def set_min_black_and_white_contrast_ratio(self, min_contrast_ratio):
        """
        Sets the minimum contrast ratio that all colors must
        have in comparison to black and white.

        :param min_contrast_ratio: The contrast ratio with values [1, 21].
        """

        if min_contrast_ratio < 1:
            raise Exception(f"Min contrast ratio {min_contrast_ratio} is below 1")

        if min_contrast_ratio > 21:
            raise Exception(f"Min contrast ratio {min_contrast_ratio} is above 21")

        self.min_contrast_ratio = min_contrast_ratio

    def generate_colors(self, initial_colors: list[tuple[float, float, float]], generate_count: int):
        """
        Generates a set of colors based on the initial color list.

        :param initial_colors: A set of initial colors to use for generation. List of (r, g, b) tuples with values [0, 1].
        :param generate_count: The number of colors to generate.
        """

        if generate_count < 1:
            raise Exception('The number of colors to generate can not be lower than one.')

        hsv_colors = list(map(
            lambda x: colorsys.rgb_to_hsv(x[0], x[1], x[2]),
            initial_colors
        ))

        saturationSum = 0
        saturationCount = 0

        for hsv_color in hsv_colors:
            if hsv_color[2] <= 0:
                self.log(f"Black color of HSV value {hsv_color} given as initial, skipping...")
                continue
            if hsv_color[2] >= 1:
                self.log(f"White color of HSV value {hsv_color} given as initial, skipping...")
                continue

            saturationSum += hsv_color[1]
            saturationCount += 1

        if saturationCount <= 0:
            raise Exception('The initial colors do not contain any colors other than white and black')

        targetSaturation = saturationSum / saturationCount

        self.log(f"Target saturation set to {targetSaturation}")
        self.log(f"Beginning generation of {generate_count} colors with initial HSV colors {hsv_colors}")


