#!/usr/bin/env python

from mpi4py import MPI
import numpy as np

def main():
    """
    Programme principal
    """

    N = 512

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    nranks = comm.Get_size()

    if rank == 0:
        A = np.random.rand(N, N)
    else:
        A = ...

    # Diffusion de la matrice A
    A = comm.(...)

    if rank == 0:
        B = np.random.rand(N, N)

        # Calcul des portions de la matrice B
        b_list = [
            B[
                :,
                (...):(...)  # debut:fin
            ] for r in range(nranks)
        ]
    else:
        b_list = ...

    # Distribution des portions de la matrice B
    b = comm.(...)

    # Calcul principal
    c = A @ b

    # Regroupement des résultats partiels
    c_list = comm.(...)

    if rank == 0:
        # Reconstruire la matrice finale C
        C = np.concatenate(c_list, axis=1)

        assert np.allclose(C, A @ B), 'Erreur de programmation'
        print('OK!')

    MPI.Finalize()


if __name__ == '__main__':
    main()
