Communications point-à-point
============================

`English <../en/point-to-point.html>`_

- Elles sont *locales*, c’est-à-dire que seuls **deux processus** sont
  impliqués : ils sont les seuls à appeler réciproquement des fonctions de
  communication, donc ils sont les seuls à participer à cet échange.

  - Les appels aux fonctions d’envoi et de réception viennent donc toujours par
    paires sur des processus différents.

- Les fonctions d’envoi et de réception peuvent être bloquantes ou non.

Envois et réceptions (bloquants)
--------------------------------

Avec ``mpi4py``, les envois de données se font à partir d’un communicateur
(``comm``) et de la `méthode
<https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.send>`__
``send()`` :

.. code-block:: python

    comm.send(envoi, dest=dest, tag=etiquette)

- ``comm`` : par exemple, ``MPI.COMM_WORLD``.
- ``envoi`` : n’importe quel objet sérialisable via `pickle
  <https://docs.python.org/3/library/pickle.html#module-pickle>`__.
- ``dest`` : rang du processus recevant des données.
- ``etiquette`` : nombre entier au choix identifiant le type de transfert.

Réciproquement, les réceptions de données se font à partir du même
communicateur et de la `méthode
<https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.recv>`__
``recv()`` :

.. code-block:: python

    recept = comm.recv(source=source, tag=etiquette, status=etat)

- ``recept`` : une variable ou une partie d’un objet modifiable, pour recevoir
  l’objet désérialisé.
- ``source`` : ``MPI.ANY_SOURCE`` (valeur par défaut) ou un rang précis.
- ``etiquette`` : ``MPI.ANY_TAG`` (valeur par défaut) ou un nombre précis.
- ``etat`` : ``None`` (valeur par défaut) ou objet de type ``MPI.Status``.

  - ``.count`` : nombre d’octets reçus.
  - ``.source`` : rang de la source des données.
  - ``.tag`` : étiquette du transfert.

Exemple - Envoi et réception
''''''''''''''''''''''''''''

Chaque processus a ses propres variables ``a`` et ``b``.
Le processus 2 envoie la valeur de sa variable ``a`` vers
le processus 0 qui reçoit cette valeur via sa variable ``b``.

.. figure:: ../images/mpi_point2point_fr.svg

Avec ``mpi4py``, voici une implémentation de cette communication :

.. code-block:: python

    if proc == 2:
        comm.send(a, dest=0, tag=746)
    elif proc == 0:
        b = comm.recv(source=2, tag=746)

Exercice #2 - Envoi d’une matrice
'''''''''''''''''''''''''''''''''

**Objectif** : envoyer une matrice 4x4 du processus 0 au processus 1.

**Instructions**

#. Allez dans le répertoire de l’exercice avec la commande
   ``cd ~/mpi201-main/lab/send_matrix``.
#. Éditez le fichier ``send_matrix.py`` pour programmer le transfert de la
   matrice.
#. Lancez ce programme avec deux (2) processus.

Éviter les situations d’interblocage
------------------------------------

Soit le code suivant :

.. code-block:: python
    :emphasize-lines: 2,5

    if proc == 0:
        comm.ssend(a, dest=2, tag=10)
        b = comm.recv(source=2, tag=11)
    elif proc == 2:
        comm.ssend(b, dest=0, tag=11)
        a = comm.recv(source=0, tag=10)

- La `méthode
  <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.ssend>`__
  ``ssend()`` est une version synchrone de ``send()``, ce qui la rend toujours
  bloquante.
- Dans le cas ci-dessus, les deux processus attendent que l’autre fasse appel
  à ``recv()``. Bref, ce code est **erroné** et cause un interblocage.
- Avec la méthode standard ``send()``, le code resterait à risque ; la
  quantité de mémoire tampon étant limitée, le code bloquera lors de l’échange
  de gros messages.

Solution 1
''''''''''

On change l’ordre des appels à ``ssend()`` et ``recv()`` pour un des deux
processus. Par exemple :

.. code-block:: python
    :emphasize-lines: 5-6

    if proc == 0:
        comm.ssend(a, dest=2, tag=10)
        b = comm.recv(source=2, tag=11)
    elif proc == 2:
        a = comm.recv(source=0, tag=10)
        comm.ssend(b, dest=0, tag=11)

On peut généraliser la technique à plus de processus :

- Les processus pairs commencent par envoyer.
- Les processus impairs commencent par recevoir.

Exercice #3 - Échange de vecteurs
'''''''''''''''''''''''''''''''''

**Objectif** : échanger un petit vecteur de données.

**Instructions**

#. Allez dans le répertoire de l’exercice avec la commande
   ``cd ~/mpi201-main/lab/exchange``.
#. Éditez le fichier ``exchange.py`` pour programmer l’échange de données.
#. Lancez ce programme avec deux (2) processus.

Solution 2
''''''''''

On utilise des communications non bloquantes pour démarrer les transferts.
Ainsi, même si l’envoi n’est pas terminé, on peut commencer la réception tout
en évitant l’interblocage. Par exemple :

.. code-block:: python
    :emphasize-lines: 2,5,8

    if proc == 0:
        requete = comm.isend(a, dest=2, tag=10)
        b = comm.recv(source=2, tag=11)
    elif proc == 2:
        requete = comm.isend(b, dest=0, tag=11)
        a = comm.recv(source=0, tag=10)

    requete.wait()

Communications non bloquantes
-----------------------------

Avec ``mpi4py``, les communicateurs ont les `méthodes
<https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html>`__
suivantes :

.. code-block:: python
    :emphasize-lines: 1,4

    requete = comm.isend(envoi, dest, tag=0)
    requete.wait()

    requete = comm.irecv(source=ANY_SOURCE, tag=ANY_TAG)
    recept = requete.wait(status=None)

- Il n’est pas nécessaire que l’envoi et la réception soient tous les deux non
  bloquants (toutes les combinaisons sont permises).
- Après l’appel à ``isend()`` ou ``irecv()``, on doit utiliser la variable
  ``requete`` pour s’assurer que la communication est complétée.

  - La `méthode
    <https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Request.html#mpi4py.MPI.Request.wait>`__
    ``wait()`` est bloquante et retourne quand la communication est terminée.
  - Lors d’une réception, c’est ``requete.wait()`` qui retourne l’objet reçu.

- Quand la communication a terminé, on peut réutiliser les objets transmis ou
  reçus.
