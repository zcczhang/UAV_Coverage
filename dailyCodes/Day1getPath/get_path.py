from numpy import *
from csv import writer

"""
:input data
"""
top_left, bottom_right = (44.937541, -93.168826), (44.936920, -93.168255)   # diagonal points
r = 6       # set the radius
"""
:parameters
"""
top, left, bottom, right = top_left[0], top_left[1], bottom_right[0], bottom_right[1]
height = 6371000*arccos(cos((top-bottom)*pi/180))
width = 6371000*arccos((cos((top*pi/180))**2)*cos((left-right)*pi/180) +
                       (sin((top*pi/180))**2))
lon_per_meter = (right - left) / width
lat_per_meter = (top-bottom)/height
path = [(top, left)]  # list of tuples which stored coordinates
hex_h = sqrt(3) / 2 * r  # height of the hexagon
dx = 2 * hex_h * lat_per_meter  # interval between two points in latitude
dy = 3 / 2 * r * lon_per_meter  # interval between two points in longitude
x1 = top - hex_h * lat_per_meter  # now is the second point
y1 = left + r / 2 * lon_per_meter
"""
:create path
"""
# get the first row
i = -1
while y1 + dy + r / 2 * lon_per_meter <= right:
    path.append((x1, y1))
    y1 += dy
    x1 = top - (.5 + .5 * i) * hex_h * lat_per_meter  # (.5+.5*i)=0/1: for columns with more/less hexagons
    i *= -1
# get the rest of the path
k = 1
while y1 > left:
    temp = []
    while x1 + hex_h * lat_per_meter > bottom:
        temp.append((x1, y1))
        x1 -= dx
    if k == -1:
        temp.reverse()
    path.extend(temp)
    x1 = top - (2.5 + .5 * k) * hex_h * lat_per_meter  # (2.5+.5*i)=0/1: for columns with more/less hexagons
    k *= -1
    y1 -= dy
path.append((top, left))
"""
:save coordinates
"""
with open('coord.csv', 'w', newline='') as f:
    w = writer(f)
    w.writerows(path)

