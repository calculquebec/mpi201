#!/usr/bin/env python

from mpi4py import MPI  # MPI.Init() implicite
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

    if rank == 0:
        t1 = MPI.Wtime()

    somme = 0.0;

    borne_inf = rank * N // nranks
    borne_sup = (rank + 1) * N // nranks

    for k in range(borne_sup - 1, borne_inf - 1, -1):
        somme += (4.0 - 8.0 * (k % 2)) / (2.0 * k + 1)

    pi = comm.reduce(somme, MPI.SUM, 0)

    if rank == 0:
        t2 = MPI.Wtime()
        print(f'PI est approximativement {pi:.16f},',
              f'avec une différence de {abs(pi - math.pi):.16f}')
        print(f'Temps = {t2 - t1:.6f} sec')

    MPI.Finalize()


if __name__ == '__main__':
    main()
