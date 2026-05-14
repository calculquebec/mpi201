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

Collective calculations
-----------------------

Reduction operations
''''''''''''''''''''

This is the equivalent of a ``gather`` with a loop performing a reduction
operation. Here are some reduction operations:

.. list-table:: Reduction operators
    :header-rows: 1

    * - Operation
      - Operator of type ``MPI.Op``
      - Op([3, 5])
    * - `Maximum
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.MAX.html>`__
      - ``MPI.MAX``
      - 5
    * - `Minimum
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.MIN.html>`__
      - ``MPI.MIN``
      - 3
    * - `Sum
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.SUM.html>`__
      - ``MPI.SUM``
      - 8
    * - `Product
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.PROD.html>`__
      - ``MPI.PROD``
      - 15
    * - `Logical AND
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.LAND.html>`__
      - ``MPI.LAND``
      - True
    * - `Logical OR
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.LOR.html>`__
      - ``MPI.LOR``
      - True
    * - `Logical exclusive OR
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.LXOR.html>`__
      - ``MPI.LXOR``
      - False
    * - `Binary AND
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.BAND.html>`__
      - ``MPI.BAND``
      - 1 (011 & 101 = 001)
    * - `Binary OR
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.BOR.html>`__
      - ``MPI.BOR``
      - 7 (011 | 101 = 111)
    * - `Binary exclusive OR
        <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.BXOR.html>`__
      - ``MPI.BXOR``
      - 6 (011 ^ 101 = 110)

Reduction with ``reduce``
'''''''''''''''''''''''''

Here is an example of a `reduction
<https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.reduce>`__
that computes the sum of local results:

.. figure:: ../images/mpi_reduce_en.svg

With ``mpi4py``, the code would be:

.. code-block:: python

    # reduce(obj: Any, op: Op=SUM, root: int = 0) -> Any | None

    b = comm.reduce(a, MPI.SUM, 2)

Reduction and broadcasting with ``allreduce``
'''''''''''''''''''''''''''''''''''''''''''''

It's the equivalent of ``reduce`` + ``bcast``, but it's `more efficient
<https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.allreduce>`__:

.. figure:: ../images/mpi_allreduce_en.svg

With ``mpi4py``, the code would be:

.. code-block:: python

    # allreduce(obj: Any, op: Op=SUM) -> Any

    b = comm.allreduce(a, MPI.SUM)

Division of the calculation space
'''''''''''''''''''''''''''''''''

We recall this figure seen in the :ref:`introduction <intro-linear-spaces>`:

.. figure:: ../images/parallel-reduction_en.svg

- The strategy of dividing the calculation space into more or less equal
  portions still works.

  .. code-block:: python

      start = rank * N // nranks      # lower bound
      end = (rank + 1) * N // nranks  # upper bound

      # Loop in the interval: start <= k < end
      for k in range(start, end):
          ...

- A second strategy involves defining a loop that starts at ``rank``, makes
  jumps of ``nranks``, and iterates until the end of the calculation space.
  Thus, each process starts the loop at a different index.

  .. code-block:: python

      for k in range(rank, N, nranks):
          ...

According to the calculation performed, it is possible that one of these two
strategies will give a more stable numerical result.

Exercise #5 - Approximation of :math:`\pi`
''''''''''''''''''''''''''''''''''''''''''

**Objective**: divide the calculation of a long series approximating the
constant :math:`\pi`.

Given:

.. math::

    \pi = 4 \times \frac{\pi}{4} = 4 \times \arctan(1)

And given `the Taylor series <https://en.wikipedia.org/wiki/Taylor_series>`__:

.. math::

    \arctan(1) = \sum_{k=0}^{\infty} \frac{(-1)^k}{2k + 1}

It is therefore possible to approximate :math:`\pi` with :math:`N` terms:

.. math::

    \pi \approx 4 \times \sum_{k=0}^{N - 1} \frac{(-1)^k}{2k + 1}

With:

.. math::

    4 \times (-1)^k & = & \: 4 \times (1 - 2 \times (k \bmod 2)) \\\\
                    & = & \: 4 - 8 \times (k \bmod 2)

Numerically, the accumulation of terms must be done in reverse order, that is,
starting with the smallest term, therefore with the index :math:`k=N-1`. This
allows the smallest terms to be accumulated accurately while minimizing the
accumulation of errors in the least significant bits of the final result.

**Instructions**

#. Go to the exercise directory with
   ``cd ~/mpi201-main/lab/pi``.
#. In `the file
   <https://github.com/calculquebec/mpi201/blob/main/lab/pi/pi-jumps.py>`__
   ``pi-jumps.py``, complete the conversion of the sequential program into a
   program using MPI.

   #. Use the strategy of **making jumps** of ``nranks`` in a loop starting at
      a value of ``k`` equal to ``rank``.
   #. Program a reduction of the local variables ``my_sum`` into the variable
      ``pi`` of process 0.
   #. Run the program with ``1``, ``2``, ``3`` and ``4`` processes.

      #. Use ``time -p`` to measure the actual elapsed time. For example,
         ``srun -n 2 time -p python pi-jumps.py``.
      #. Observe the accuracy of the approximation of pi and the ``real`` time
         of each process.

#. In `the file
   <https://github.com/calculquebec/mpi201/blob/main/lab/pi/pi-portions.py>`__
   ``pi-portions.py``, complete the conversion of the sequential program into a
   program using MPI.

   #. Use the strategy of **looping from a lower bound to an upper bound**.
   #. Repeat steps 2.2 (reduction) and 2.3 (experimentation) above, but for the
      file ``pi-portions.py``.
