#!/usr/bin/env python

from mpi4py import MPI
import sys


def main():
    """
    Programme principal / Main program
    """

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if size < 2:
        sys.exit(None)

    if rank == 0:
        A = [1.0, 2.0]

        # Send & Receive
        comm.( ... )
        comm.( ... )
        print(f'Process {rank} sent     A=[{A[0]}, {A[1]}]')
        print(f'Process {rank} received B=[{B[0]}, {B[1]}]')

    if rank == 1:
        B = [3.0, 4.0]

        # Send & Receive
        comm.( ... )
        comm.( ... )
        print(f'Process {rank} sent     B=[{B[0]}, {B[1]}]')
        print(f'Process {rank} received A=[{A[0]}, {A[1]}]')

    MPI.Finalize()


if __name__ == '__main__':
    main()
