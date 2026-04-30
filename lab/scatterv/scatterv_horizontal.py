#!/usr/bin/env python

from mpi4py import MPI
import numpy as np

def main():
    """
    Programme principal / Main program
    """

    N = 5

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    nranks = comm.Get_size()

    if rank == 0:
        # A matrix to be split - numbers stored by columns
        matrice = np.arange(N * N, dtype='float64').reshape(N, N, order='F')
        print(f'Matrice à diviser :\n{matrice}')

        # List of shapes (dimensions) of the uneven portions of the NxN matrix
        tailles = [p.shape for p in np.array_split(matrice, nranks, axis=1)]
        print(f'Tailles pour {nranks} processus : {tailles}')
    else:
        matrice = None
        tailles = None

    # Share all shapes with all processes
    tailles = comm.bcast(tailles)

    n_elements = [t[0] * t[1] for t in tailles]
    portion = np.zeros(tailles[rank], order='F')

    # Each process gets a portion of a given shape
    comm.Scatterv([matrice, n_elements], portion)

    print(f'Portion du rank {rank} :\n{portion}')

    # Gather the scaled values by N in process 0
    comm.Gatherv(portion * N, [matrice, n_elements])

    if rank == 0:
        print(f'Matrice finale :\n{matrice}')

    MPI.Finalize()


if __name__ == '__main__':
    main()
