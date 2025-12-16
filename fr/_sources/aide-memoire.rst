Aide-mémoire
============

`English <../en/cheatsheet.html>`_

.. list-table:: Gestion des processus MPI
    :header-rows: 1

    * - Concept
      - `Python <https://mpi4py.readthedocs.io/en/stable/>`__ (``mpi4py``)
      - `C/Fortran <https://www.mpi-forum.org/docs/>`__ (standard)
    * - Initialisation
      - `MPI.Init()
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Init.html>`__
      - `MPI_Init()
        <https://www.mpi-forum.org/docs/mpi-4.1/mpi41-report.pdf#subsection.11.2.1>`__
    * - Finalisation
      - `MPI.Finalize()
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Finalize.html>`__
      - `MPI_Finalize()
        <https://www.mpi-forum.org/docs/mpi-4.1/mpi41-report.pdf#subsection.11.2.2>`__
    * - Avortement
      - ``sys.exit(None)``
      - `MPI_Abort()
        <https://www.mpi-forum.org/docs/mpi-4.1/mpi41-report.pdf#subsection.11.4.2>`__
    * -
      -
      -
    * - Communicateur
      - `MPI.COMM_WORLD
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.COMM_WORLD.html>`__
      - `MPI_COMM_WORLD
        <https://www.mpi-forum.org/docs/mpi-4.1/mpi41-report.pdf#section.11.2>`__
    * - Rang
      - `MPI.Comm.Get_rank()
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.Get_rank>`__
      - `MPI_Comm_rank()
        <https://www.mpi-forum.org/docs/mpi-4.1/mpi41-report.pdf#page=362>`__
    * - Nombre de processus
      - `MPI.Comm.Get_size()
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.Get_size>`__
      - `MPI_Comm_size()
        <https://www.mpi-forum.org/docs/mpi-4.1/mpi41-report.pdf#subsection.7.4.1>`__

.. list-table:: Communications point-à-point
    :header-rows: 1

    * - Concept
      - `Python <https://mpi4py.readthedocs.io/en/stable/>`__ (objets)
      - `Python <https://mpi4py.readthedocs.io/en/stable/>`__ (tableaux Numpy)
      - `C/Fortran <https://www.mpi-forum.org/docs/>`__ (standard)
    * - Types de données
      - `Sérialisation <https://fr.wikipedia.org/wiki/S%C3%A9rialisation>`__
        automatique
      - ``MPI.CHAR`` `et autres
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.html>`__
      - ``MPI_CHAR`` `et autres
        <https://www.mpi-forum.org/docs/mpi-4.1/mpi41-report.pdf#page=76>`__
    * -
      -
      -
      -
    * - Envoi standard
      - `MPI.Comm.send()
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.send>`__
      - `MPI.Comm.Send()
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.Send>`__
      - `MPI_Send()
        <https://www.mpi-forum.org/docs/mpi-4.1/mpi41-report.pdf#section.3.2>`__
    * - Réception (bloquante)
      - `MPI.Comm.recv()
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.recv>`__
      - `MPI.Comm.Recv()
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.Recv>`__
      - `MPI_Recv() <https://www.mpi-forum.org/docs/mpi-4.1/mpi41-report.pdf#subsection.3.2.4>`__
    * -
      -
      -
      -
    * - Envoi non-bloquant
      - `MPI.Comm.isend()
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.isend>`__
      - `MPI.Comm.Isend()
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.Isend>`__
      - `MPI_Isend()
        <https://www.mpi-forum.org/docs/mpi-4.1/mpi41-report.pdf#subsection.3.7.2>`__
    * - Réception non-bloquante
      - `MPI.Comm.irecv()
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.irecv>`__
      - `MPI.Comm.Irecv()
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.Irecv>`__
      - `MPI_Irecv()
        <https://www.mpi-forum.org/docs/mpi-4.1/mpi41-report.pdf#page=117>`__
    * - Attente (bloquante)
      - `MPI.Request.wait()
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Request.html#mpi4py.MPI.Request.wait>`__
      - `MPI.Request.wait()
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Request.html#mpi4py.MPI.Request.wait>`__
      - `MPI_Wait()
        <https://www.mpi-forum.org/docs/mpi-4.1/mpi41-report.pdf#subsection.3.7.3>`__

.. list-table:: Communications collectives
    :header-rows: 1

    * - Concept
      - `Python <https://mpi4py.readthedocs.io/en/stable/>`__ (objets)
      - `Python <https://mpi4py.readthedocs.io/en/stable/>`__ (tableaux Numpy)
      - `C/Fortran <https://www.mpi-forum.org/docs/>`__ (standard)
    * - Diffusion
      - `MPI.Comm.bcast()
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.bcast>`__
      - `MPI.Comm.Bcast()
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.Bcast>`__
      - `MPI_Bcast()
        <https://www.mpi-forum.org/docs/mpi-4.1/mpi41-report.pdf#section.6.4>`__
    * - Distribution
      - `MPI.Comm.scatter()
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.scatter>`__
      - `MPI.Comm.Scatter()
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.Scatter>`__
      - `MPI_Scatter()
        <https://www.mpi-forum.org/docs/mpi-4.1/mpi41-report.pdf#section.6.6>`__
    * - Regroupement
      - `MPI.Comm.gather()
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.gather>`__
      - `MPI.Comm.Gather()
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.Gather>`__
      - `MPI_Gather()
        <https://www.mpi-forum.org/docs/mpi-4.1/mpi41-report.pdf#section.6.5>`__
    * - Regroupement à tous
      - `MPI.Comm.allgather()
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.allgather>`__
      - `MPI.Comm.Allgather()
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.Allgather>`__
      - `MPI_Allgather()
        <https://www.mpi-forum.org/docs/mpi-4.1/mpi41-report.pdf#section.6.7>`__
    * - Transposition globale
      - `MPI.Comm.alltoall()
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.alltoall>`__
      - `MPI.Comm.Alltoall()
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.Alltoall>`__
      - `MPI_Alltoall()
        <https://www.mpi-forum.org/docs/mpi-4.1/mpi41-report.pdf#section.6.8>`__
    * -
      -
      -
      -
    * - Réduction
      - `MPI.Comm.reduce()
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.reduce>`__
      - `MPI.Comm.Reduce()
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.Reduce>`__
      - `MPI_Reduce()
        <https://www.mpi-forum.org/docs/mpi-4.1/mpi41-report.pdf#subsection.6.9.1>`__
    * - Réduction et diffusion
      - `MPI.Comm.allreduce()
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.allreduce>`__
      - `MPI.Comm.Allreduce()
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.Allreduce>`__
      - `MPI_Allreduce()
        <https://www.mpi-forum.org/docs/mpi-4.1/mpi41-report.pdf#subsection.6.9.6>`__
