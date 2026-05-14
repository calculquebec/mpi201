Parallel Programming with MPI4py
================================

`Français <../fr/index.html>`_

About
-----

- This training workshop is at an intermediate level.
- The main objective is to learn how to use an **inter-process communication
  library** to do distributed parallel computing.
- The different concepts are shown with examples in Python, but they are
  classically programmed in C/C++ and Fortran.

Table of contents
-----------------

#. :doc:`1-introduction`

   #. Distributed memory machine
   #. Questions to ask yourself
   #. Calculation division strategies

#. :doc:`2-mpi`

   #. What is MPI?
   #. Structure of an MPI code
   #. Explicit parallelization
   #. MPI Environment
   #. Communications via MPI

#. :doc:`3-point-to-point`

   #. Sending and receiving data
   #. Avoiding deadlock situations
   #. Non-blocking communications

#. :doc:`4-collectives`

   #. Collective data transfers
   #. Collective calculations

#. :doc:`5-conclusion`

.. note::

    This workshop was designed for guided sessions with a Calcul Québec
    instructor on our cloud computing platform. The files necessary for the
    exercises are in your home directory on the platform.

    You can also follow this workshop on your own and do the exercises on any
    Calcul Québec or Digital Research Alliance of Canada cluster. Your jobs’
    wait time, however, will be longer than on the cloud platform. Download the
    necessary files with the following command or `browse them online
    <https://github.com/calculquebec/mpi201>`__:

    .. code-block:: console

        git clone https://github.com/calculquebec/mpi201 mpi201-main

.. toctree::
    :caption: Chapters
    :maxdepth: 2
    :titlesonly:
    :hidden:

    1-introduction
    2-mpi
    3-point-to-point
    4-collectives
    5-conclusion
    8-appendix

.. toctree::
    :caption: Reference
    :maxdepth: 2
    :titlesonly:
    :hidden:

    90-cheatsheet
    99-bibliography

.. toctree::
    :caption: External links
    :hidden:

    Alliance Technical Documentation <https://docs.alliancecan.ca/wiki/Technical_documentation/en>
    Calcul Québec Training <https://www.calculquebec.ca/en/academic-research-services/training/>
