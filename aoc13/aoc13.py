#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 10:30:02 2019

@author: robertnolet
"""

import sys
sys.path.append('../IntCode')
import IntCode
from itertools import ifilter
import matplotlib.pyplot as plt
import numpy as np

def plotscreen(tiles):
    xmax = max(x for (x, y, tile) in tiles)
    ymax = max(y for (x, y, tile) in tiles)
    grid = np.zeros((ymax+1, xmax+1))
    for (x, y, tile) in tiles: grid[y,x] = tile
    plt.imshow(grid)
    
def triples(it):
    for i in it:
        yield (i, it.next(), it.next())

def move(ball, paddle):
    if ball > paddle: return 1
    if ball < paddle: return -1
    return 0

# Answer part 1        
print sum(tile == 2 for (x, y, tile) in triples(IntCode.fromfile('input.txt')))

# Answer part 2
# Setup game
inp = []
code = IntCode.fromfile('input.txt', iter(inp))
code.mem[0] = 2

# We're actually not interested in blocks or walls, only in score and
# ball/paddle positions, so we filter those out.
it = ifilter(lambda t: (t[0] == -1) or (t[2] in [3,4]), triples(code))

# Read initial ball and paddle position
for i in range(2):
    (x, y, tile) = it.next()
    if tile == 4: ball = x
    elif tile == 3: paddle = x
    
# Set first move
inp.append(move(ball, paddle))

# Play by keeping paddle always under ball
for (x, y, tile) in it:
    if x == -1:
        score = tile
    elif tile == 3:
        paddle = x
    elif tile == 4:
        ball = x
        inp.append(move(ball, paddle))
print score
