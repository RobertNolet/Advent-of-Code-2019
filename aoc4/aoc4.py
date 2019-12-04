#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 10:16:20 2019

@author: robertnolet
"""

from itertools import combinations_with_replacement as combr

# Input
inp = "138241-674034"
# Number of digits
n = 6

# Parse input
[s,e] = [tuple(map(int, st)) for st in inp.split('-')]

# Answer part 1
pwds = filter(lambda x: (s <= x <= e) and (len(set(x)) < n), combr(range(10), n)) 
print len(pwds)
    
# Answer part 2
print sum(2 in map(x.count,x) for x in pwds) 
