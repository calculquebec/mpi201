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
        A = None

    # Diffusion de la matrice A
    A = comm.bcast(A, 0)

    if rank == 0:
        B = np.random.rand(N, N)

        # Calcul des portions de la matrice B
        b_list = [
            B[
                :,
                (r * N // nranks):((r + 1) * N // nranks)  # debut:fin
            ] for r in range(nranks)
        ]

        # Voir aussi : numpy.hsplit(matrice, [séparateurs])
        # b_list = np.hsplit(B, [r * N // nranks for r in range(1, nranks)])
    else:
        b_list = None

    # Distribution des portions de la matrice B
    b = comm.scatter(b_list, 0)

    # Calcul principal
    c = A @ b

    # Regroupement des résultats partiels
    c_list = comm.gather(c, 0)

    if rank == 0:
        # Reconstruire la matrice finale C
        C = np.concatenate(c_list, axis=1)

        assert np.allclose(C, A @ B), 'Erreur de programmation'
        print('OK!')

    MPI.Finalize()


if __name__ == '__main__':
    main()
