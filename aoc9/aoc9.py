#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 08:20:04 2019

@author: robertnolet
"""


# Dictionary of operations. Each entry has as key the operation number
# and as value a tuple containing the number of arguments (npar), and a function.
# The function has as input:
#     x   : a list of length npar,
#     inp : an iterator for user input,
#     ip  : the current instruction pointer
# The function has as output a tuple of three values:
#     1st : The result of a calculation, or None
#     2nd : An output to be printed, or None
#     3rd : The next instruction pointer
# Format -- opcode : (npar, lambda x, inp: (result, output, jump_ip))   
ops = {1 : (2, lambda x, inp, ip: (x[0]+x[1], None,  ip+4)),
       2 : (2, lambda x, inp, ip: (x[0]*x[1], None,  ip+4)),
       3 : (0, lambda x, inp, ip: (inp.next(), None, ip+2)),
       4 : (1, lambda x, inp, ip: (None, x[0], ip+2)),
       5 : (2, lambda x, inp, ip: (None, None, x[1] if (x[0] != 0) else ip+3)),
       6 : (2, lambda x, inp, ip: (None, None, x[1] if (x[0] == 0) else ip+3)),
       7 : (2, lambda x, inp, ip: (int(x[0] <  x[1]), None, ip+4)),
       8 : (2, lambda x, inp, ip: (int(x[0] == x[1]), None, ip+4)),
       9 : (1, lambda x, inp, ip: (x[0], None, ip+2))}

class IntCode:
    def __init__(self, program, inp = [], ip=0):
        self.mem = program
        self.ip = ip
        self.inp = iter(inp)
        self.rel = 0
        self.active = True
    
    def __iter__(self):
        return self
    
    def next(self):
        out = None
        while (out == None):
            if not self.active: raise StopIteration
            out = self.step()
        return out
    
    def readvalue(self, val, mode):
        if   mode == 0: return self.mem[val] if val < len(self.mem) else 0
        elif mode == 1: return val
        elif mode == 2: return self.mem[self.rel+val] if self.rel+val < len(self.mem) else 0
        else:
            print "Unknown read mode! {}"%mode
            exit()
            
    def writevalue(self, res, addr, mode):
        if mode == 2:
            addr += self.rel
        elif mode != 0:
            print 'Unknown write mode!'
            exit()            
        if len(self.mem) <= addr: 
            self.mem.extend([0]*(addr - len(self.mem) + 1))
        self.mem[addr] = res
            
    def step(self):
        opcode = self.mem[self.ip]
        if opcode == 99:
            self.active = False
            return None
        (npar, op) = ops[opcode%100]
        modes = [(opcode / 10**i) % 10 for i in range(2, 2+npar)]
        parms = self.mem[(self.ip+1):(self.ip+1+npar)]
        args  = [self.readvalue(p,m) for (p,m) in zip(parms, modes)]
        (res, out, new_ip) = op(args, self.inp, self.ip)
        if (opcode%100 == 9): self.rel += res
        elif (res != None): self.writevalue(res, self.mem[self.ip+npar+1], (opcode/10**(npar+2))%10)
        self.ip = new_ip
        return out
    
    def execute(self):
        return list(self)
        
            
#test1 = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
#print IntCode(test1).execute()
        
#test2 = [1102,34915192,34915192,7,4,7,99,0]
#print IntCode(test2).execute()

#test3 = [104,1125899906842624,99]
#print IntCode(test3).execute()

# Answer part 1
print IntCode(map(int, open('input.txt').readline().split(',')), iter([1])).execute()

# Answer part 2
print IntCode(map(int, open('input.txt').readline().split(',')), iter([2])).execute()
