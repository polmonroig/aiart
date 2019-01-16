import numpy as np


# get average color of a list of colors
def avg_color(colors):
    p_color = np.array([0, 0, 0])
    for color in colors:
        p_color[0] += color[0]
        p_color[1] += color[1]
        p_color[2] += color[2]
    size = colors.shape[0]
    p_color /= size
    return p_color
