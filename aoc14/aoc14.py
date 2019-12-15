#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 11:44:23 2019

@author: robertnolet
"""

import re
import numpy as np

pat = re.compile('(\d+) (\S+)')
def parse(s):
    m = pat.match(s)
    return (int(m.group(1)), m.group(2))

def sparse_to_dense(l, rows, cols):
    result = np.zeros((rows, cols))
    for (r, m, n) in l: result[r,m] = n
    return result

def idiv_up(a, b):
    result = a/b
    result[a%b > 0] += 1
    return result
    
xlist = []
ylist = []
mats = ['ORE']
for r, line in enumerate(open('input.txt')):
    [s_in, s_out] = line.split(' => ')
    (n, mat_out) = parse(s_out)
    if mat_out in mats:
        m_out = mats.index(mat_out)
    else:
        m_out = len(mats)
        mats.append(mat_out)
    ylist.append((m_out, n))
    for s in s_in.split(', '):
        n, mat = parse(s)
        if mat in mats:
            m = mats.index(mat)
        else:
            m = len(mats)
            mats.append(mat)
        xlist.append((m,m_out,n))
x = np.zeros((len(mats), len(mats)), dtype=int)
for (m, r, n) in xlist: x[m,r] = n
x[0,0] = 1
y = np.zeros((len(mats)), dtype=int)
for (m,n) in ylist: y[m] = n
y[0] = 1
    

depth = -np.ones(y.shape, dtype=int)
depth[0] = 1
d = 2
while np.any(depth < 0):
    depth[[(depth[r] == -1) and not np.any(x[:,r]*depth < 0) for r in range(len(y))]] = d
    d += 1
    
req = np.zeros(y.shape, dtype=int)
req[mats.index('FUEL')] = 1
for d in reversed(range(1,max(depth)+1)):
    nruns = np.zeros(y.shape, dtype=int)
    nruns[depth == d] = idiv_up(req[depth == d],y[depth == d])
    req = req - y*nruns + x.dot(nruns)
ore_to_fuel = req[0]
print ore_to_fuel

ore = 1000000000000
while req[0] < ore:
    fuel = ore/ore_to_fuel
    req = np.zeros(y.shape, dtype=int)
    req[mats.index('FUEL')] = fuel
    for d in reversed(range(1,max(depth)+1)):
        nruns = np.zeros(y.shape, dtype=int)
        nruns[depth == d] = idiv_up(req[depth == d],y[depth == d])
        req = req - y*nruns + x.dot(nruns)
    ore_to_fuel = req[0]/fuel
print fuel-2



        

    
