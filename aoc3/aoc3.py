#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 09:14:47 2019

@author: robertnolet
"""

import re

dirs = {'D' : (0,-1),
        'L' : (-1,0),
        'R' : (+1,0),
        'U' : (0,+1)}
pat = re.compile('([DLRU])(\d+)')


def dist(p):
    return abs(p[0]) + abs(p[1])

def create_path(ls):
    route = map(lambda r: (dirs[r.group(1)], int(r.group(2))), map(pat.match, ls))
    (x,y) = (0,0)
    path = []
    for (d, l) in route:
        path.extend([(x + i*d[0], y + i*d[1]) for i in range(1,l+1)])
        x += l*d[0]
        y += l*d[1]
    return path
    

#test1 = 'R75,D30,R83,U83,L12,D49,R71,U7,L72'
#test2 = 'U62,R66,U55,R34,D71,R55,D58,R83'
#path1 = create_path(test1.split(','))
#path2 = create_path(test2.split(','))

f = open('input.txt')
path1 = create_path(f.readline().split(','))
path2 = create_path(f.readline().split(','))

lp = set(path1).intersection(set(path2))

# Answer part 1
print min(dist(p) for p in lp)

# Answer part 2
print min(path1.index(p) + path2.index(p) for p in lp) + 2