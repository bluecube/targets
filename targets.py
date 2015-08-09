#!/usr/bin/python3

import math
import microsvg

mm = microsvg.mm

diameter = 140 # mm
rings = 10
white_rings = rings // 2
stroke_width = 0.5 # mm
padding = 15 # percent of diameter (on each side)
font_family = "Verdana"
font_size = 60 # percent of ring size

def c(black):
    if black:
        return "black"
    else:
        return "white"
size = diameter * (1 + padding / 50)
offset = size / 2
ring_size = diameter / (2 * rings - 1)
font_size = font_size * ring_size / 100
with microsvg.Svg(width=mm(size), height=mm(size)) as image:
    for i in reversed(range(rings)):
        r = (i + 0.5) * ring_size
        text_r = i * ring_size
        black = i < white_rings and i > 0
        with image.tag("g") as group:
            group.circle(mm(offset), mm(offset),mm(r),
                         fill=c(black),
                         stroke=c(not black),
                         stroke_width=mm(stroke_width))

            if i == 0:
                group.line(mm(offset - ring_size / 2), mm(offset),
                           mm(offset + ring_size / 2), mm(offset),
                           stroke_width=mm(stroke_width),
                           stroke=c(not black))
                group.line(mm(offset), mm(offset - ring_size / 2),
                          mm(offset), mm(offset + ring_size / 2),
                          stroke_width=mm(stroke_width),
                          stroke=c(not black))
            else:
                for j in range(4):
                    alpha = math.pi * j / 2
                    group.text(rings - i,
                               mm(offset + math.cos(alpha) * text_r),
                               mm(offset + math.sin(alpha) * text_r + font_size * 0.3),
                               fill=c(not black),
                               text_anchor = "middle",
                               font_family = font_family,
                               font_size = mm(font_size))
