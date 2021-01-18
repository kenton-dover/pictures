import os
import glob
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from pywaffle import Waffle


imageArray = []
colorArray = []
colorPercentage = 50


def get_colors(imageArray):
    for color in imageArray:
        if not colorArray:
            color[3] = color[3] + 1
            colorArray.append(color)
            # colorArray[0][0] = color[0]
        else:
            for colorIndex, tempColor in enumerate(colorArray):
                redMin = tempColor[0] - colorPercentage
                redMax = tempColor[0] + colorPercentage
                greenMin = tempColor[1] - colorPercentage
                greenMax = tempColor[1] + colorPercentage
                blueMin = tempColor[2] - colorPercentage
                blueMax = tempColor[2] + colorPercentage
                if color[0] >= redMin and color[0] <= redMax and color[1] >= greenMin and color[1] <= greenMax and color[2] >= blueMin and color[2] <= blueMax:
                    colorArray[colorIndex][3] += 1
                    break

                elif len(colorArray) == colorIndex + 1:
                    color[3] = color[3] + 1
                    colorArray.append(color)
    return colorArray


def plot_fig(colorArray):
    colorArray.sort(key=lambda x: x[3])
    colorArray = colorArray[-20:]
    print(colorArray)
    color = []
    occurrence = []
    for item in colorArray:
        occurrence.append(item[3])
        color.append('#%02x%02x%02x' %
                     (int(item[0]), int(item[1]), int(item[2])))

    fig = plt.figure(
        FigureClass=Waffle,
        rows=1,
        columns=5,
        colors=color,
        values=occurrence,
        figsize=(5, 3)  # figsize is a parameter of matplotlib.pyplot.figure
    )
    plt.show()


filename = "/Users/kentondover/Programming/python/pictures/pictures/platform.jpg"


size = 128, 128


file, ext = os.path.splitext(filename)
im = Image.open(filename)
im.thumbnail(size)
im.save(file + ".thumbnail", "JPEG")


with Image.open(filename.replace("jpg", "thumbnail")) as image:
    width, height = image.size
    totalPixels = width * height
    data = np.asarray(image)

    for rowIndex, rows in enumerate(data):
        for colorIndex, color in enumerate(rows):
            imageArray.append(
                [
                    color[0],
                    color[1],
                    color[2],
                    0
                    # rowIndex,
                    # colorIndex
                ])
    # imageArray = np.array(imageArray)
    colorArray = get_colors(imageArray)
    plot_fig(colorArray)
