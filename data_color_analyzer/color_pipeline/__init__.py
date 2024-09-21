import data_color_analyzer.color_pipeline.color_blindness as color_blindness
import data_color_analyzer.color_pipeline.perceived_diff as perceived_diff


class ColorPipeline:
    def __init__(self, color_blindness_algorithm: str, perceived_diff_algorithm: str):
        self.color_blindness = color_blindness.get_algorithm(color_blindness_algorithm)
        self.perceived_diff = perceived_diff.get_algorithm(perceived_diff_algorithm)
