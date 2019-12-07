#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 09:11:43 2019

@author: robertnolet
"""

import re

def dist(orbits, start = 'COM', dest = None):
    """ Calculate distance from start to dest using Dijkstra's
    algorithm. If dest = None, all distances are calculated and
    returned as a dictionary."""
    result = {start : 0}
    update = set(orbits[start])
    d = 1
    while (update):
        new_update = set()
        for u in update:
            if (u == dest): return d
            result[u] = d
            new_update.update({s for s in orbits[u] if not result.has_key(s)})
        update = new_update
        d += 1
    return result

def calculate_orbits(orbitdata):
    """ Create a dictionary from the orbit data having as key all the orbits
    in orbitdata, and as value a list of all connected orbits."""
    orbits = {}
    for (s, d) in orbitdata:
        if not orbits.has_key(s): orbits[s] = []
        if not orbits.has_key(d): orbits[d] = []
        orbits[s].append(d)
        orbits[d].append(s)
    return orbits
                
        
pat = re.compile(r'(\w+)\)(\w+)')
orbitdata = [pat.match(line).groups() for line in open('input.txt')]
orbits = calculate_orbits(orbitdata)

# Answer part 1
print sum(dist(orbits).values())

# Answer part 2
print dist(orbits, 'SAN', 'YOU') - 2

