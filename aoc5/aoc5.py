#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 08:46:12 2019

@author: robertnolet
"""

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
       
            
def execute(opcodes, inp = iter([1])):
    ip = 0
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
        if (out != None): print out # Print output
        if (new_ip != None): ip = new_ip # Jump

# Answer part 1
opcodes = map(int, open('input.txt').readline().split(','))
execute(opcodes)
        
# Answer part 2
opcodes = map(int, open('input.txt').readline().split(','))
execute(opcodes, inp = iter([5]))

