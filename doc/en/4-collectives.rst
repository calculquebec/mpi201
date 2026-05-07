Collective communications
=========================

`Français <../fr/4-collectives.html>`_

Collective communications can:

- **move data**;

  - ``comm.bcast()``
  - ``comm.scatter()``
  - ``comm.gather()``

- **do collective computations**.

  - ``comm.reduce()``, ``comm.allreduce()``

Each call to these methods must be made by **all processes of the same
communicator**.

Collective data transfers
-------------------------

Broadcasting data with ``bcast``
''''''''''''''''''''''''''''''''

To send the same information to all processes in a communicator, a `method
<https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.bcast>`__
performing a **broadcast** can be used:

.. figure:: ../images/mpi_bcast_en.svg

With ``mpi4py``, the code would be:

.. code-block:: python

    if rank == 2:
        a = 3
    else:
        a = None

    # bcast(obj: Any, root: int = 0) -> Any

    a = comm.bcast(a, 2)

Data distribution with ``scatter``
''''''''''''''''''''''''''''''''''

To send a portion of the data to each process in a communicator, a `method
<https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.scatter>`__
performing a **distribution** can be used:

.. figure:: ../images/mpi_scatter_en.svg

With ``mpi4py``, the code would be:

.. code-block:: python

    if rank == 2:
        a = [5, 8, 3, 12]
    else:
        a = None

    # scatter(seq_obj: Sequence[Any] | None, root: int = 0) -> Any

    b = comm.scatter(a, 2)

Gathering data with ``gather``
''''''''''''''''''''''''''''''

To retrieve multiple data portions within a single process of a communicator,
the ``gather`` `method
<https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.gather>`__
can be used:

.. figure:: ../images/mpi_gather_en.svg

With ``mpi4py``, the code would be:

.. code-block:: python

    # gather(obj: Any, root: int = 0) -> list[Any] | None

    b = comm.gather(a, 2)

    if rank == 2:
        for value in b:
            print(value)

Workspace partitioning
''''''''''''''''''''''

Before starting an exercise, let's review how to divide the workspace. Recall
the figure we saw in the :ref:`introduction <intro-two-dim-spaces>`:

.. figure:: ../images/parallel-array-2d.svg

One strategy is to divide the workspace into more or less equal portions
**along one dimension**. The goal is to determine at which index a process will
begin its calculation and up to which (excluded) index it must calculate.

- Since the size ``N`` of a dimension is not necessarily an integer multiple of
  ``nranks``, we cannot perform an integer division of ``N`` by ``nranks`` to
  define a single portion size. This would risk omitting elements from the
  calculation.

  .. code-block:: python

      N = 18      # elements
      nranks = 5  # processes or portions
      portion_size = N // nranks  # 3 elements per process

      assert portion_size * nranks == N, f'{portion_size * nranks} != {N}'

      # AssertionError: 15 != 18

- However, we can calculate a lower bound and an upper bound for each portion
  based on the variable ``rank``. In the code below, we see two ways to
  calculate the lower bound ``start``. Subsequently, we would need to use
  ``rank + 1`` in the same formulas to calculate the upper bound ``end``.

  .. code-block:: python

      for rank in range(nranks):
          portion_size = N / nranks  # 3.6
          start_by_size_float = int(portion_size * rank)
          start_by_product_first = rank * N // nranks

          print(start_by_size_float, start_by_product_first)

      # 0 0
      # 3 3
      # 7 7
      # 10 10
      # 14 14

- In the example below, the upper bound ``end`` of the ``rank`` process
  corresponds to the lower bound ``start`` of the ``rank + 1`` process. Thus,
  this bound calculation ensures that none of the ``N`` elements are overlooked
  while maintaining roughly equal calculation portions.

  .. code-block:: python

      for rank in range(nranks):
          # If rank is 0 (the first rank), then start is index 0
          start = rank * N // nranks

          # If rank is nranks-1 (the last rank), then end is index N
          end = (rank + 1) * N // nranks

          print(f'{rank = } : {start = :2d}, {end = :2d} (diff = {end-start})')

      # rank = 0 : start =  0, end =  3 (diff = 3)
      # rank = 1 : start =  3, end =  7 (diff = 4)
      # rank = 2 : start =  7, end = 10 (diff = 3)
      # rank = 3 : start = 10, end = 14 (diff = 4)
      # rank = 4 : start = 14, end = 18 (diff = 4)

