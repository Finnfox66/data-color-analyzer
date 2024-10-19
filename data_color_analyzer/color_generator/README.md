# Color generation process

These tools are meant to, when given a set of initial color values, generate a set (of given size) of colours that all have as big of a perceived difference to each other and the initial color values as possible.

All generated colors must have the same saturation value. The initial color values are assumed to have the same saturation values, but this may not be the case. We take the saturation value of each color, calculate the mean and use that as our target saturation value.

## Black and white

Black and white are automatically added to the initial values if they do not exist within it. They are not used for the saturation calculation. If there are no colors besides white and black in the initial color set, an error is thrown.

The user can set a minimum contrast that all generated colors must maintain from black and white.

## Color blindness

For each color distance, the value is calculated separately for each color blindness type. The root mean square (RMS) is then taken for these distance values.
