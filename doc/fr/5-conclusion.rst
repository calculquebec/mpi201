Conclusion
==========

`English <../en/5-conclusion.html>`_

Rappel de quelques concepts du parallélisme :

- Communications et synchronisations

  - Dépendances entre processeurs

- `Scalabilité <https://docs.alliancecan.ca/wiki/Scalability/fr>`__ et
  `loi d’Amdahl <https://fr.wikipedia.org/wiki/Loi_d%27Amdahl>`__

  - Granularité - quantité minimale de travail à faire de manière autonome
  - Répartition de la charge

Une bibliothèque MPI comme ``mpi4py`` facilite les communications :

- via un environnement de communication

  - ``from mpi4py import MPI  # MPI.Init() implicite``
  - ``comm = MPI.COMM_WORLD``
  - ``rank = comm.Get_rank()``, ``nranks = comm.Get_size()``
  - ``MPI.Finalize()``

- point-à-point

  - ``comm.send(envoi, dest=dest, tag=etiquette)``
  - ``recept = comm.recv(source=source, tag=etiquette, status=etat)``

- non-bloquantes

  - ``requete = comm.isend(envoi, dest, tag=etiquette)``
  - ``requete = comm.irecv(source=ANY_SOURCE, tag=ANY_TAG)``

- collectives

  - ``comm.bcast()``, ``comm.scatter()``, ``comm.gather()``,
    ``comm.allgather()``, ``comm.alltoall()``
  - ``comm.reduce()``, ``comm.allreduce()``
