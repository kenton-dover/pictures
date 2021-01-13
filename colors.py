from PIL import Image
from collections import Counter

import matplotlib.pyplot as plt
from pywaffle import Waffle


filename = "/Users/kentondover/Programming/python/pictures/pictures/0D3A0201.jpg"
with Image.open(filename) as image:
    width, height = image.size
    totalPixels = width * height
    pix = image.load()
    pixels = []
    for x in range(width):
        for y in range(height):
            pixels.append(pix[x, y])

    counter = Counter(pixels)
    mostCommon = counter.most_common(10)

    color = []
    occurrence = []
    for item in mostCommon:

        color.append('#%02x%02x%02x' % item[0])
        occurrence.append(item[1] / totalPixels * 100)
    print(mostCommon)
    print("")
    print(mostCommon[0])

    fig = plt.figure(
        FigureClass=Waffle,
        rows=1,
        columns=5,
        colors=color,
        values=occurrence,
        figsize=(5, 3)  # figsize is a parameter of matplotlib.pyplot.figure
    )
    plt.show()
