import numpy as np
import math
import colorsys
import time
import wcag_contrast_ratio as contrast

from data_color_analyzer.color_pipeline import ColorPipeline
from data_color_analyzer.color_generator.crawler import Crawler

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
            lambda x: colorsys.rgb_to_hsv(*x),
            initial_colors
        ))

        saturationSum = 0
        saturationCount = 0

        has_black = False
        has_white = False

        for hsv_color in hsv_colors:
            if hsv_color[2] <= 0:
                self.log(f"Black color of HSV value {hsv_color} given as initial, skipping...")
                has_black = True
                continue
            if hsv_color[2] >= 1:
                self.log(f"White color of HSV value {hsv_color} given as initial, skipping...")
                has_white = True
                continue

            saturationSum += hsv_color[1]
            saturationCount += 1

        if saturationCount <= 0:
            raise Exception('The initial colors do not contain any colors other than white and black')

        targetSaturation = saturationSum / saturationCount

        if not has_black:
            hsv_colors.append((0.0, 0.0, 0.0))
        if not has_white:
            hsv_colors.append((0.0, 0.0, 1.0))

        self.log(f"Target saturation set to {targetSaturation}")
        self.log(f"Beginning generation of {generate_count} colors with initial HSV colors {hsv_colors}")

        start_time = time.time()
        # diff_map = self.calculate_diff_map(hsv_colors, targetSaturation)
        potential_results = self.find_with_crawlers(hsv_colors, targetSaturation)
        elapsed_seconds = time.time() - start_time
        self.log(f"Diff map calculated in: {elapsed_seconds} seconds")
        self.log(potential_results)

    def calculate_diff_map_simple(self, compare_hsv_colors: list[tuple[float, float, float]], targetSaturation: float) -> np.ndarray[np.float64]:
        map = np.zeros((256, 256))
        saturation = int(round(targetSaturation * 255))

        for hue in range(0, 256):
            for value in range(0, 256):
                hsv_color = tuple(np.array((hue, saturation, value)) / 255)
                rgb_color = colorsys.hsv_to_rgb(*hsv_color)

                # The color must have at least the minimum contrast to black and white
                if contrast.rgb(rgb_color, (0.0, 0.0, 0.0)) < self.min_contrast_ratio:
                    continue
                if contrast.rgb(rgb_color, (1.0, 1.0, 1.0)) < self.min_contrast_ratio:
                    continue

                diff = self.get_hsv_rms_color_difference(hsv_color, compare_hsv_colors)
                map[hue, value] = diff

        return map

    def calculate_diff_map(self, compare_hsv_colors: list[tuple[float, float, float]], target_saturation: float) -> np.ndarray[np.float64]:
        detail_divs = [4, 2, 1]
        diff_maps = list(map(lambda x: np.zeros((int(256 / x), int(256 / x))), detail_divs))
        saturation = int(round(target_saturation * 255))

        diff_avg = 0

        for idx in range(0, len(detail_divs)):
            detail_div = detail_divs[idx]
            diff_map = diff_maps[idx]
            detail_offset = ((detail_div / 2.0) - 0.5) / 256.0

            diff_sum = 0
            diff_count = 0

            scale = int(256 / detail_div)

            for hue in range(0, scale):
                for value in range(0, scale):
                    if idx > 0:
                        # Check if the previously calculated estimate is
                        # under the diff average.
                        diff_estimate = diff_maps[idx - 1][int(hue / 2), int(value / 2)]
                        if diff_estimate < diff_avg:
                            # Do not recalculate this, use the estimate.
                            diff_map[hue, value] = diff_estimate
                            continue

                    hsv_color = np.array((hue, saturation, value)) / 255
                    rgb_color = colorsys.hsv_to_rgb(*hsv_color)

                    # The color must have at least the minimum contrast to black and white
                    if contrast.rgb(rgb_color, (0.0, 0.0, 0.0)) < self.min_contrast_ratio:
                        continue
                    if contrast.rgb(rgb_color, (1.0, 1.0, 1.0)) < self.min_contrast_ratio:
                        continue

                    hsv_color_with_offset = tuple(hsv_color + detail_offset)
                    diff = self.get_hsv_rms_color_difference(hsv_color_with_offset, compare_hsv_colors)
                    diff_map[hue, value] = diff

                    diff_sum += diff
                    diff_count += 1

            diff_avg = diff_sum / diff_count

        return diff_maps[len(diff_maps) - 1]

    def find_with_crawlers(self, compare_hsv_colors: list[tuple[float, float, float]], target_saturation: float):
        diff_map = np.zeros((256, 256))

        crawlers: list[tuple[int, int]] = []
        for compare_hsv_color in compare_hsv_colors:
            hue = int(round(compare_hsv_color[0] * 255))
            value = int(round(compare_hsv_color[2] * 255))
            crawlers.extend(self.get_new_crawlers((hue, value)))

        results: list[tuple[float, float, float]] = []

        while (len(crawlers) > 0):
            crawler = crawlers.pop()
            new_crawlers = self.get_new_crawlers(crawler)
            better_found = False
            for new_crawler in new_crawlers:
                new_diff = diff_map[new_crawler[0], new_crawler[1]]
                is_already_explored = new_diff != 0

                if not is_already_explored:
                    hsv_color = (new_crawler[0] / 255, target_saturation, new_crawler[1] / 255)
                    rgb_color = colorsys.hsv_to_rgb(*hsv_color)

                    # The color must have at least the minimum contrast to black and white
                    if contrast.rgb(rgb_color, (0.0, 0.0, 0.0)) < self.min_contrast_ratio:
                        continue
                    if contrast.rgb(rgb_color, (1.0, 1.0, 1.0)) < self.min_contrast_ratio:
                        continue

                    new_diff = self.get_hsv_rms_color_difference(hsv_color, compare_hsv_colors)
                    diff_map[new_crawler[0], new_crawler[1]] = new_diff

                old_diff = diff_map[crawler[0], crawler[1]]

                if new_diff > old_diff:
                    if not is_already_explored:
                        crawlers.append(new_crawler)
                    better_found = True

            if not better_found:
                results.append((crawler[0] / 255, target_saturation, crawler[1] / 255))

        return results

    def get_new_crawlers(self, crawler: tuple[int, int]):
        crawlers = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                new_x = crawler[0] + dx
                new_y = crawler[1] + dy
                if new_x >= 0 and new_x <= 255 and new_y >= 0 and new_y <= 255:
                    crawlers.append((new_x, new_y))
        return crawlers

    def get_hsv_rms_color_difference(self, hsv_color: tuple[float, float, float], compare_hsv_colors: list[tuple[float, float, float]]):
        """
        Calculates the root mean square (RMS) for the difference
        values between the given color and the list of comparison colors.

        :param hsv_color: The color to compare as (h, s, v) with values [0, 1].
        :param compare_hsv_colors: The list of colors to compare as (h, s, v) with values [0, 1].
        """

        diff_square_sum = 0

        rgb_color = colorsys.hsv_to_rgb(*hsv_color)

        for compare_hsv_color in compare_hsv_colors:
            compare_rgb_color = colorsys.hsv_to_rgb(*compare_hsv_color)

            diff = self.color_pipeline.get_color_difference(rgb_color, compare_rgb_color)
            diff_square_sum += diff * diff

        return math.sqrt(diff_square_sum / len(compare_hsv_colors))


