#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 09:14:47 2019

@author: robertnolet
"""

import re

# Map directions D, L, R, U to tuples (dx,dy)
dirs = {'D' : (0,-1),
        'L' : (-1,0),
        'R' : (+1,0),
        'U' : (0,+1)}

# Regular expression for parsing direction+length strings
pat = re.compile('([DLRU])(\d+)')

# Manhatten distance
def dist(p):
    return abs(p[0]) + abs(p[1])

# Create a list of points (x,y) from a list of direction+length strings
def create_path(ls):
    # Map the list of direction strings to a list of tuples ((dx,dy), length)
    route = map(lambda r: (dirs[r.group(1)], int(r.group(2))), map(pat.match, ls))
    
    # Set origin of path
    (x,y) = (0,0)
    path = []
    
    # Extend path for each direction in route
    for ((dx, dy), l) in route:
        path.extend([(x + i*dx, y + i*dy) for i in range(1,l+1)])
        x += l*dx
        y += l*dy
    return path
    

#test1 = 'R75,D30,R83,U83,L12,D49,R71,U7,L72'
#test2 = 'U62,R66,U55,R34,D71,R55,D58,R83'
#path1 = create_path(test1.split(','))
#path2 = create_path(test2.split(','))

f = open('input.txt')
path1 = create_path(f.readline().split(','))
path2 = create_path(f.readline().split(','))

# Intersection points
ips = set(path1).intersection(set(path2))

# Answer part 1
print min(dist(p) for p in ips)

# Answer part 2
print min(path1.index(p) + path2.index(p) for p in ips) + 2