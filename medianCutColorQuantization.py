import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from pywaffle import Waffle
import os

imageArray = []
colorArray = []
reducedImage = []


def make_image():
    data = np.asarray(reducedImage)

    img = Image.fromarray(data)
    img.save("reduced.jpg")
    img.show()


def plot_fig():

    color = []
    occurance = []
    for item in colorArray:
        occurance.append(item[3])
        color.append('#%02x%02x%02x' %
                     (int(item[0]), int(item[1]), int(item[2])))

    fig = plt.figure(
        FigureClass=Waffle,
        rows=5,
        columns=10,
        colors=color,
        values=occurance,
        figsize=(5, 3)  # figsize is a parameter of matplotlib.pyplot.figure
    )
    plt.show()


def median_cut_quantize(imageArray):
    # when it reaches the end, color quantize
    redAverage = np.mean(imageArray[:, 0])
    greenAverage = np.mean(imageArray[:, 1])
    blueAverage = np.mean(imageArray[:, 2])

    colorArray.append([redAverage, greenAverage, blueAverage, len(imageArray)])

    for data in imageArray:
        reducedImage[data[3]][data[4]] = [
            redAverage, greenAverage, blueAverage]


def split_into_buckets(imageArray, depth):
    if len(imageArray) == 0:
        return

    if depth == 0:
        median_cut_quantize(imageArray)
        return

    redRange = np.max(imageArray[:, 0]) - np.min(imageArray[:, 0])
    greenRange = np.max(imageArray[:, 1]) - np.min(imageArray[:, 1])
    blueRange = np.max(imageArray[:, 2]) - np.min(imageArray[:, 2])

    spaceWithGreatestRange = 0

    if greenRange >= redRange and greenRange >= blueRange:
        spaceWithGreatestRange = 1
    elif blueRange >= redRange and blueRange >= greenRange:
        spaceWithGreatestRange = 2
    elif redRange >= blueRange and redRange >= greenRange:
        spaceWithGreatestRange = 0

    imageArray = imageArray[imageArray[:, spaceWithGreatestRange].argsort()]
    medianIndex = int((len(imageArray)+1)/2)

    split_into_buckets(imageArray[0:medianIndex], depth-1)
    split_into_buckets(imageArray[medianIndex:], depth-1)


filename = "/Users/kentondover/Programming/python/pictures/pictures/0D3A0201.jpg"
size = 128, 128


file, ext = os.path.splitext(filename)
im = Image.open(filename)
im.thumbnail(size)
im.save(file + ".thumbnail", "JPEG")


with Image.open(filename.replace("jpg", "thumbnail")) as image:
    width, height = image.size
    reducedImage = np.zeros([height, width, 3], dtype=np.uint8)
    totalPixels = width * height
    data = np.asarray(image)

    for rowIndex, rows in enumerate(data):
        for colorIndex, color in enumerate(rows):
            imageArray.append(
                [
                    color[0],
                    color[1],
                    color[2],
                    rowIndex,
                    colorIndex
                ])
    imageArray = np.array(imageArray)
    split_into_buckets(imageArray, 4)
    plot_fig()
    make_image()
