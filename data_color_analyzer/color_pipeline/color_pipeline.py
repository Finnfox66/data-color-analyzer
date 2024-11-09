import numpy as np

import data_color_analyzer.color_pipeline.color_blindness as color_blindness
import data_color_analyzer.color_pipeline.perceived_diff as perceived_diff


class ColorPipeline:
    def __init__(self, color_blindness_algorithm: str, perceived_diff_algorithm: str):
        self.color_blindness = color_blindness.get_algorithm(color_blindness_algorithm)
        self.perceived_diff = perceived_diff.get_algorithm(perceived_diff_algorithm)

        self.set_color_blindness_levels(0, 0, 0)

    def set_color_blindness_levels(self, protanopia: float, deutranopia: float, tritanopia: float):
        """
        Sets the weights of the different color blindness levels
        used for the color difference calculation.

        :param protanopia: The weight of protanopia (unable to perceive red) color blindness, values [0, 1].
        :param deutranopia: The weight of deutranopia (unable to perceive green) color blindness, values [0, 1].
        :param tritanopia: The weight of tritanopia (unable to perceive blue) color blindness, values [0, 1].
        """

        self.protanopia = protanopia
        self.deutranopia = deutranopia
        self.tritanopia = tritanopia

        self.update_conversion_matrix()

    def update_conversion_matrix(self):
        self.conversion_matrix = np.matmul(
            np.matmul(
                self.color_blindness.lms_protanopia_sim(self.protanopia),
                self.color_blindness.lms_deutranopia_sim(self.deutranopia)
            ),
            self.color_blindness.lms_tritanopia_sim(self.tritanopia)
        )

    def get_color_difference(self, a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
        """
        Get a difference score for two colors simulated for color blindness.

        :param a: The first color as (r, g, b) with values [0, 1].
        :param b: The second color as (r, g, b) with values [0, 1].
        """
        a_sim = self.get_simulated_color(a)
        b_sim = self.get_simulated_color(b)

        diff = self.perceived_diff.get_color_difference(tuple(a_sim), tuple(b_sim))
        return diff



    def get_simulated_color(self, a: tuple[float, float, float]) -> float:
        """
        Get a version of a given color with the simulated color blindness levels.

        :param a: The color as (r, g, b) with values [0, 1].
        """
        rgb = np.array(a)

        # Color in LMS color space
        lms = np.matmul(rgb, self.color_blindness.rgb_to_lms())

        # Color converted to the color blindness scale
        conv = np.matmul(lms, self.conversion_matrix)

        # Fully simulated color back in the RGB color space
        return np.matmul(conv, self.color_blindness.lms_to_rgb())
