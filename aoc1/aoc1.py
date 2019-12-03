#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 10:03:37 2019

@author: robertnolet
"""

def fuel_cost(mass):
    return (mass / 3) - 2

def full_fuel_cost(mass):
    x = fuel_cost(mass)
    return 0 if (x <= 0) else x + full_fuel_cost(x)

# test
# print full_fuel_cost(100756)

#Answer part 1
print sum(fuel_cost(int(line)) for line in open("input.txt"))

#Answer part 2
print sum(full_fuel_cost(int(line)) for line in open("input.txt"))