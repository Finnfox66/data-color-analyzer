from pyciede2000 import ciede2000

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

    def get_color_difference(a: (float, float, float), b: (float, float, float)):
        ciede2000(a, b)
