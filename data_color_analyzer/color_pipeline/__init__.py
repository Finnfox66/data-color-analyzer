import numpy as np

import data_color_analyzer.color_pipeline.color_blindness as color_blindness
import data_color_analyzer.color_pipeline.perceived_diff as perceived_diff


class ColorPipeline:
    def __init__(self, color_blindness_algorithm: str, perceived_diff_algorithm: str):
        self.color_blindness = color_blindness.get_algorithm(color_blindness_algorithm)
        self.perceived_diff = perceived_diff.get_algorithm(perceived_diff_algorithm)

        self.set_color_blindness_levels(0, 0, 0)

    def set_color_blindness_levels(self, protanopia: float, deutranopia: float, tritanopia: float):
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

    def get_color_difference(self, a: (float, float, float), b: (float, float, float)) -> float:
        """
        Get a difference score for two colors simulated for color blindness.
        :param a: The first color as (r, g, b).
        :param b: The second color as (r, g, b).
        """
        a_rgb = np.array(a)
        b_rgb = np.array(b)

        # Colors in LMS color space
        a_lms = np.matmul(a_rgb, self.color_blindness.rgb_to_lms())
        b_lms = np.matmul(b_rgb, self.color_blindness.rgb_to_lms())

        # Colors converted to the color blindness scale
        a_conv = np.matmul(a_lms, self.conversion_matrix)
        b_conv = np.matmul(b_lms, self.conversion_matrix)

        # Fully simulated colors back in the RGB color space
        a_sim = np.matmul(a_conv, self.color_blindness.lms_to_rgb())
        b_sim = np.matmul(b_conv, self.color_blindness.lms_to_rgb())

        diff = self.perceived_diff.get_color_difference(tuple(a_sim), tuple(b_sim))
        return diff
