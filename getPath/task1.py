from math import sqrt, floor
from csv import writer

# get two points in the diagonal
topLeft, bottomRight = (44.937541, -93.168826), (44.936920, -93.168255)

top = topLeft[0]
left = topLeft[1]
bottom = bottomRight[0]
right = bottomRight[1]

box = [(top, left), (top, right), (bottom, right), (bottom, left), (top, left)]

with open('box.csv', 'w', newline='') as f:
    w = writer(f)
    w.writerows(box)

# read x, y in Flylitchi
x = 45
y = 69.1

# set the radius
r = 5

long_per_meter = (right-left)/x
lat_per_meter = (top-bottom)/y


def get_path(top, bottom, left, x, r):
    origin = (top, left)
    path = [origin]             # list of tuples which stored coordinates
    dy = 3/2*r*long_per_meter   # interval between two points in y in longitude
    hex_h = sqrt(3) / 2 * r     # height of the hexagon
    x1 = origin[0] - hex_h * lat_per_meter      # now is the second point
    y1 = origin[1] + r/2 * long_per_meter
    # get the first two rows
    for i in range(floor((x - r / 2) / (dy/long_per_meter))):
        path.append((x1, y1))
        y1 += dy
        if x1 == origin[0] - hex_h * lat_per_meter:
            x1 = origin[0]
        else:
            x1 = origin[0] - hex_h * lat_per_meter
    path.append((x1, y1))
    # get the rest of the path
    dx = 2 * hex_h * lat_per_meter      # interval between two points in x in latitude
    s = -1      # a parameter to see if
    x2 = x1
    # from the right to left
    while y1 > left:
        if s == -1:
            # from the top to bottom
            while (x2-hex_h*lat_per_meter) > bottom:
                x2 -= dx
                path.append((x2, y1))
            x2 = x1
        else:
            # from the bottom to top
            temp = []
            x2 = top-hex_h*lat_per_meter
            while (x2-hex_h*lat_per_meter) > bottom:
                x2 -= dx
                temp.append((x2, y1))
            temp.reverse()
            path.extend(temp)
            x2 = x1
        s *= -1
        y1 -= dy
    # finish the path and get back to the origin
    path.append(origin)
    return path


HC = get_path(top, bottom, left, x, r)
with open('coord.csv', 'w', newline='') as f:
    w = writer(f)
    w.writerows(HC)

