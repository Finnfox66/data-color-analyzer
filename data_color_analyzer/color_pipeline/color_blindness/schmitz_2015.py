import numpy as np

class Schmitz2015:
    """
    This algorithm assumes that all colors are in range [0, 1].

    Article: https://ixora.io/projects/colorblindness/color-blindness-simulation-research/
    """

    @staticmethod
    def get_description():
        return 'An improved color blindness algorithm by James Schmitz from a web article written in 2015.'

    @staticmethod
    def get_reference():
        return """
        @misc{Schmitz2015,
            title = {Color Blindness Simulation Research},
            howpublished = {\\url{https://ixora.io/projects/colorblindness/color-blindness-simulation-research/}},
            note = {Accessed: 2024-09-21}
        }
        """

    @staticmethod
    def rgb_to_lms():
        """
        Matrix for RGB color-space to LMS color-space transformation.
        """
        return np.array([[0.31399022, 0.63951294, 0.04649755],
                         [0.15537241, 0.75789446, 0.08670142],
                         [0.01775239, 0.10944209, 0.87256922]]).T

    @staticmethod
    def lms_to_rgb() -> np.ndarray:
        """
        Matrix for LMS colorspace to RGB colorspace transformation.
        """
        return np.array([[5.47221206, -4.6419601, 0.16963708],
                         [-1.1252419, 2.29317094, -0.1678952],
                         [0.02980165, -0.19318073, 1.16364789]]).T

    @staticmethod
    def lms_protanopia_sim(degree: float = 1.0) -> np.ndarray:
        """
        Matrix for Simulating Protanopia colorblindness from LMS color-space.
        :param degree: Protanopia degree.
        """
        return np.array([[1 - degree, 1.05118294 * degree, -0.05116099 * degree],
                         [0, 1, 0],
                         [0, 0, 1]]).T

    @staticmethod
    def lms_deutranopia_sim(degree: float = 1.0) -> np.ndarray:
        """
        Matrix for Simulating Deutranopia colorblindness from LMS color-space.
        :param degree: Deutranopia degree.
        """
        return np.array([[1, 0, 0],
                         [0.9513092 * degree, 1 - degree, 0.04866992 * degree],
                         [0, 0, 1]]).T

    @staticmethod
    def lms_tritanopia_sim(degree: float = 1.0) -> np.ndarray:
        """
        Matrix for Simulating Tritanopia colorblindness from LMS color-space.
        :param degree: Tritanopia degree.
        """
        return np.array([[1, 0, 0],
                         [0, 1, 0],
                         [-0.86744736 * degree, 1.86727089 * degree, 1 - degree]]).T
