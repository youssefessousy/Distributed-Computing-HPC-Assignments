# -*- coding: utf-8 -*-

"""
Created on Tue Dec 15 19:51:42 2020

@author: ESSOUSY Youssef
"""
"""
   In this file, we generate a parallel code that computes the integral
   of a function using the Trapeze method. Since my computer has four
   processors, we will parallelize using less than four processors.
"""

############## Libraries Importation ##################

import numpy as np
import matplotlib.pyplot as plt
from mpi4py import MPI
import time

########### Communicator, Rank and Size

COMM = MPI.COMM_WORLD
RANK = COMM.Get_rank()
SIZE = COMM.Get_size()

# Defining the function that calculate the integral using Trapeze method

def compute_integrale_rectangle(x, y, nbi):
    integrale = 0.
    for i in range(nbi):
        integrale = integrale + y[i]*(x[i+1]-x[i])
    return integrale

t    = time.time()
xmin = 0
xmax = 3*np.pi/2
nbx  = 80           # Points number
xint = 3*np.pi/4    # The middle point
nbi  = nbx - 1      # Intervals number

x = np.linspace(xmin, xmax, nbx)    # The vector points
y = np.cos(x)                       # The vector image of points

# Computing the integral without parallelization using the function defined

integrale = compute_integrale_rectangle(x, y, nbi)
t1  = time.time() - t
print("The integral without parallelization : integrale =", integrale," run in ",t1,"s")

# Computing the integral using Parallelization
t    = time.time()   # Start timing for the parallelized computing
tag  = 1
if RANK == 1:
    nbx = int(nbx/2)
    nbi = nbx - 1       # Intervals number
    x   = np.linspace(xmin, xint, nbx)
    y   = np.cos(x)
    integrale1 = compute_integrale_rectangle(x, y, nbi)
    COMM.send(integrale1, dest=0, tag=tag)  # Sending the computed value to proc of rank 0

if RANK==2:
    nbx = int(nbx/2)
    nbi = nbx - 1       # Intervals number
    x   = np.linspace(xint, xmax, nbx)
    y   = np.cos(x)
    integrale2 = compute_integrale_rectangle(x, y, nbi)
    COMM.send(integrale2, dest=0, tag=tag)  # Sending the computed value to proc of rank 0

if RANK==0 :
    recvbuf1 = COMM.recv(source=1,tag=tag) # Recieving the value computedfrom proc of rank 1
    recvbuf2 = COMM.recv(source=2,tag=tag) # Recieving the value computedfrom proc of rank 1
    t2  = time.time() - t
    print("The integral with parallelization : integrale=", recvbuf1+ recvbuf2," run in ",t2,"s") # The sum of the two values gives the integral value

