Annexes
=======

`English <../en/8-appendix.html>`_

Autres communications collectives
---------------------------------

Regroupement à tous avec ``allgather``
''''''''''''''''''''''''''''''''''''''

C’est l’équivalent de ``gather`` + ``bcast``, mais en `plus efficace
<https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.allgather>`__ :

.. figure:: ../images/mpi_allgather_fr.svg

Avec ``mpi4py``, on aurait le code suivant :

.. code-block:: python

    # allgather(envoi: Any) -> list[Any]

    b = comm.allgather(a)

Transposition globale avec ``alltoall``
'''''''''''''''''''''''''''''''''''''''

C’est l’équivalent de ``scatter`` * ``gather``, mais en `plus efficace
<https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.alltoall>`__ :

.. figure:: ../images/mpi_alltoall_fr.svg

Avec ``mpi4py``, on aurait le code suivant :

.. code-block:: python

    # alltoall(envoi: Sequence[Any]) -> list[Any]

    b = comm.alltoall(a)

Mesure du temps écoulé avec ``MPI.Wtime()``
-------------------------------------------

Pour mesurer précisément le temps d’exécution d’une partie du code Python, on
peut utiliser la fonction ``MPI.Wtime()`` qui retourne une valeur de temps en
secondes en double précision. Pour calculer un temps écoulé, il suffit
d’appeler la fonction deux fois et de calculer la différence des valeurs
retournées. Typiquement, un seul processus effectue ce calcul.

.. code-block:: python

    if rank == 0:
        t1 = MPI.Wtime()

    # Calcul parallèle et communications

    if rank == 0:
        t2 = MPI.Wtime()
        print(f'Temps = {t2 - t1:.6f} sec')

Notions avancées
----------------

La bibliothèque ``mpi4py`` possède d’autres fonctionnalités intéressantes
pour optimiser les communications et pour s’ajuster aux problèmes dont les
portions de calcul sont inégales.

Communications avec des tableaux NumPy
''''''''''''''''''''''''''''''''''''''

Dans les chapitres de l’atelier, les fonctions de communication utilisées
passaient par une sérialisation et une reconstruction des objets via le
`module <https://docs.python.org/3/library/pickle.html#module-pickle>`__
``pickle`` pour transférer des données. Or, pour l’envoi de
tableaux NumPy, cette étape de sérialisation est inutilement longue, car les
données sont déjà uniformes et sans structure complexe. De plus, MPI est déjà
conçu pour transférer des tableaux de données standards (des entiers ou des
nombres à virgule flottante). Alors, comment en bénéficier?

Pour permettre des communications plus efficaces avec des tableaux NumPy, la
bibliothèque ``mpi4py`` fournit plusieurs méthodes équivalentes à celles que
nous avons vues, excepté que leur nom débute par une majuscule :

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

Voici un extrait de code adapté de l’exemple `Broadcasting a NumPy array
<https://mpi4py.readthedocs.io/en/stable/tutorial.html#collective-communication>`__ :

.. code-block:: python

    if rank == 0:
        tableau = np.arange(1000, dtype='i')
    else:
        tableau = np.empty(1000, dtype='i')

    # Le processus 0 envoie son tableau aux autres
    comm.Bcast(tableau, 0)

On remarque que le tableau à la réception doit être préalablement construit
avant d’appeler la méthode ``Bcast()``.

Pour d’autres exemples, voir le `tutoriel complet
<https://mpi4py.readthedocs.io/en/stable/tutorial.html>`__.


Communications collectives avec des portions inégales
'''''''''''''''''''''''''''''''''''''''''''''''''''''

Les fonctions de communication collective vues jusqu’ici envoyaient un même
nombre d’éléments pour chaque processus MPI. Avec ``mpi4py``, les tableaux
NumPy peuvent être divisés ou reconstruits avec un nombre différent de valeurs
pour chaque processus :

- Les deux méthodes principales sont : `MPI.Comm.Scatterv
  <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.Scatterv>`__
  et `MPI.Comm.Gatherv
  <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.Gatherv>`__.
- Ces méthodes ne tiennent pas automatiquement compte du stockage interne
  des tableaux NumPy ; elles supposent une séquence contiguë de données en
  mémoire. Il faut donc planifier le stockage interne du tableau NumPy :
  en mode *C*, les valeurs d’une matrice 2D sont stockées ligne par ligne,
  alors qu’en mode *Fortran* elles sont stockées colonne par colonne.

  - Pour plus d’information, voir les `strides
    <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.strides.html>`__
    et `le paramètre
    <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`__
    ``order``.

- Voir aussi `les exemples
  <https://github.com/calculquebec/mpi201/tree/main/lab/scatterv>`__
  dans ``~/mpi201-main/lab/scatterv``.

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
