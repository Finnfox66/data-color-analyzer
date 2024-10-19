import numpy as np
from pyciede2000 import ciede2000
from skimage import color

class Ciede2000:
    """
    Library page: https://pypi.org/project/pyciede2000/
    """

    @staticmethod
    def get_description():
        return 'CIEDE2000 standard as implemented by the pyciede2000 library.'
    
    @staticmethod
    def get_reference():
        return """
        @article{Sharma2005TheObservations,
            title = {{The CIEDE2000 color-difference formula: Implementation notes, supplementary test data, and mathematical observations}},
            year = {2005},
            journal = {Color Research {\&} Application},
            author = {Sharma, Gaurav and Wu, Wencheng and Dalal, Edul N},
            number = {1},
            month = {2},
            pages = {21--30},
            volume = {30},
            publisher = {Wiley Subscription Services, Inc., A Wiley Company},
            url = {http://dx.doi.org/10.1002/col.20070},
            doi = {10.1002/col.20070},
            issn = {1520-6378},
            keywords = {CIE, CIE94, CIEDE2000, CIELAB, CMC, color-difference metrics}
        }
        """

    def get_color_difference(a: tuple[float, float, float], b: tuple[float, float, float]):
        """
        Get a difference score for two colors.

        :param a: The first color as (r, g, b) with values [0, 1].
        :param b: The second color as (r, g, b) with values [0, 1].
        """

        # Convert colors from [0, 1] to [0, 255]
        a_arr = np.array(a) * 255.0
        b_arr = np.array(b) * 255.0

        # Convert the colors to the Lab color representation
        colors = np.array([[a_arr, b_arr]], dtype=np.uint8)
        colors_lab = color.rgb2lab(colors)

        data = ciede2000(tuple(colors_lab[0][0]), tuple(colors_lab[0][1]))
        result = data['delta_E_00']
        return result / 100
