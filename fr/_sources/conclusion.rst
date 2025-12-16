Conclusion
==========

`English <../en/conclusion.html>`_

Rappel de quelques concepts du parallélisme :

- Communications et synchronisations

  - Dépendances entre processeurs

- `Scalabilité <https://docs.alliancecan.ca/wiki/Scalability/fr>`__ et
  `loi d’Amdahl <https://fr.wikipedia.org/wiki/Loi_d%27Amdahl>`__

  - Granularité - quantité minimale de travail à faire de manière autonome
  - Répartition de la charge

MPI dans les autres langages
----------------------------

- C et Fortran : le standard MPI est déjà défini dans ces langages.
- C++ :

  - MPI 3.0 a éliminé les interfaces C++.
  - `Boost MPI <https://www.boost.org/doc/libs/release/libs/mpi/>`__ :
    bibliothèque pratique et très puissante pour les développeurs en C++.
  - `Midi-conférence Boost-MPI
    <https://www.youtube.com/watch?v=U0axIKTO3wM>`__.

  .. code-block:: c++

      boost::mpi::environment env(argc, argv);
      boost::mpi::communicator world;
      std::string s;

      if (world.rank() == 0)
          world.recv(boost::mpi::any_source, 746, s);

Défis de parallélisation supplémentaires
----------------------------------------

Les codes suivants fonctionnent déjà en mode séquentiel.
C’est maintenant à vous de les paralléliser avec MPI :

- `Convolution sur une image
  <https://github.com/calculquebec/cq-formation-convolution/tree/main/defi-mpi>`__
- `Écoulement de chaleur
  <https://github.com/calculquebec/cq-formation-ecoulement-chaleur>`__
- `Problème à N corps
  <https://github.com/calculquebec/cq-formation-nbody>`__

Pour mesurer le temps d’exécution d’un programme, la commande ``time srun``
doit être dans un `script de tâche
<https://docs.alliancecan.ca/wiki/Running_jobs/fr#T.C3.A2che_MPI>`__
soumis avec la commande ``sbatch`` :

.. code-block:: bash

    #!/bin/bash
    #SBATCH --ntasks=4
    #SBATCH … # temps, mémoire, etc.

    time srun ./programme

Bonus - Notions avancées
------------------------

La bibliothèque ``mpi4py`` possède d’autres fonctionnalités :

- Communications avec des tableaux NumPy.

  - Ce sont les méthodes débutant par une majuscule (`voir le tutoriel
    <https://mpi4py.readthedocs.io/en/stable/tutorial.html>`__).
  - `MPI.Comm.Send
    <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.Send>`__,
    `MPI.Comm.Recv
    <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.Recv>`__
  - `MPI.Comm.Isend
    <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.Isend>`__,
    `MPI.Comm.Irecv
    <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.Irecv>`__
  - `MPI.Comm.Bcast
    <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.Bcast>`__,
    `MPI.Comm.Scatter
    <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.Scatter>`__,
    `MPI.Comm.Gather
    <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.Gather>`__

- Communications collectives avec des portions inégales.

  - Les fonctions de communication collective vues jusqu’ici envoyaient un même
    nombre d’éléments pour chaque processus MPI.
  - Avec ``mpi4py``, les tableaux NumPy peuvent être divisés ou reconstruits
    avec un nombre différent de valeurs pour chaque processus :

    - Avec `MPI.Comm.Scatterv
      <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.Scatterv>`__
      et `MPI.Comm.Gatherv
      <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.Gatherv>`__.
    - Ces méthodes ne tiennent pas automatiquement compte du stockage interne
      des tableaux NumPy, mais seulement de la séquence contiguë de données en
      mémoire. Il faut donc planifier le stockage interne du tableau NumPy :
      en mode *C*, les valeurs d’une matrice 2D sont stockées ligne par ligne,
      alors qu’en mode *Fortran* elles sont stockées colonne par colonne.

      - Pour plus d’information, voir les `strides
        <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.strides.html>`__.

    - Voir `les exemples
      <https://github.com/calculquebec/mpi201/tree/main/lab/scatterv>`__
      dans ``~/mpi201-main/lab/scatterv``.
