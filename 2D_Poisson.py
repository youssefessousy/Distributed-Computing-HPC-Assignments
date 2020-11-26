#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 14:59:24 2020

@author: kissami
"""

import numpy
from matplotlib import pyplot, cm
from numba import njit
from mpl_toolkits.mplot3d import Axes3D
import time 

@njit(fastmath=True)
def solve_2d_Poisson():
    nx = 150
    ny = 150
    nt  = 100
    xmin = 0
    xmax = 2
    ymin = 0
    ymax = 1
    
    dx = (xmax - xmin) / (nx - 1)
    dy = (ymax - ymin) / (ny - 1)
    
    # Initialization
    p  = numpy.zeros((ny, nx))
    pd = numpy.zeros((ny, nx))
    b  = numpy.zeros((ny, nx))
    x  = numpy.linspace(xmin, xmax, nx)
    y  = numpy.linspace(xmin, xmax, ny)
    row, col = p.shape
    
    # Source
    b[int(ny / 4), int(nx / 4)]  = 100
    b[int(3 * ny / 4), int(3 * nx / 4)] = -100
    
        
    return x, y, p
    
    
#compute the cpu time of the solving 2d Poisson equation
start = time.time()
start = time.time()
x, y, p = solve_2d_Poisson()
end = time.time()        
print("Execution time is : {msec} ms".format(msec=(end-start)*1000) )    

    
fig = pyplot.figure(figsize=(10, 7), dpi=100)
ax = fig.gca(projection='3d')
X, Y = numpy.meshgrid(x, y)
surf = ax.plot_surface(X, Y, p, rstride=1, cstride=1, cmap=cm.viridis,
        linewidth=0, antialiased=False)
ax.view_init(30, 225)
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
