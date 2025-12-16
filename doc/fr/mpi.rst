Premiers pas avec MPI
=====================

`English <../en/mpi.html>`_

Qu’est-ce que MPI?
------------------

MPI, pour **Message Passing Interface**, est une interface de transmission de
messages.

- Ce n’est **pas** un langage de programmation.
- C’est à l’origine une **bibliothèque de fonctions** que l’on peut appeler à
  partir du Fortran, du C ou encore du C++.
- C’est une `norme officielle <https://www.mpi-forum.org/docs/>`__
  (de MPI 1.0 en 1994 à `MPI 4.1
  <https://www.mpi-forum.org/docs/mpi-4.1/mpi41-report.pdf>`__
  depuis novembre 2023).
- Hors norme, il existe des interfaces en d’autres langages :
  **Python**, R, Perl et Java.

  - Par exemple, `mpi4py
    <https://mpi4py.readthedocs.io/en/stable/overview.html>`__.

Structure d’un code MPI
-----------------------

Dans un programme MPI, que ce soit en C, en Fortran ou en Python :

- On doit d’abord `initialiser l’environnement d’exécution
  <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Init.html>`__.
  Avec la bibliothèque ``mpi4py``, il suffit d’importer le module ``MPI``.
- Avant la fin du programme, on doit `terminer l’environnement d’exécution
  <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Finalize.html>`__
  en appelant la fonction ``MPI.Finalize()``.
- Tous les autres appels à MPI doivent se faire entre les opérations ci-dessus.

.. code-block:: python

    #!/usr/bin/env python

    from mpi4py import MPI  # MPI.Init() implicite

    def main():
        """
        Programme principal
        """

        # Code parallèle

        MPI.Finalize()

    if __name__ == '__main__':
        main()

Parallélisation explicite
-------------------------

- C’est la responsabilité de la programmeuse ou du programmeur de dire à chaque
  processus ce qu’il doit faire selon son *rang* dans la liste des processus.
- Chaque processus échange avec les autres les données dont ils ont besoin pour
  résoudre un problème.
- Un code source appelant la bibliothèque MPI utilise donc (en général) le
  concept de programme unique travaillant sur des données multiples (*Single
  Program, Multiple Data* ou SPMD).

Communicateurs
''''''''''''''

Un communicateur désigne un **groupe de processus** pouvant communiquer
ensemble.

- La majorité des fonctions MPI sont appelées avec un communicateur pour savoir
  sur quel groupe de processus agir.
- Avec ``mpi4py``, le `communicateur par défaut
  <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.COMM_WORLD.html>`__
  ``MPI.COMM_WORLD`` englobe tous les processus.
- Dans une utilisation plus avancée, on peut créer d’autres communicateurs.

  .. figure:: ../images/communicators.svg
      :height: 360 px
      :class: no-scaled-link

Nombre de processus et un rang unique
'''''''''''''''''''''''''''''''''''''

Pour s’orienter dans un programme parallèle donné, chaque processus dans un
communicateur doit savoir le `nombre de processus impliqués
<https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.Get_size>`__
et son `rang
<https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.Get_rank>`__
parmi eux.

- Ces valeurs sont communément appelées ``size``, soit la taille du
  communicateur, et ``rank``, respectivement.
- Le rang est un identifiant entier unique dont la valeur est de ``0`` à
  ``size-1`` inclusivement.
- Avec ``mpi4py`` et le communicateur par défaut, voici comment obtenir les
  valeurs de ``rank`` et ``size`` :

  .. code-block:: python

      comm = MPI.COMM_WORLD
      rank = comm.Get_rank()
      size = comm.Get_size()

.. note::

    En cas de conflit de nom avec une autre variable ``size`` dans votre code,
    vous pouvez utiliser ``nranks`` à la place.

Dans le fichier ``~/mpi201-main/lab/bonjour/bonjour.py``,
on a l’exemple suivant :

.. code-block:: python

    #!/usr/bin/env python

    from mpi4py import MPI  # MPI.Init() implicite

    def main():
        """
        Programme principal
        """

        rank = MPI.COMM_WORLD.Get_rank()
        nranks = MPI.COMM_WORLD.Get_size()
        print(f'Ici le processus {rank} de {nranks}')

        MPI.Finalize()

    if __name__ == '__main__':
        main()

Environnement requis pour utiliser MPI
--------------------------------------

Pour utiliser MPI en Python, il faut deux modules :

- Un module permettant de compiler et d’exécuter un programme MPI est chargé
  par défaut (``openmpi``). Pour voir tous les modules chargés :

  .. code-block:: console
      :emphasize-lines: 8

      [alice@narval1 ~]$ module list

      Currently Loaded Modules:
        1) CCconfig            6) ucx/1.14.1            11) flexiblas/3.3.1
        2) gentoo/2023   (S)   7) libfabric/1.18.0      12) blis/0.9.0
        3) gcccore/.12.3 (H)   8) pmix/4.2.4            13) StdEnv/2023     (S)
        4) gcc/12.3      (t)   9) ucc/1.2.0
        5) hwloc/2.9.1        10) openmpi/4.1.5    (m)

