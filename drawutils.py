#!/usr/bin/env python3

import cairocffi as cairo
import math

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
            cr.arc(x, y, 0.025, 0, 2*math.pi)
            cr.set_source_rgb(0,0,0)
            cr.fill()
