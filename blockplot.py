import cairocffi as cairo
import math
from itertools import zip_longest

from drawutils import *

def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

DATAX = [(('Germany','Germany','Germany'),
         ('United States','Germany','Germany'),
         ('United States','Germany','United States')),
         (('Sweden','Sweden','Sweden'),
         ('United States','Sweden','Sweden'),
         ('United States','Sweden','United States')),
         (('Norway','Norway','Norway'),
         ('Sweden','Sweden','Sweden'),
         ('United States','Norway','Sweden'))]

MAPX = {'Norway':[(1,0,0),(1,.5,.5),(1,.75,.75)],
        'Sweden': [(0,0,1),(.5,.5,1),(.75,.75,1)],
        'Germany': [(1,1,0), (1,1,.5),(1,1,.75)],
        'United States': [(.75,.75,.75),(.75,.75,.75),(.75,.75,.75)]}

def get_colors(ethn):
    if ethn[0] != 'United States':
        return (MAPX[ethn[0]][0],MAPX[ethn[0]][0])
    else:
        return (MAPX[ethn[1]][1], MAPX[ethn[2]][1])

colormap = {'a':(1,0,0),
            'b':(0,1,0),
            'c':(.5,.5,1),
            'd':(1,.5,.5),
            'e':(.5,1,.5),
            'f':(1,1,.5),
            'g':(.5,1,1)}


RAD = 0.45
SPACING = 0.1
N_PER_ROW = 2

def circle_group(ctx, plot_data, color_map):
    j = 1
    for group in grouper(plot_data,N_PER_ROW):
        i = 0
        for code in group:
            if not code: return
            i += 1
            circle(ctx, i, j, RAD, color_map[code])
        j += 1

def split_circle_group(ctx, plot_data):
    j = 1
    for group in grouper(plot_data,N_PER_ROW):
        i = 0
        for code in group:
            if not code: return
            print(code)
            i += 1
            split_circle(ctx, i, j, RAD, code[0],code[1])
        j += 1


def group_center(data):
    n_rows = math.ceil(len(data) / N_PER_ROW)
    n_cols = min(len(data), N_PER_ROW)
    return (n_cols/2 + .5, n_rows / 2 + .5)





WIDTH, HEIGHT = 256, 256

surface = cairo.PDFSurface ("example.pdf", WIDTH, HEIGHT)
ctx = cairo.Context (surface)

ctx.scale (WIDTH/6, HEIGHT/6) # Normalizing the canvas

data = DATAX[2]

ctx.push_group()
split_circle_group(ctx, [get_colors(x) for x in data])
x, y = group_center(data)
print(x,y)
n_cols = min(len(data), N_PER_ROW)
n_rows = math.ceil(len(data) / N_PER_ROW)
#path_ellipse(ctx, x, y, n_cols+.75, math.ceil(len(data) / N_PER_ROW) + .75)
rounded_rect(ctx, 1-(RAD+SPACING), 1-(RAD+SPACING), n_cols+SPACING,  n_rows+SPACING)
ctx.set_line_width(0.05)
ctx.set_dash((.2,.2))
ctx.stroke()

group = ctx.pop_group()
#group.set_matrix(cairo.Matrix())
m = group.get_matrix()
m.translate(-1,-1)
group.set_matrix(m)
ctx.set_source(group)
ctx.paint_with_alpha(1)

grid_points(ctx)
surface.finish()
