#!/usr/bin/python3

import contextlib
import math

diameter = 140 # mm
rings = 10
black_rings = 4
stroke_width = 0.5 # mm
padding = 15 # percent of diameter (on each side)
font_family = "Verdana"
font_size = 60 # percent of ring size

def escape(s):
    escapes = {"&": "&amp;",
               '"': "&quot;",
               "'": "&apos;",
               ">": "&gt;",
               "<": "&lt;"}

    return "".join(escapes.get(c, c) for c in s)

@contextlib.contextmanager
def tag(name, **parameters):
    print("<" + name + "".join(" " + k + '="' + escape(str(v)) + '"' for k, v in parameters.items()) + ">", end="")
    yield
    print("</" + name + ">", end="")

def c(black):
    if black:
        return "black"
    else:
        return "white"

def mm(n):
    return "{:.2f}mm".format(n)

size = diameter * (1 + padding / 50)
offset = size / 2
ring_size = diameter / (2 * rings - 1)
font_size = font_size * ring_size / 100
with tag("svg", xmlns="http://www.w3.org/2000/svg",
         width=mm(size), height=mm(size)):
    for i in reversed(range(rings)):
        r = (i + 0.5) * ring_size
        text_r = i * ring_size
        black = i < (rings - black_rings) and i > 0
        with tag("g"):
            with tag("circle",
                     cx=mm(offset), cy=mm(offset),
                     r=mm(r),
                     fill=c(black),
                     stroke=c(not black),
                     stroke_width=mm(stroke_width)):
                pass
            for j in range(4):
                alpha = math.pi * j / 2
                with tag("text",
                         x=mm(offset + math.cos(alpha) * text_r),
                         y=mm(offset + math.sin(alpha) * text_r + font_size * 0.3),
                         fill=c(not black),
                         **{"text-anchor": "middle",
                            "font-family": font_family,
                            "font-size": mm(font_size)}):
                    print(rings - i, end="")
