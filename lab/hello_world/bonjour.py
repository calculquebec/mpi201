#!/usr/bin/env python

from mpi4py import MPI  # MPI.Init() implicite

def main():
    """
    Programme principal
    """

    rank = MPI.COMM_WORLD.Get_rank()
    nranks = MPI.COMM_WORLD.Get_size()
    print(f'Ici le processus {rank} de {nranks}')

    MPI.Finalize()

if __name__ == '__main__':
    main()
