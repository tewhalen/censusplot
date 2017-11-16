import cairocffi as cairo
import math
from drawutils import grid_points

def lat2y(a):
    "Spherical Pseudo-Mercator projection"
    return 180.0/math.pi*math.log(math.tan(math.pi/4.0+a*(math.pi/180.0)/2.0))



d = [(41.9776029, -87.6767852),
(41.9776564, -87.6767865),
(41.9776714, -87.6767698),
(41.9776893, -87.6767714),
(41.977688, -87.676788),
(41.9777511, -87.676791),
(41.9777523, -87.6767561),
(41.9777577, -87.676745),
(41.9777576, -87.6767247),
(41.9777507, -87.6767101),
(41.9776052, -87.6767061),
(41.9776029, -87.6767852)]

WIDTH, HEIGHT = 256, 256

surface = cairo.PDFSurface ("test_building.pdf", WIDTH, HEIGHT)
ctx = cairo.Context (surface)


def norm_latlong(coords, new_range):

    xes = [x[1]  for x in coords]
    yys = [lat2y(x[0]) * -1 for x in coords]
    minx = min(xes)
    miny = min(yys)

    nxes = [x - minx for x in xes]
    nyys = [y - miny for y in yys]
    rx = max(nxes)
    ry = max(nyys)
    fact = max(rx, ry)

    normed_x = [n/ fact * new_range  for n in nxes]
    normed_y = [n/ fact * new_range  for n in nyys]

    return list(zip(normed_x, normed_y))

normed = norm_latlong(d, 10)

ctx.scale (WIDTH/10, HEIGHT/10) # Normalizing the canvas

ctx.move_to(*normed[0])
for x,y in normed[1:]:
    print(x,y)
    ctx.line_to(x,y)
ctx.set_line_width(0.025)
ctx.set_source_rgb(0,0,0)
ctx.stroke_preserve()
ctx.set_source_rgb(.9,.9,.9)
ctx.fill()

grid_points(ctx)
