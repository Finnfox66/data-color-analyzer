import numpy as np

class Vienot1999:
    """
    Original research paper: https://vision.psychol.cam.ac.uk/jdmollon/papers/colourmaps.pdf
    Referencing research paper: https://arxiv.org/pdf/1711.10662.pdf
    Implementation adapted from: https://github.com/tsarjak/Simulate-Correct-ColorBlindness
    """

    @staticmethod
    def get_description():
        return 'A widely used and cited color blindness algorithm by Francoise Vienot, Hans Brettel and John D. Mollon from a research paper written in 1999.'

    @staticmethod
    def get_reference():
        return """
        @article{https://doi.org/10.1002/(SICI)1520-6378(199908)24:4<243::AID-COL5>3.0.CO;2-3,
            author = {Viénot, Françoise and Brettel, Hans and Mollon, John D.},
            title = {Digital video colourmaps for checking the legibility of displays by dichromats},
            journal = {Color Research \& Application},
            volume = {24},
            number = {4},
            pages = {243-252},
            keywords = {colour, dichromacy, computer, simulation, recognition, fundamentals, colour vision deficiencies},
            doi = {https://doi.org/10.1002/(SICI)1520-6378(199908)24:4<243::AID-COL5>3.0.CO;2-3},
            url = {https://onlinelibrary.wiley.com/doi/abs/10.1002/%28SICI%291520-6378%28199908%2924%3A4%3C243%3A%3AAID-COL5%3E3.0.CO%3B2-3},
            eprint = {https://onlinelibrary.wiley.com/doi/pdf/10.1002/%28SICI%291520-6378%28199908%2924%3A4%3C243%3A%3AAID-COL5%3E3.0.CO%3B2-3},
            abstract = {Abstract We propose replacement colourmaps that allow a designer to check the colours seen by protanopes and deuteranopes. Construction of the colourmaps is based on the LMS specification of the primaries of a standard video monitor and has been carried out for 256 colours, including 216 colours that are common to many graphics applications of MS Windows and Macintosh computing environments. © 1999 John Wiley \& Sons, Inc. Col Res Appl, 24, 243–252, 1999},
            year = {1999}
        }
        """

    @staticmethod
    def rgb_to_lms():
        """
        Matrix for RGB color-space to LMS color-space transformation.
        """
        return np.array([[17.8824, 43.5161, 4.11935],
                         [3.45565, 27.1554, 3.86714],
                         [0.0299566, 0.184309, 1.46709]]).T

    @staticmethod
    def lms_to_rgb() -> np.ndarray:
        """
        Matrix for LMS colorspace to RGB colorspace transformation.
        """
        return np.array([[0.0809, -0.1305, 0.1167],
                         [-0.0102, 0.0540, -0.1136],
                         [-0.0004, -0.0041, 0.6935]]).T

    @staticmethod
    def lms_protanopia_sim(degree: float = 1.0) -> np.ndarray:
        """
        Matrix for Simulating Protanopia colorblindness from LMS color-space.
        :param degree: Protanopia degree.
        """
        return np.array([[1 - degree, 2.02344 * degree, -2.52581 * degree],
                         [0, 1, 0],
                         [0, 0, 1]]).T

    @staticmethod
    def lms_deutranopia_sim(degree: float = 1.0) -> np.ndarray:
        """
        Matrix for Simulating Deutranopia colorblindness from LMS color-space.
        :param degree: Deutranopia degree.
        """
        return np.array([[1, 0, 0],
                         [0.494207 * degree, 1 - degree, 1.24827 * degree],
                         [0, 0, 1]]).T

    # Where is this from? It's not in the referenced research papers.
    @staticmethod
    def lms_tritanopia_sim(degree: float = 1.0) -> np.ndarray:
        """
        Matrix for Simulating Tritanopia colorblindness from LMS color-space.
        :param degree: Tritanopia degree.
        """
        return np.array([[1, 0, 0],
                         [0, 1, 0],
                         [-0.395913 * degree, 0.801109 * degree, 1 - degree]]).T
