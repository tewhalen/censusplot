import cairocffi as cairo
import math, itertools
from drawutils import grid_points

def lat2y(a):
    "Spherical Pseudo-Mercator projection"
    return 180.0/math.pi*math.log(math.tan(math.pi/4.0+a*(math.pi/180.0)/2.0))


TEST_DATA = {1903:((41.9776029, -87.6767852),
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
(41.9776029, -87.6767852)),
1907:((41.9776006, -87.6768643),
(41.9776734, -87.6768672),
(41.9776803, -87.67688),
(41.9777681, -87.6768828),
(41.9777692, -87.6768331),
(41.9777555, -87.6768314),
(41.9777567, -87.6768112),
(41.9777471, -87.6768002),
(41.977673, -87.676801),
(41.977662, -87.6767938),
(41.977603, -87.6767907),
(41.9776006, -87.6768643)),
1911:((41.9776182, -87.6770608),
(41.9777664, -87.6770648),
(41.9777674, -87.6769876),
(41.9776411, -87.6769834),
(41.9776399, -87.6770073),
(41.9776193, -87.6770075),
(41.9776182, -87.6770608)),
1917:((41.9776508, -87.6772462),
(41.9777442, -87.6772489),
(41.9777464, -87.677168),
(41.9776517, -87.6771653),
(41.9776508, -87.6772462)),
1916:((41.9780114, -87.6771929),
(41.9780115, -87.6772149),
(41.9780184, -87.6772222),
(41.9780186, -87.6772498),
(41.9780543, -87.6772513),
(41.9780625, -87.6772604),
(41.9781257, -87.6772616),
(41.9781338, -87.6772505),
(41.9781709, -87.6772519),
(41.9781719, -87.6771839),
(41.9780223, -87.6771799),
(41.9780114, -87.6771929))}

WIDTH, HEIGHT = 256, 256

surface = cairo.PDFSurface ("test_building.pdf", WIDTH, HEIGHT)
ctx = cairo.Context (surface)


class Normer:
    def __init__(self, coord_set):
        self.coord_set = coord_set
        xes = [x[1]  for x in itertools.chain.from_iterable(coord_set)]
        yys = [lat2y(x[0]) * -1 for x in itertools.chain.from_iterable(coord_set)]
        self.minx = min(xes)
        self.miny = min(yys)

        rx = max(xes) - self.minx
        ry = max(yys) - self.miny
        self.fact = max(rx, ry)

    def norm(self, coords, new_range):
        ncords = [((x - self.minx) / self.fact * new_range,
                  (lat2y(y) *  -1 - self.miny) / self.fact * new_range) for y,x in coords]
        return ncords

def draw_building(normed):
    ctx.save()
    ctx.move_to(*normed[0])
    for x,y in normed[1:]:
        ctx.line_to(x,y)
    ctx.set_line_width(0.025)
    ctx.set_source_rgb(0,0,0)
    ctx.stroke_preserve()
    ctx.set_source_rgb(.9,.9,.9)
    ctx.fill()
    ctx.restore()

normer = Normer(TEST_DATA.values())
ctx.scale (WIDTH/10, HEIGHT/10) # Normalizing the canvas

for addr, building in TEST_DATA.items():
    draw_building(normer.norm(building, 10))

grid_points(ctx)
