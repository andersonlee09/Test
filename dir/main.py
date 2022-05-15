import math

import matplotlib.pyplot as plt
import readExcel
from collections import OrderedDict

# minDimension, minLongitude
minDimension, minLongitude = 18.25, 75.99
# one minDimension or minLongitude to some KM
x = 130
y = 111.1 / 92 * x
# Offset in map
p_x = -100
p_y = 280
# drew map as background picture
img = plt.imread(r'./pic/map.png')
fig, ax = plt.subplots()
ax.imshow(img, extent=[0, 8000, 0, 6000])
PCFactory, phoneFactory, deliveryCenter, costumer = readExcel.getDifferentPointInMap()


# get x ticks value of point
def getx(point: tuple) -> float:
    return (point[1] - minLongitude) * x + p_x


# get y ticks value of point
def gety(point: tuple) -> float:
    return (point[0] - minDimension) * y + p_y


def drawLine(startPoint: tuple, endPoint: tuple, color='black', linewidth=0.25):
    """
    :param startPoint: (x, y) point in map.
    :param endPoint: (x, y) point in map.
    :param color: line color in map.
    :param linewidth: width of line to drew map. such as 1.
    """
    plt.plot([getx(startPoint), getx(endPoint)], [gety(startPoint), gety(endPoint)],
             color=color,
             linewidth=linewidth)


def getDistanceOfTwoPoint(p1: tuple, p2: tuple) -> float:
    return ((getx(p1) - getx(p2)) ** 2 + (gety(p1) - gety(p2)) ** 2) ** 0.5


def getMinDistanceOfTwoPoint(point: tuple, targetPoints: list) -> tuple:
    """
    todo search a point from targetPoint to get min distance of point & one target point.
    """
    minDistance = 2 ** 30
    targetPoint = (0, 0)
    for target in targetPoints:
        distance = getDistanceOfTwoPoint(point, target)
        if distance < minDistance:
            minDistance = distance
            targetPoint = target
    return targetPoint


# clear x & y ticks
plt.xticks([])
plt.yticks([])

# start to draw!
for _ in costumer:
    if 128 > _[1] > 80 and _[0] > 20:
        plt.scatter(getx(_), gety(_),
                    c='purple',
                    marker='o',
                    s=8,
                    label='consumer')
        # todo draw from consumer to phone factory
        # drawLine(_, getMinDistanceOfTwoPoint(_, phoneFactory))

        # todo draw from consumer to deliver center, deliver city to pc factory
        deliveryCenterPoint = getMinDistanceOfTwoPoint(_, deliveryCenter)
        drawLine(_, deliveryCenterPoint, '#B41490', 0.5)
        drawLine(deliveryCenterPoint, getMinDistanceOfTwoPoint(deliveryCenterPoint, PCFactory), '#343EB4')
for _ in deliveryCenter:
    plt.scatter(getx(_), gety(_),
                c='green',
                marker='s',
                s=24,
                label='deliver center')
for _ in phoneFactory:
    plt.scatter(getx(_), gety(_),
                c='blue',
                marker='x',
                s=35,
                label='phone factory')
for _ in PCFactory:
    # plt.scatter((_[1] - minLongitude) * 111.1, (_[0] - minDimension) * 92,
    plt.scatter(getx(_), gety(_),
                c='red',
                marker='x',
                s=35,
                label='PC factory')
handles, labels = plt.gca().get_legend_handles_labels()
by_label = OrderedDict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys(), loc='lower right')
plt.show()
