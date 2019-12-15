#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 08:51:45 2019

@author: robertnolet
"""

import re
from itertools import combinations
import numpy as np

# Calculate the greatest common denominator of a and b
def gcd(a,b):
    if b==0: return a
    return gcd(b, a%b)

def diffmatrix(x):
    result = np.zeros((len(x[0]), 4, 4))
    for (i,j) in combinations(range(4), 2):
        result[:,i,j] = x[i,:] - x[j,:]
        result[:,j,i] = x[j,:] - x[i,:]
    return result

def acc(x):
    a = np.zeros(x.shape, dtype = int)
    for (i,j) in combinations(range(4),2):
        a[i][x[i] > x[j]] -= 1
        a[i][x[i] < x[j]] += 1
        a[j][x[i] > x[j]] += 1
        a[j][x[i] < x[j]] -= 1
    return a
   
def step(x, v, t, dt = None):
    a = acc(x)
    dx = diffmatrix(x)
    if (dt == None) and np.any(dx + [np.eye(4, dtype=int)]*len(x[0]) == 0):
        dt = 1
    elif (dt == None):
        dv = diffmatrix(v)
        da = diffmatrix(a)
        n = np.ones((len(x[0]),4,4))
        n[(da == 0) & (dv != 0)] = -dx[(da==0) & (dv != 0)]/dv[(da==0) & (dv != 0)]   
        n[(da == 0) & (dv == 0)] = 1000
        disc = (2*dv + da)**2 - 8*da*dx
        w = (da != 0) & (disc >= 0)
        n[w & (dx>0)] = -0.5 - dv[w & (dx>0)]/(1.*da[w & (dx>0)]) - 0.5*(disc[w & (dx>0)]**0.5)/da[w & (dx>0)]
        n[w & (dx<0)] = -0.5 - dv[w & (dx<0)]/(1.*da[w & (dx<0)]) + 0.5*(disc[w & (dx<0)]**0.5)/da[w & (dx<0)]
        n[(da != 0) & (disc < 0)] = 1000    
        n[n<0] = 1000
        dt = int(np.min(n))
        if dt == 0: dt = 1
    return x + dt*v + (dt+1)*dt*a/2, v + dt*a, t + dt

    
pat = re.compile('<x=(-*\d+), y=(-*\d+), z=(-*\d+)>')

# Answer part 1
x = np.array([map(int, pat.match(line).groups((1,2,3))) for line in open('input.txt')])
v = np.zeros(x.shape, dtype = int)
t = 0
for i in xrange(1000):
    x, v, t = step(x, v, t, dt=1)   
print sum(sum(abs(xm))*sum(abs(vm)) for (xm, vm) in zip(x,v))

# Answer part 2
x0 = np.array([map(int, pat.match(line).groups((1,2,3))) for line in open('input.txt')])
ts = []
xs = []
for k in range(3):
    x = x0[:,[k]].copy()
    v = np.zeros(x.shape, dtype = int)
    t = 0
    x, v, t = step(x, v, t)
    x1 = x.copy()
    v1 = v.copy()
    t1 = t
    while (t == t1) or not np.all((x == x1) & (v == v1)):
        last = (x.copy(), v.copy(), t)
        x, v, t = step(x, v, t)
    x, v, t = last
    while not np.all((x == x0[:,[k]]) & (v == 0)):
        x, v, t = step(x, v, t, dt=1)
    ts.append(t)
t01 = ts[0]*ts[1]/gcd(ts[0], ts[1])
t012 = t01*ts[2]/gcd(t01, ts[2])
print t012

