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
pwds = [x for x in combr(range(10), n)   # Loop over non-decreasing seq.
          if (s <= x <= e)               # Check range
          and (len(set(x)) < n)]         # Check if any digit is repeated
print len(pwds)
    
# Answer part 2
print len([x for x in pwds if any(x.count(d) == 2 for d in x)]) 
