#!/usr/bin/env python

from mpi4py import MPI  # MPI.Init() is called implicitly

def main():
    """
    Main program
    """

    rank = MPI.COMM_WORLD.Get_rank()
    nranks = MPI.COMM_WORLD.Get_size()
    print(f"Hello, I'm process {rank} of {nranks}")

    MPI.Finalize()

if __name__ == '__main__':
    main()