- In practice, each process has only one ``rank``, so the two bounds of the
  portion are calculated only once.

  .. code-block:: python

      start = rank * N // nranks
      end = (rank + 1) * N // nranks

      # A selection of your choice
      portion_h = matrix[start:end, :]  # A portion of a few lines
      portion_v = matrix[:, start:end]  # A portion of a few columns

Exercise #4 - Matrix multiplication
'''''''''''''''''''''''''''''''''''

**Objective**: share the calculation of a matrix multiplication.

Since the `matrix multiplication
<https://en.wikipedia.org/wiki/Matrix_multiplication>`__ :math:`A \times B = C`
can be calculated column by column, each process will have the same matrix
:math:`A` and a unique portion of matrix :math:`B`, namely a block of a few
consecutive columns from :math:`B`. The partial products will then be
concatenated horizontally to form the resulting matrix :math:`C`.

.. figure:: ../images/parallel-mat-mul.svg

**Instructions**

#. Go to the exercise directory with ``cd ~/mpi201-main/lab/multiplication``.
#. In `the file
   <https://github.com/calculquebec/mpi201/blob/main/lab/multiplication/matrices_en.py>`__
   ``matrices_en.py``, edit the lines with ``...``. Essentially, the root
   process:

   #. Creates matrix ``A`` and **broadcasts** this matrix to other processes.
   #. Creates roughly equal portions of ``B`` in ``b_list`` and **distributes**
      one portion to each process.
   #. **Gathers** the partial multiplications in ``c_list`` and generates the
      resulting matrix ``C``.

#. Load a ``scipy-stack`` module to gain access to NumPy.
#. Run the program with two (2), three (3) and four (4) processes.

Calculs collectifs
------------------

Opérations de réduction
'''''''''''''''''''''''

C’est l’équivalent d’un ``gather`` avec une boucle effectuant une opération de
réduction. Voici quelques opérations de réduction :

.. list-table:: Opérateurs de réduction
    :header-rows: 1

    * - Opération
      - Opérateur de type ``MPI.Op``
      - Op([3, 5])
    * - `Maximum
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.MAX.html>`__
      - ``MPI.MAX``
      - 5
    * - `Minimum
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.MIN.html>`__
      - ``MPI.MIN``
      - 3
    * - `Somme
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.SUM.html>`__
      - ``MPI.SUM``
      - 8
    * - `Produit
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.PROD.html>`__
      - ``MPI.PROD``
      - 15
    * - `ET logique
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.LAND.html>`__
      - ``MPI.LAND``
      - Vrai
    * - `OU logique
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.LOR.html>`__
      - ``MPI.LOR``
      - Vrai
    * - `OU exclusif logique
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.LXOR.html>`__
      - ``MPI.LXOR``
      - Faux
    * - `ET binaire
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.BAND.html>`__
      - ``MPI.BAND``
      - 1 (011 & 101 = 001)
    * - `OU binaire
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.BOR.html>`__
      - ``MPI.BOR``
      - 7 (011 | 101 = 111)
    * - `OU exclusif binaire
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.BXOR.html>`__
      - ``MPI.BXOR``
      - 6 (011 ^ 101 = 110)

Réduction avec ``reduce``
'''''''''''''''''''''''''

Voici un exemple de `réduction
<https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.reduce>`__
effectuant une somme :

.. figure:: ../images/mpi_reduce_en.svg

Avec ``mpi4py``, on aurait le code suivant :

.. code-block:: python

    # reduce(envoi: Any, op: Op=SUM, racine: int = 0) -> Any | None

    b = comm.reduce(a, MPI.SUM, 2)

