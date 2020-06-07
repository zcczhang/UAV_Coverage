"""
__author__ = "Charles Zhang"
__time__ = "2020-06-04 19:53"
"""

from math import *
from numpy import *
from csv import writer


# (44.937541, -93.168826), (44.936920, -93.168255)


def get_scale(top_left, bottom_right):
    """
    :param top_left: the origin
    :param bottom_right: diagonal point
    :return: (long_per_meter, lat_per_meter)
    """
    top, left, bottom, right = top_left[0], top_left[1], bottom_right[0], bottom_right[1]
    height = 6371000*arccos(cos((top-bottom)*pi/180))
    width = 6371000*arccos((cos((top*pi/180))**2)*cos((left-right)*pi/180) +
                           (sin((top*pi/180))**2))
    return (right - left) / width, (top - bottom) / height


def get_centers(top_left, bottom_right, r):
    top, left, bottom, right = top_left[0], top_left[1], bottom_right[0], bottom_right[1]
    scale = get_scale(top_left, bottom_right)
    lon_per_meter, lat_per_meter = scale[0], scale[1]
    hex_h = sqrt(3) / 2 * r     # height of the hexagon
    dx = 2 * hex_h * lat_per_meter  # interval between two points in x (latitude)
    dy = 3/2 * r * lon_per_meter      # interval between two points in y (longitude)
    x = top - hex_h * lat_per_meter
    y = left + r/2 * lon_per_meter

    path = [top, left]
    i = -1
    while y + r / 2 * lon_per_meter <= right:
        path.append((x, y))
        y += dy
        x = top - (.5 + .5 * i) * hex_h * lat_per_meter  # (.5+.5*i)=0/1: for columns with more/less hexagons
        i *= -1
    path.append((x, y))

    i = -1
    while y + r/2*lon_per_meter <= right:
        while x-hex_h*lat_per_meter >= bottom:
            path.append((x, y))
            x -= dx
        y += dy
        x = top - (.5 + .5 * i) * hex_h * lat_per_meter  # (.5+.5*i)=0/1: for columns with more/less hexagons
        i *= -1
    print(i)

    path.append((top, left))
    return path


def get_hc(centers):
    path=[]
    return 0


p = get_centers((44.937541, -93.168826), (44.936920, -93.168255), 5)

with open('coord.csv', 'w', newline='') as f:
    w = writer(f)
    w.writerows(p)


