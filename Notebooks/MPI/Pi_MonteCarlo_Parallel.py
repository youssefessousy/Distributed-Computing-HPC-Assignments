"""
Created on Thu Dec 17 19:39:54 2020

@author: ESSOUSY Youssef
"""

####################################################

import random
from mpi4py import MPI
import time

####################################################

COMM = MPI.COMM_WORLD
rank = COMM.Get_rank()
size = COMM.Get_size()

def compute_pi(N):
    count = 0
    for i in range(N) :
        x = random.uniform(-1, 1) 
        y = random.uniform(-1, 1) 
        if x**2 + y**2 <= 1:
            count += 1
    pi = 4*count/N
    return pi

t   = time.time()
N   = 1000000
nbc = int(N/size) + (size == (rank + 1))*(N%size)

pi_ = compute_pi(nbc)/size
pi  = COMM.reduce(pi_, op=MPI.SUM, root=0)
if rank == 0 :
    time = time.time()-t
    print("pi = ", pi, " and CPU time = ", time, "s")

