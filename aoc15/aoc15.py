#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 11:41:00 2019

@author: robertnolet
"""

import sys
sys.path.append('../IntCode')
import IntCode

dirs = {1 : ( 0,-1),
        2 : ( 0, 1),
        3 : (-1, 0),
        4 : ( 1, 0)}

def findroute(knownmap, newpos, pos = None):
    (x, y) = newpos
    update = {(x+dx, y+dy) for (dx, dy) in dirs.values() 
                           if (knownmap.get((x+dx,y+dy)) == '.')}
    dist = {newpos : 0}
    d = 1
    while update and not dist.has_key(pos):
        for p in update: dist[p] = d
        update = {(x+dx, y+dy) for (x,y) in update for (dx, dy) in dirs.values()
                               if (knownmap.get((x+dx,y+dy)) == '.' 
                               and not dist.has_key((x+dx, y+dy)))}
        d += 1
    if pos == None: return max(dist.values())
    elif not dist.has_key(pos):
        print 'Route not found!'
        return []
    (x,y) = pos
    d = dist[pos]
    result = []
    while d != 0:
        (d, x, y, r) = min((dist.get((x+dx,y+dy),d+1), x+dx, y+dy, r) 
                            for (r, (dx, dy)) in dirs.iteritems())
        result.append(r)
    return result

def printmap(knownmap, pos):
    xmin = min(x for (x,y) in knownmap.keys())
    xmax = max(x for (x,y) in knownmap.keys())
    ymin = min(y for (x,y) in knownmap.keys())
    ymax = max(y for (x,y) in knownmap.keys())
    lines = [list(' '*(xmax-xmin+1)) for y in range(ymin, ymax+1)]
    for ((x,y), t) in knownmap.iteritems():
        lines[y-ymin][x-xmin] = t
    lines[-ymin][-xmin] = 'o'
    lines[pos[1]-ymin][pos[0]-xmin] = 'X'
    print '\n'.join(map(''.join, lines))

inp = []
code = IntCode.fromfile('input.txt', iter(inp))

knownmap = {(0,0) : '.'}
toexplore = dirs.values()
pos = (0,0)
while toexplore:
    newpos = toexplore.pop(0)
    route = findroute(knownmap, newpos, pos)
    inp.extend(route)
    for (r,s) in zip(route[0:-1], code):
        if s == 0: print 'Unexpected wall!'
        (dx, dy) = dirs[r]
        pos = (pos[0]+dx, pos[1]+dy)        
    status = code.next()
    if status == 0:
        knownmap[newpos] = '#'
    elif status == 1:
        knownmap[newpos] = '.'
        pos = newpos
        toexplore.extend([(pos[0]+dx, pos[1]+dy) 
            for (dx, dy) in dirs.values() 
            if not knownmap.has_key((pos[0]+dx, pos[1]+dy))
            and not (pos[0]+dx, pos[1]+dy) in toexplore])
    elif status == 2:
        knownmap[newpos] = 'O'
        pos = newpos
        toexplore.extend([(pos[0]+dx, pos[1]+dy) 
            for (dx, dy) in dirs.values() 
            if not knownmap.has_key((pos[0]+dx, pos[1]+dy))
            and not (pos[0]+dx, pos[1]+dy) in toexplore])
        oxypos = pos
        break
printmap(knownmap, pos)
print len(findroute(knownmap, (0,0), oxypos))


# Reset IntCode, since it terminates after finding oxygen, but keep known map.
inp = []
code = IntCode.fromfile('input.txt', iter(inp))
pos = (0,0)

# Make sure the rover doesn't cross the oxygen while exploring.
for (dx, dy) in dirs.values():
    if (oxypos[0]+dx, oxypos[1]+dy) in toexplore:
        toexplore.remove((oxypos[0]+dx, oxypos[1]+dy))


while toexplore:
    newpos = toexplore.pop(0)
    route = findroute(knownmap, newpos, pos)
    inp.extend(route)
    for (r,s) in zip(route[0:-1], code):
        if s == 0: print 'Unexpected wall!'
        (dx, dy) = dirs[r]
        pos = (pos[0]+dx, pos[1]+dy)        
    status = code.next()
    if status == 0:
        knownmap[newpos] = '#'
    elif status == 1:
        knownmap[newpos] = '.'
        pos = newpos
        toexplore.extend([(pos[0]+dx, pos[1]+dy) 
            for (dx, dy) in dirs.values() 
            if not knownmap.has_key((pos[0]+dx, pos[1]+dy))
            and not (pos[0]+dx, pos[1]+dy) in toexplore])
printmap(knownmap, pos)

print findroute(knownmap, oxypos)
   
    
        