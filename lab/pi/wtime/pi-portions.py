#!/usr/bin/env python

from mpi4py import MPI
import math
import sys


def main():
    """
    Main program
    """

    N = 100000000

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    nranks = comm.Get_size()

    if rank == 0:
        t1 = MPI.Wtime()

    my_sum = 0.0;

    start = rank * N // nranks
    end = (rank + 1) * N // nranks

    for k in range(start, end):
        k = N - 1 - k  # Do N - 1 first
        my_sum += (4.0 - 8.0 * (k % 2)) / (2.0 * k + 1)

    pi = comm.reduce(my_sum, MPI.SUM, 0)

    if rank == 0:
        t2 = MPI.Wtime()
        print(f'PI is approximately {pi:.16f},',
              f'with an error of {pi - math.pi:.16f}')
        print(f'Time = {t2 - t1:.6f} sec')

    MPI.Finalize()


if __name__ == '__main__':
    main()