Réduction et diffusion avec ``allreduce``
'''''''''''''''''''''''''''''''''''''''''

C’est l’équivalent de ``reduce`` + ``bcast``, mais en `plus efficace
<https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.allreduce>`__ :

.. figure:: ../images/mpi_allreduce_en.svg

Avec ``mpi4py``, on aurait le code suivant :

.. code-block:: python

    # allreduce(envoi: Any, op: Op=SUM) -> Any

    b = comm.allreduce(a, MPI.SUM)

Division de l’espace de calcul
''''''''''''''''''''''''''''''

On se rappelle cette figure vue en :ref:`introduction <intro-linear-spaces>`:

.. figure:: ../images/parallel-reduction_en.svg

- La stratégie qui consiste à diviser l’espace de calcul en portions plus
  ou moins égales fonctionne encore.

  .. code-block:: python

      borne_inf = rank * N // nranks        # borne inférieure
      borne_sup = (rank + 1) * N // nranks  # borne supérieure

      # Boucle dans l'intervalle : borne_inf <= k < borne_sup
      for k in range(borne_inf, borne_sup):
          ...

- Une seconde stratégie consiste à définir une boucle qui débute à ``rank``,
  effectue des sauts de ``nranks`` et itère jusqu’à la fin de l’espace de
  calcul. Ainsi, chaque processus débute la boucle à un indice différent.

  .. code-block:: python

      for k in range(rank, N, nranks):
          ...

Selon le calcul effectué, il se pourrait que l’une de ces deux stratégies donne
un résultat numérique plus stable.

Exercice #5 - Approximation de :math:`\pi`
''''''''''''''''''''''''''''''''''''''''''

**Objectif** : diviser le calcul d’une longue série approximant la constante
:math:`\pi`.

Étant donné :

.. math::

    \pi = 4 \times \frac{\pi}{4} = 4 \times \arctan(1)

Et étant donné `la série de Taylor
<https://fr.wikipedia.org/wiki/S%C3%A9rie_de_Taylor>`__ :

.. math::

    \arctan(1) = \sum_{k=0}^{\infty} \frac{(-1)^k}{2k + 1}

Il est donc possible d'approximer :math:`\pi` au moyen de :math:`N` termes :

.. math::

    \pi \approx 4 \times \sum_{k=0}^{N - 1} \frac{(-1)^k}{2k + 1}

Avec :

.. math::

    4 \times (-1)^k & = & \: 4 \times (1 - 2 \times (k \bmod 2)) \\\\
                    & = & \: 4 - 8 \times (k \bmod 2)

Numériquement, l’accumulation des termes doit se faire dans l’ordre inverse,
c’est-à-dire en commençant par le plus petit des termes, donc avec l’indice
:math:`k=N-1`. Cela permet d’accumuler avec précision les plus petits termes
tout en minimisant l’accumulation d’erreurs dans les bits les moins
significatifs du résultat final.

**Instructions**

#. Allez dans le répertoire de l’exercice avec la commande
   ``cd ~/mpi201-main/lab/pi``.
#. Dans `le fichier
   <https://github.com/calculquebec/mpi201/blob/main/lab/pi/pi-sauts.py>`__
   ``pi-sauts.py``, complétez la conversion du programme séquentiel en
   programme utilisant MPI.

   #. Utilisez la stratégie qui consiste à **faire des sauts** de ``nranks``
      dans une boucle débutant à une valeur de ``k`` égale à ``rank``.
   #. Programmez une réduction des variables locales ``somme`` dans la variable
      ``pi`` du processus 0.
   #. Lancez le programme avec ``1``, ``2``, ``3`` et ``4`` processus.

      #. Utilisez ``time -p`` pour mesurer le temps réel écoulé. Par exemple,
         ``srun -n 2 time -p python pi-sauts.py``.
      #. Observez la précision de l’approximation de pi et le temps ``real`` de
         chaque processus.

#. Dans `le fichier
   <https://github.com/calculquebec/mpi201/blob/main/lab/pi/pi-blocs.py>`__
   ``pi-blocs.py``, complétez la conversion du programme séquentiel en
   programme utilisant MPI.

   #. Utilisez la stratégie qui consiste à **boucler d’une borne inférieure à
      une borne supérieure**.
   #. Refaites les étapes 2.2 (réduction) et 2.3 (expérimentation) ci-dessus,
      mais pour le fichier ``pi-blocs.py``.
