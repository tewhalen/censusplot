import cairocffi as cairo
import math
from itertools import zip_longest

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

def circle(ctx,x,y,radius, fill_color):
    ctx.save()
    ctx.set_line_width(0.05)
    ctx.set_source_rgb(0,0,0)
    ctx.arc(x, y, radius, 0, 2*math.pi)
    ctx.stroke_preserve()
    ctx.set_source(cairo.SolidPattern(*fill_color))
    ctx.fill()
    ctx.restore()

def split_circle(ctx, x, y, radius, fill_color_a, fill_color_b):
    ctx.save()
    ctx.move_to(x,y)
    ctx.arc(x, y, radius, math.pi/2, 3*math.pi/2)
    ctx.line_to(x,y+radius)
    ctx.set_source(cairo.SolidPattern(*fill_color_a))
    ctx.fill()

    ctx.move_to(x,y)
    ctx.arc(x,y, radius, 3*math.pi/2, math.pi/2)
    ctx.line_to(x,y-radius)
    ctx.set_source(cairo.SolidPattern(*fill_color_b))
    ctx.fill()

    outline = True

    if outline:
        ctx.set_line_width(0.05)
        ctx.set_source_rgb(0,0,0)
        ctx.arc(x, y, radius, 0, 2*math.pi)
        ctx.stroke()
    ctx.restore()

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

def path_ellipse(cr, x, y, width, height, angle=0):
    """
    x      - center x
    y      - center y
    width  - width of ellipse  (in x direction when angle=0)
    height - height of ellipse (in y direction when angle=0)
    angle  - angle in radians to rotate, clockwise
    """
    cr.save()
    cr.translate(x, y)
    cr.rotate(angle)
    cr.scale(width / 2.0, height / 2.0)
    cr.arc(0.0, 0.0, 1.0, 0.0, 2.0 * math.pi)
    cr.restore()

def rounded_rect(cr, x, y, width, height):
    radius = height / 10.0
    degrees = math.pi / 180

    cr.save()
    cr.arc(x + width - radius, y + radius, radius, -90 * degrees, 0)
    cr.arc(x + width - radius, y + height - radius, radius, 0 * degrees, 90 * degrees)
    cr.arc(x + radius, y + height - radius, radius, 90 * degrees, 180 * degrees)
    cr.arc(x + radius, y + radius, radius, 180 * degrees, 270 * degrees)
    cr.close_path()
    cr.restore()


def grid_points(cr):
    """helpful for debugging"""
    for x in range(6):
        for y in range(6):
            circle(cr, x,y,0.01,(0,0,0))

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

#grid_points(ctx)

surface.finish()
