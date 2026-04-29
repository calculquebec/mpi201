#!/usr/bin/env python

from mpi4py import MPI
import numpy as np

def main():
    """
    Main program
    """

    N = 512

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    nranks = comm.Get_size()

    if rank == 0:
        A = np.random.rand(N, N)
    else:
        A = None

    # Diffusion of matrix A
    A = comm.bcast(A, 0)

    if rank == 0:
        B = np.random.rand(N, N)

        # Calculate the portions of matrix B
        b_list = [
            B[
                :,
                (r * N // nranks):((r + 1) * N // nranks)  # start:end
            ] for r in range(nranks)
        ]

        # See also: numpy.hsplit(matrix, [separators])
        # b_list = np.hsplit(B, [r * N // nranks for r in range(1, nranks)])
    else:
        b_list = None

    # Distribution of portions of matrix B
    b = comm.scatter(b_list, 0)

    # Main calculation
    c = A @ b

    # Group the partial results
    c_list = comm.gather(c, 0)

    if rank == 0:
        # Reconstruct the final matrix C
        C = np.concatenate(c_list, axis=1)

        assert np.allclose(C, A @ B), 'Programming error'
        print('OK!')

    MPI.Finalize()


if __name__ == '__main__':
    main()
