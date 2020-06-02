from math import sqrt, floor
from csv import writer

# get two points in the diagonal
topLeft, bottomRight = (44.924480, -93.161307), (44.923933, -93.159719)

top = topLeft[0]
left = topLeft[1]
bottom = bottomRight[0]
right = bottomRight[1]

box = [(top, left), (top, right), (bottom, right), (bottom, left), (top, left)]

with open('box.csv', 'w', newline='') as f:
    w = writer(f)
    w.writerows(box)

# read x, y in Flylitchi
x = 125.2
y = 60.9

# set the radius
r = 10

long_per_meter = (right-left)/x
lat_per_meter = (top-bottom)/y


def get_path(top, bottom, left, x, r):
    origin = (top, left)
    path = [origin]
    dy = 3/2*r*long_per_meter
    hex_h = sqrt(3) / 2 * r
    x1 = origin[0] - hex_h * lat_per_meter
    y1 = origin[1] + r/2 * long_per_meter
    for i in range(floor((x - r / 2) / (dy/long_per_meter))):
        path.append((x1, y1))
        y1 += dy
        if x1 == origin[0] - hex_h * lat_per_meter:
            x1 = origin[0]
        else:
            x1 = origin[0] - hex_h * lat_per_meter
    path.append((x1, y1))

    dx = 2 * hex_h * lat_per_meter
    s = -1
    x2 = x1
    while y1 > left:
        if s == -1:
            while (x2-dx-hex_h*lat_per_meter) > bottom:
                x2 -= dx
                path.append((x2, y1))
            x2 = x1
        else:
            temp = []
            x2 = top-hex_h*lat_per_meter
            while (x2-dx-hex_h*lat_per_meter) > bottom:
                x2 -= dx
                temp.append((x2, y1))
            temp.reverse()
            path.extend(temp)
            x2 = x1
        s *= -1
        y1 -= dy

    path.append(origin)
    return path


HC = get_path(top, bottom, left, x, r)
with open('coord.csv', 'w', newline='') as f:
    w = writer(f)
    w.writerows(HC)

