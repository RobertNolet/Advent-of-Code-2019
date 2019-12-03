#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 09:16:59 2019

@author: robertnolet
"""

from copy import copy
from itertools import count

ops = {1 : lambda x,y: x+y,
       2 : lambda x,y: x*y}
            
def execute(opcodes, result_pos = 0):
    for ip in count(0,4):
        if opcodes[ip] == 99: break
        [inst, adrx, adry, adrr] = opcodes[ip:(ip+4)]
        opcodes[adrr] = ops[inst](opcodes[adrx],opcodes[adry])
    return opcodes[result_pos]

def tri_iter():
    """ Iterate over pairs (a,b) with a,b ≥ 0, in a 'triangular' order."""
    return ((j,i-j) for i in count() for j in xrange(i))

def find_output(opcodes, output):
    for (noun, verb) in tri_iter():
        inp = copy(opcodes)
        inp[1:3] = [noun, verb]
        if (execute(inp) == output): break
    return (noun,verb)

#test1 = [1,9,10,3,2,3,11,0,99,30,40,50]
#print execute(test1)

output = 19690720   # Date of Apollo 11 moon landing?
opcodes = map(int, open('input.txt').readline().split(','))

# Answer part 1
inp = copy(opcodes)
inp[1:3] = [12,2]
print execute(inp)

# Answer part 2
(noun, verb) = find_output(opcodes, output)    
print 100*noun + verb
    

