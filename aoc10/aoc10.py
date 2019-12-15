#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 09:40:47 2019

@author: robertnolet
"""

import numpy as np
from itertools import combinations

# Calculate the greatest common denominator of a and b
def gcd(a,b):
    if b==0: return a
    return gcd(b, a%b)

# Count the number of objects between coordinates c1 and c2 in data
def n_between(c1, c2, data):
    g = gcd(abs(c1[0]-c2[0]), abs(c1[1] - c2[1]))
    dx = (c2[1] - c1[1])/g
    dy = (c2[0] - c1[0])/g
    return sum(data[c1[0]+i*dy, c1[1]+i*dx] == '#' for i in range(1,g))
    
# Calculate at which angle, clockwise from up, coordinates c1 are as seen from mc
def angle(mc, c1):
    dy = c1[0] - mc[0]
    dx = c1[1] - mc[1]
    a = -np.arctan2(-dx, -dy)
    return a if a >= 0 else a + 2*np.pi
 
# Load data    
data = np.array([list(line.strip()) for line in open('input.txt')])
coords = map(list, np.argwhere(data == '#'))

# Count how many other asteroids each asteroid can 'see'  
counts = np.zeros(len(coords), dtype = int)                   
for ((i,c1), (j,c2)) in combinations(enumerate(coords), 2):
    if n_between(c1, c2, data) == 0: counts[[i,j]] += 1

# Answer part 1
mc = coords[np.argmax(counts)]
print (max(counts), mc)

# Answer part 2
order = sorted([(n_between(mc, c1, data), 
                 angle(mc, c1), 
                 100*c1[1]+c1[0])
                 for c1 in coords if (c1 != mc)])
print order[199]

        
