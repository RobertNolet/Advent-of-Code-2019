#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 10:10:50 2019

@author: robertnolet
"""

from copy import copy
from itertools import permutations

# Dictionary of operations. Each entry has as key the operation number
# and as value a tuple containing the number of arguments (npar), and a function.
# The function has as input:
#     x   : a list of length npar,
#     inp : an iterator for user input.
# The function has as output a tuple of three values:
#     1st : The result of a calculation, or None
#     2nd : An output to be printed, or None
#     3rd : The next instruction pointer, or None
# Format -- opcode : (npar, lambda x, inp: (result, output, jump_ip))   
ops = {1 : (2, lambda x, inp: (x[0]+x[1], None,  None)),
       2 : (2, lambda x, inp: (x[0]*x[1], None,  None)),
       3 : (0, lambda x, inp: (inp.next(), None, None)),
       4 : (1, lambda x, inp: (None, x[0], None)),
       5 : (2, lambda x, inp: (None, None, x[1] if (x[0] != 0) else None)),
       6 : (2, lambda x, inp: (None, None, x[1] if (x[0] == 0) else None)),
       7 : (2, lambda x, inp: (int(x[0] <  x[1]), None, None)),
       8 : (2, lambda x, inp: (int(x[0] == x[1]), None, None))}
       
            
def execute(opcodes, inp = iter([1]), ip = 0, exit_on_output = False):
    """ Execute the intcode program in opcodes, with input inp and starting
    from instruction at index ip. 
    
    If exit_on_output is false (default) the
    program will run until it reaches instruction 99, and exit returning a
    tuple with the last found output, and the index of instruction 99.
    
    If exit_on_output is true, the program will run until any instruction
    generates output, and exit returning a tuple with the output and the
    index (ip) of the next instruction to be run. If the program encounters
    instruction 99 it will exit returning (None, ip)."""
    result = None
    while ((opcodes[ip]%100) != 99):
        # Read opcode
        opcode = opcodes[ip]
        (np, op) = ops[opcode%100]
        ip += 1
        # Read parameters
        pmode = [(opcode / 10**i) % 10 for i in range(2, 2+np)]
        parms = opcodes[ip:(ip+np)]
        ip += np
        # For positional parameters, read values        
        args  = [opcodes[p] if m == 0 else p for (p,m) in zip(parms, pmode)]
        # Execute op
        (res, out, new_ip) = op(args, inp)      
        if (res != None): 
            adrr = opcodes[ip]   # Read adress where to write result
            opcodes[adrr] = res  # Write result
            ip += 1
        if (out != None): 
            if exit_on_output: return (out, ip)
            result = out            
        if (new_ip != None): ip = new_ip # Jump
    return (result, ip)

def thrust(opcodes, phase):
    inp = 0
    for p in phase:
        (inp, ip) = execute(opcodes, iter([p,inp]))
    return inp

def feedback_thrust(opcodes, phase):
    amps = [copy(opcodes) for i in range(5)]
    ips = [0]*5
    inp = 0
    
    # Initialize with as input the phase, and input values.
    for i in range(5):
        (inp, ip) = execute(amps[i], iter([phase[i],inp]), ips[i], True)
        ips[i] = ip

    # Loop with new input values until the last amplifier exits (returns None)
    while (inp != None):
        last_inp = inp
        for i in range(5):
            (inp, ip) = execute(amps[i], iter([inp]), ips[i], True)
            ips[i] = ip
    return last_inp

#test1 = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
#print thrust(copy(test1), [4,3,2,1,0])
#print max((thrust(copy(test1), phase), phase) for phase in permutations([0,1,2,3,4]))

#test2 = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
#print thrust(copy(test2), [0, 1, 2, 3, 4])
#print max((thrust(copy(test2), phase), phase) for phase in permutations([0,1,2,3,4]))

#test3 = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
#print feedback_thrust(test3, [9,8,7,6,5])

opcodes = map(int, open('input.txt').readline().split(','))

# Answer part 1
print max(thrust(copy(opcodes), phase) for phase in permutations([0,1,2,3,4]))

# Answer part 2
print max(feedback_thrust(copy(opcodes), phase) for phase in permutations([5, 6, 7, 8, 9]))

