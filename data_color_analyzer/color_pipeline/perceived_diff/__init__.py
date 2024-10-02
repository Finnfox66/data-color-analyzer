from data_color_analyzer.color_pipeline.perceived_diff.ciede2000 import Ciede2000

PERCEIVED_DIFF_ALGORITHMS = ['ciede2000']

def get_algorithm(algorithm):
    if (algorithm == 'ciede2000'):
        return Ciede2000

    raise Exception(f"The perceived diff algorithm '{algorithm}' is not in the list of accepted algorithms {PERCEIVED_DIFF_ALGORITHMS}")
