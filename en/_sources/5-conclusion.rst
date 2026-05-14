Conclusion
==========

`Français <../fr/5-conclusion.html>`_

A reminder of some concepts of parallelism:

- Communications and synchronizations

  - Dependencies between processes

- `Scalability <https://docs.alliancecan.ca/wiki/Scalability>`__ and
  `Amdahl's law <https://en.wikipedia.org/wiki/Amdahl%27s_law>`__

  - Granularity - minimum amount of work to be done independently
  - Load distribution

An MPI library like ``mpi4py`` facilitates:

- communications via a communication environment

  - ``from mpi4py import MPI  # MPI.Init() is called implicitly``
  - ``comm = MPI.COMM_WORLD``
  - ``rank = comm.Get_rank()``, ``nranks = comm.Get_size()``
  - ``MPI.Finalize()``

- point-to-point communications

  - ``comm.send(obj, dest, tag=tag)``
  - ``data = comm.recv(source=source, tag=tag, status=status)``

- non-blocking communications

  - ``request = comm.isend(obj, dest, tag=tag)``
  - ``request = comm.irecv(source=ANY_SOURCE, tag=ANY_TAG)``

- collective communications

  - ``comm.bcast()``, ``comm.scatter()``, ``comm.gather()``,
    ``comm.allgather()``, ``comm.alltoall()``
  - ``comm.reduce()``, ``comm.allreduce()``
