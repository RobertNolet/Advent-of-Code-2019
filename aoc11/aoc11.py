#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 09:49:43 2019

@author: robertnolet
"""

import sys
sys.path.append('../IntCode')
import IntCode
import numpy as np
import matplotlib.pyplot as plt

def pairs(it):
    for i in it: yield (i, it.next())

class Robot:
    def __init__(self, code, inp = [0], panels = {}):
        (self.dy, self.dx) = (-1,0)
        (self.y , self.x ) = ( 0,0)
        self.panels = panels
        self.inp = inp
        self.code = code
    
    def turn(self, t):
        if   t == 0: (self.dy, self.dx) = (-self.dx,  self.dy)
        elif t == 1: (self.dy, self.dx) = ( self.dx, -self.dy)
        else: print 'Unknown turn direction!'
    
    def move(self, n=1):
        self.y += n*self.dy
        self.x += n*self.dx
    
    def get_color(self):
        return self.panels.get((self.y,self.x),0)
    
    def set_color(self, c):
        self.panels[(self.y,self.x)] = c
        
    def run(self):
        for (c, t) in pairs(self.code):
            self.set_color(c)
            self.turn(t)
            self.move()
            self.inp.append(self.get_color())        
        
    
    
# Answer part 1
inp = [0]
robot = Robot(IntCode.fromfile('input.txt', iter(inp)), inp)
robot.run()
print len(robot.panels)

# Answer part 2
inp = [1]
robot = Robot(IntCode.fromfile('input.txt', iter(inp)), inp, {(0,0):1})
robot.run()

xmin = min(x for (y,x) in robot.panels.keys())
xmax = max(x for (y,x) in robot.panels.keys())
ymin = min(y for (y,x) in robot.panels.keys())
ymax = max(y for (y,x) in robot.panels.keys())
image = np.zeros(((ymax-ymin+1), (xmax-xmin+1)), dtype=int)
for ((y,x), c) in robot.panels.iteritems(): image[y,x] = c
plt.imshow(image)

