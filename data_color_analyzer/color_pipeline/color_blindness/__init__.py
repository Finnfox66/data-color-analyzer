from data_color_analyzer.color_pipeline.color_blindness.vienot_1999 import Vienot1999
from data_color_analyzer.color_pipeline.color_blindness.schmitz_2015 import Schmitz2015

COLOR_BLINDNESS_ALGORITHMS = ['Vienot1999', 'Schmitz2015']

def get_algorithm(algorithm):
    if (algorithm == 'Vienot1999'):
        return Vienot1999()
    if (algorithm == 'Schmitz2015'):
        return Schmitz2015()

    raise Exception(f"The color blindness algorithm '{algorithm}' is not in the list of accepted algorithms {COLOR_BLINDNESS_TYPES}")