- Un module ``mpi4py`` est aussi requis, mais il n’est pas chargé par défaut.
  On peut chercher une version adéquate avec la commande ``module spider`` :

  .. code-block:: console
      :emphasize-lines: 14

      [alice@narval1 ~]$ module spider mpi4py

      -------------------------------------------------------------------------
        mpi4py:
      -------------------------------------------------------------------------
          Versions:
              mpi4py/3.0.3
              mpi4py/3.1.2
              mpi4py/3.1.3
              mpi4py/3.1.4
              mpi4py/3.1.4 (E)
              mpi4py/3.1.6
              mpi4py/4.0.0
              mpi4py/4.0.3

  .. code-block:: console
      :emphasize-lines: 17

      [alice@narval1 ~]$ module spider mpi4py/4.0.3

      -------------------------------------------------------------------------
        mpi4py: mpi4py/4.0.3
      -------------------------------------------------------------------------
          Description:
            MPI for Python (mpi4py) provides bindings of the Message Passing
            Interface (MPI) standard for the Python programming language,
            allowing any Python program to exploit multiple processors.

          Properties:
            Tools for development / Outils de développement

          You will need to load all module(s) on any one of the lines below
          before the "mpi4py/4.0.3" module is available to load.

            StdEnv/2023  gcc/12.3  openmpi/4.1.5

- Puisque nous avons déjà toutes les dépendances requises, nous pouvons ensuite
  charger ``mpi4py`` dans l’environnement. Note : un module Python sera chargé
  automatiquement.

  .. code-block:: console
      :emphasize-lines: 8-9

      [alice@narval1 ~]$ module load mpi4py/4.0.3
      [alice@narval1 ~]$ module list

      Currently Loaded Modules:
        1) CCconfig            6) ucx/1.14.1            11) flexiblas/3.3.1
        2) gentoo/2023   (S)   7) libfabric/1.18.0      12) blis/0.9.0
        3) gcccore/.12.3 (H)   8) pmix/4.2.4            13) StdEnv/2023     (S)
        4) gcc/12.3      (t)   9) ucc/1.2.0             14) python/3.11.5   (t)
        5) hwloc/2.9.1        10) openmpi/4.1.5    (m)  15) mpi4py/4.0.3    (t)

Compilation d’un programme MPI
''''''''''''''''''''''''''''''

Alors qu’un programme en C ou en Fortran requiert une `compilation
<https://docs.alliancecan.ca/wiki/MPI/fr#Cadre_d'ex%C3%A9cution>`__ avant de
pouvoir exécuter le programme, un script en Python est compilé lors de son
exécution.

Lancement d’un programme MPI
''''''''''''''''''''''''''''

Le lancement d’un programme MPI se fait typiquement à l’aide d’une commande
``mpirun`` ou ``mpiexec``. Par exemple :

.. code-block:: console

    mpiexec -n 120 python script.py

La commande ci-dessus lancerait 120 processus identiques, chacun exécutant
``python`` sur un processeur. Avec l’ordonnanceur `Slurm
<https://slurm.schedmd.com/>`__, nous allons plutôt utiliser la commande
``srun``. Par exemple :

.. code-block:: console

    [alice@narval1 ~]$ srun -n 10 hostname
    compute-node2
    compute-node2
    compute-node2
    compute-node2
    compute-node2
    compute-node1
    compute-node1
    compute-node1
    compute-node1
    compute-node1

Exercice #1 - Premier lancement
'''''''''''''''''''''''''''''''

**Objectif** : exécuter un premier code MPI.

**Instructions**

#. Allez dans le répertoire de l’exercice avec la commande
   ``cd ~/mpi201-main/lab/bonjour``.
#. Validez les modules et chargez les modules manquants, au besoin :

   .. code-block:: console

       [alice@narval1 bonjour]$ module list
       [alice@narval1 bonjour]$ module load mpi4py/4.0.3

#. Avec ``srun``, lancez 4 processus ``python`` avec le script ``bonjour.py`` :

   .. code-block:: console

       [alice@narval1 bonjour]$ srun -n 4 python bonjour.py
       Ici le processus 3 de 4
       Ici le processus 2 de 4
       Ici le processus 0 de 4
       Ici le processus 1 de 4

.. note::

    Tel que vu dans cet exercice, l’ordre d’affichage des résultats peut varier
    à cause de l’exécution des différents processus en simultané : leur durée
    peut varier et le système d’exploitation peut parfois favoriser légèrement
    certains processus.

Les communications via MPI
--------------------------

Voici quelques informations à savoir avant de programmer toute communication.

- **Les types de données**

  - La bibliothèque ``mpi4py`` `sérialise
    <https://fr.wikipedia.org/wiki/S%C3%A9rialisation>`__ automatiquement tout
    objet et envoie simplement un vecteur d’octets.
  - À la réception d’un message, l’objet est reconstitué.
  - La gestion des types se fait donc automatiquement.

- **Les types de communications**

  - :doc:`Point-à-point <point-a-point>` : deux processus d’un même
    communicateur communiquent au moyen d’un envoi et d’une réception.
  - :doc:`Collectives <collectives>` : tous les processus d’un même
    communicateur appellent la même fonction et communiquent ensemble.
