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

    my_sum = 0.0;

    for k in range(0, N):
        k = N - 1 - k  # Do N - 1 first
        my_sum += (4.0 - 8.0 * (k % 2)) / (2.0 * k + 1)

    pi = my_sum

    if rank == 0:
        print(f'PI is approximately {pi:.16f},',
              f'with an error of {pi - math.pi:.16f}')

    MPI.Finalize()


if __name__ == '__main__':
    main()
