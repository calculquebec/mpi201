#!/usr/bin/env python

from mpi4py import MPI
import math
import sys


def main():
    """
    Programme principal
    """

    N = 100000000

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    nranks = comm.Get_size()

    somme = 0.0;

    borne_inf = rank * N // nranks
    borne_sup = (rank + 1) * N // nranks

    for k in range(borne_inf, borne_sup):
        k = N - 1 - k  # N - 1 en premier
        somme += (4.0 - 8.0 * (k % 2)) / (2.0 * k + 1)

    pi = comm.reduce(somme, MPI.SUM, 0)

    if rank == 0:
        print(f'PI est approximativement {pi:.16f},',
              f'avec une erreur de {pi - math.pi:.16f}')

    MPI.Finalize()


if __name__ == '__main__':
    main()
