"""
__author__ = "Charles Zhang"
__time__ = "2020-06-04 19:53"
"""
from numpy import *
from csv import writer
"""
:input data
"""
# get two points in the diagonal
top_left, bottom_right = (44.924480, -93.161307), (44.923933, -93.159719)

# top_left, bottom_right = (44.937541, -93.168826), (44.936920, -93.168255)
# top_left, bottom_right = (44.937334, -93.168802), (44.937175, -93.168317)
# top_left, bottom_right = (44.937363, -93.168796), (44.937048, -93.168330)
# set the radius
r = 8
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
i = -1      # -1/1 for columns with less/more hexagons
while y1 + hex_h * lon_per_meter <= right:
    path.append((x1, y1))
    y1 += dy
    x1 = top - (.5 + .5 * i) * hex_h * lat_per_meter
    i *= -1
path.append((x1, y1))
# get the rest of the HC path
x1 = top - (2.5+.5*i) * hex_h * lat_per_meter
y1 = left + (1.25-.75*i) * r * lon_per_meter
x2 = x1
rest_path = []
k = i
# special situation for the last two columns
if k == -1:
    while x1 >= bottom:
        rest_path.append((x1, y1))
        x1 -= hex_h*lat_per_meter
        y1 += k*dy
        k *= -1
    x1 = top - 3 * hex_h * lat_per_meter
    y1 = left + 7/2 * r * lon_per_meter
    k *= -1

while y1 - r/2*lon_per_meter <= right:
    temp = []
    while x1 > bottom:
        temp.append((x1, y1))
        x1 -= dx
    if i == -1:
        temp.reverse()
    rest_path.extend(temp)
    x1 = x2 + k * (.5 + .5 * i) * hex_h * lat_per_meter
    i *= -1
    y1 += dy
rest_path.reverse()
path.extend(rest_path)
path.append((top, left))
# save coordinates
with open('coord.csv', 'w', newline='') as f:
    w = writer(f)
    w.writerows(path)

