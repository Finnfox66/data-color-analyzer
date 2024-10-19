# data-color-analyzer

Python script for analyzing data colors

## Setup

```sh
poetry install
```

## Use

To run the app in the GUI mode, run

```sh
poetry run gui
```

To generate a color set using the CLI, run

```sh
poetry run generate <generate_count> <initial_color_hex_1> [<inital_color_hex_2>, ...]
```

## Sources

pyciede2000
https://pypi.org/project/pyciede2000/

StackExchange: "How do I calculate how the colourblind would see a given colour?"
https://graphicdesign.stackexchange.com/questions/84407/how-do-i-calculate-how-the-colourblind-would-see-a-given-colour/84417#84417

"Color Blindness Simulation Research"
https://ixora.io/projects/colorblindness/color-blindness-simulation-research/

"Exploring Color Math Through Color Blindness"
https://dev.to/ndesmic/exploring-color-math-through-color-blindness-2m2h
