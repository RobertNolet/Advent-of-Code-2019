#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 09:40:09 2019

@author: robertnolet
"""

import numpy as np
import matplotlib.pyplot as plt

w = 25
h = 6

data = np.reshape(map(int, open('input.txt').readline()), (-1, h, w))

# Answer part 1
(s, l) = min((s,l) for (l,s) in enumerate(np.sum(data == 0, axis=(1,2))))
print np.sum(data[l,:,:] == 1) * np.sum(data[l,:,:] == 2)

# Answer part 2
result = np.zeros((h, w))
for layer in reversed(data):
    result[layer != 2] = layer[layer != 2]
plt.imshow(result)
