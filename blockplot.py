import cairocffi as cairo
import math
from itertools import zip_longest
import csv, collections


from drawutils import *

def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

MAPX = {'Norway':[(1,0,0),(1,.5,.5),(1,.75,.75)],
        'Sweden': [(0,0,1),(.5,.5,1),(.75,.75,1)],
        'Germany': [(1,1,0), (1,1,.5),(1,1,.75)],
        'United States': [(.75,.75,.75),(.75,.75,.75),(.75,.75,.75)],
        "England": [(1,.569,.302),(1,.691,.5),(1,.768,.625)],
        'Finland': [(1,.253,1),(1,.468,1),(1,.67,1)],
        'Ireland':[(0,1,0),(.5,1,.5),(.75,1,.75)],
        'Luxembourg':[(.78,.78,.19),(.78,.78,.4),(.78,.78,.6)],
        'Denmark':[(1,0,1),(1,.5,1),(1,.75,1)]}

def get_colors(ethn):
    default = ((.9,.9,.9), (.9,.9,.9))
    if ethn[0] != 'United States':
        return (MAPX.get(ethn[0], default)[0],MAPX.get(ethn[0], default)[0])
    else:
        return (MAPX.get(ethn[1], default)[1], MAPX.get(ethn[2], default)[1])

RAD = 0.45
SPACING = 0.1
N_PER_ROW = 2

def split_circle_group(ctx, plot_data):
    j = 1
    for group in grouper(plot_data,N_PER_ROW):
        i = 0
        for code in group:
            if not code: return
            i += 1
            split_circle(ctx, i, j, RAD, code[0],code[1])
        j += 1



def plot_household(ctx, household_data):
    last_row = 0
    draw_groups = []
    for household, d in household_data.items():
        data = [(x['birthplace'],x['birthplace_father'],x['birthplace_mother']) for x in d]
        ctx.push_group()
        split_circle_group(ctx, [get_colors(x) for x in data])
        n_cols = min(len(data), N_PER_ROW)
        n_rows = math.ceil(len(data) / N_PER_ROW)
        rounded_rect(ctx, 1-(RAD+SPACING/2), 1-(RAD+SPACING/2), n_cols,  n_rows)
        ctx.set_line_width(0.025)
        ctx.set_dash((.2,.2))
        ctx.stroke()

        group = ctx.pop_group()
        m = group.get_matrix()
        m.translate(0,last_row)
        last_row -= n_rows
        group.set_matrix(m)
        draw_groups.append(group)
    for group in draw_groups:
        ctx.set_source(group)
        ctx.paint()

if __name__ == '__main__':
    WIDTH, HEIGHT = 256, 256

    surface = cairo.PDFSurface ("example.pdf", WIDTH, HEIGHT)
    ctx = cairo.Context (surface)

    ctx.scale (WIDTH/10, HEIGHT/10) # Normalizing the canvas
    with open('Summerdale Population - 1920 Census.csv') as f:
        reader = csv.DictReader(f)
        raw_data = [row for row in reader]
    info = collections.defaultdict(lambda: collections.defaultdict(list))
    for row in raw_data:
        info[(row['address'], row['prefix'], row['street'],row['area'])][row['household_id']].append(row)


    choice = list(info.values())[3]


    ctx.push_group()
    plot_household(ctx, choice)
    group = ctx.pop_group()
    ctx.set_source(group)
    ctx.paint()

    #grid_points(ctx)
    surface.finish()
