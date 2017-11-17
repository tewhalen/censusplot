import cairocffi as cairo
import math, itertools, csv, collections
from drawutils import grid_points

from blockplot import plot_household
import osm_building

def lat2y(a):
    "Spherical Pseudo-Mercator projection"
    return 180.0/math.pi*math.log(math.tan(math.pi/4.0+a*(math.pi/180.0)/2.0))



def coord_min(coord_set):
    return (min(x[0] for x in coord_set), min(x[1] for x in coord_set))

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

    def norm_single(self, pair, new_range):
        return self.norm([pair], new_range)[0]

def building_outlines(b_info):
    outlines = {}
    for w in b_info.ways:
        key = (w.tags['addr:housenumber'], w.tags['addr:street:prefix'], w.tags['addr:street:name'])
        outlines[key] = [(float(n.lat), float(n.lon)) for n in w.get_nodes()]
    return outlines

def draw_building(ctx, normed):
    ctx.save()
    ctx.move_to(*normed[0])
    for x,y in normed[1:]:
        ctx.line_to(x,y)
    ctx.set_line_width(0.025)
    ctx.set_source_rgb(0,0,0)
    ctx.stroke_preserve()
    ctx.set_source_rgb(.95,.95,.95)
    ctx.fill()
    ctx.restore()

if __name__ == '__main__':
    WIDTH, HEIGHT = 256, 256

    surface = cairo.PDFSurface ("test_building.pdf", WIDTH, HEIGHT)
    ctx = cairo.Context (surface)

    # read csv
    with open('berwynblocks.csv') as f:
        reader = csv.DictReader(f)
        raw_data = [row for row in reader]
    info = collections.defaultdict(lambda: collections.defaultdict(list))
    for row in raw_data:
        info[(row['housenumber'], row['prefix'], row['street'])][row['household_id']].append(row)
    print(info.keys())
    # query OSM for the building outlines
    building_info = osm_building.query_buildings('Chicago',info.keys())
    outlines = building_outlines(building_info)
    normer = Normer(outlines.values())
    ctx.scale (WIDTH/10, HEIGHT/10) # Normalizing the canvas

    for addr, building in outlines.items():
        draw_building(ctx, normer.norm(building, 10))


    glyph_groups = []
    for key, choice in info.items():
        ctx.push_group()
        print(key)
        plot_household(ctx, choice)
        group = ctx.pop_group()
        m = group.get_matrix()
        q1 = coord_min(normer.norm(outlines[key],10))
        print(q1)
        m.scale(3.4,3.4)
        m.translate(-q1[0]+.1,-q1[1]+.1)


        group.set_matrix(m)
        glyph_groups.append(group)
    for group in glyph_groups:
        ctx.set_source(group)
        ctx.paint()


    #grid_points(ctx)
