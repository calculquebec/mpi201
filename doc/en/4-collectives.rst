Collective communications
=========================

`Français <../fr/4-collectives.html>`_

Les communications collectives peuvent faire :

- Des **déplacements de données**.

  - ``comm.bcast()``
  - ``comm.scatter()``
  - ``comm.gather()``

- Des **calculs collectifs**.

  - ``comm.reduce()``, ``comm.allreduce()``

Chaque appel à ces méthodes doit être fait par **tous les processus d’un même
communicateur**.

Déplacements de données
-----------------------

Diffusion de données avec ``bcast``
'''''''''''''''''''''''''''''''''''

Pour envoyer les mêmes informations à tous les processus d’un même
communicateur, on utilise une `méthode
<https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.bcast>`__
effectuant une **diffusion** :

.. figure:: ../images/mpi_bcast_en.svg

Avec ``mpi4py``, on aurait le code suivant :

.. code-block:: python

    if rank == 2:
        a = 3
    else:
        a = None

    # bcast(objet: Any, racine: int = 0) -> Any

    a = comm.bcast(a, 2)

Distribution de données avec ``scatter``
''''''''''''''''''''''''''''''''''''''''

Pour envoyer une portion des données à chaque processus d’un même
communicateur, on utilise une `méthode
<https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.scatter>`__
effectuant une **distribution** :

.. figure:: ../images/mpi_scatter_en.svg

Avec ``mpi4py``, on aurait le code suivant :

.. code-block:: python

    if rank == 2:
        a = [5, 8, 3, 12]
    else:
        a = None

    # scatter(envoi: Sequence[Any] | None, racine: int = 0) -> Any

    b = comm.scatter(a, 2)

Regroupement de données avec ``gather``
'''''''''''''''''''''''''''''''''''''''

Pour récupérer plusieurs portions de données dans un seul processus d’un
communicateur, on utilise une `méthode
<https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.gather>`__
effectuant un **regroupement** :

.. figure:: ../images/mpi_gather_en.svg

Avec ``mpi4py``, on aurait le code suivant :

.. code-block:: python

    # gather(envoi: Any, racine: int = 0) -> list[Any] | None

    b = comm.gather(a, 2)

    if rank == 2:
        for valeur in b:
            print(valeur)

Division de l’espace de travail
'''''''''''''''''''''''''''''''

Avant de se lancer avec un exercice, revoyons comment diviser l’espace de
travail. On se rappelle cette figure vue en
:ref:`introduction <intro-two-dim-spaces>`:

.. figure:: ../images/parallel-array-2d.svg

Une première stratégie consiste à diviser l’espace de travail en portions plus
ou moins égales **selon une dimension**. L’objectif est de déterminer à quel
indice un processus débutera son calcul et jusqu’à quel indice (exclus) il doit
calculer.

- Puisque la taille ``N`` d’une dimension n’est pas nécessairement un multiple
  entier de ``nranks``, on ne peut pas faire une division entière de ``N`` par
  ``nranks`` pour définir une taille unique de portion. On risquerait alors
  d’oublier des éléments à calculer.

  .. code-block:: python

      N = 18      # éléments
      nranks = 5  # processus ou portions
      taille_portion = N // nranks  # 3 éléments par processus

      assert taille_portion * nranks == N, f'{taille_portion * nranks} != {N}'

      # AssertionError: 15 != 18

- Par contre, on peut calculer une borne inférieure et une borne supérieure
  pour chaque portion en fonction de la variable ``rank``. Dans le code
  ci-dessous, on voit deux façons de calculer la borne inférieure ``debut``.
  Par la suite, il faudrait utiliser ``rank + 1`` dans les mêmes formules pour
  calculer la borne supérieure ``fin``.

  .. code-block:: python

      for rank in range(nranks):
          taille_portion = N / nranks  # 3.6
          debut_par_taille_float = int(taille_portion * rank)
          debut_produit_dabord = rank * N // nranks

          print(debut_par_taille_float, debut_produit_dabord)

      # 0 0
      # 3 3
      # 7 7
      # 10 10
      # 14 14

- Dans l’exemple ci-dessous, la borne supérieure ``fin`` du processus ``rank``
  correspond à la borne inférieure ``debut`` du processus ``rank + 1``. Ainsi,
  ce calcul des bornes permet de n’oublier aucun des ``N`` éléments tout en
  ayant des portions de calcul plus ou moins égales.

  .. code-block:: python

      for rank in range(nranks):
          # Si rank vaut 0 (le premier rang), debut vaut 0
          debut = rank * N // nranks

          # Si rank vaut nranks-1 (le dernier rang), fin vaut N
          fin = (rank + 1) * N // nranks

          print(f'{rank = } : {debut = :2d}, {fin = :2d} (diff = {fin-debut})')

      # rank = 0 : debut =  0, fin =  3 (diff = 3)
      # rank = 1 : debut =  3, fin =  7 (diff = 4)
      # rank = 2 : debut =  7, fin = 10 (diff = 3)
      # rank = 3 : debut = 10, fin = 14 (diff = 4)
      # rank = 4 : debut = 14, fin = 18 (diff = 4)

- En pratique, chaque processus n'a qu'un seul ``rank``, alors les deux bornes
  de la portion sont calculées une seule fois.

  .. code-block:: python

      debut = rank * N // nranks
      fin = (rank + 1) * N // nranks

      # Une sélection au choix
      portion_h = matrice[debut:fin, :]  # Une portion de quelques lignes
      portion_v = matrice[:, debut:fin]  # Une portion de quelques colonnes

Exercice #4 - Multiplication de matrices
''''''''''''''''''''''''''''''''''''''''

**Objectif** : partager le calcul d’une multiplication de matrices.

Étant donné que `le produit matriciel
<https://fr.wikipedia.org/wiki/Produit_matriciel>`__ :math:`A \times B = C`
peut se calculer colonne par colonne, chaque processus aura la même matrice
:math:`A` et une portion unique de la matrice :math:`B`, soit un bloc de
quelques colonnes consécutives de :math:`B`. Les produits partiels seront
ensuite concaténés horizontalement pour former la matrice résultante :math:`C`.

.. figure:: ../images/parallel-mat-mul.svg

**Instructions**

#. Allez dans le répertoire de l’exercice avec la commande
   ``cd ~/mpi201-main/lab/mat_mul``.
#. Dans `le fichier
   <https://github.com/calculquebec/mpi201/blob/main/lab/mat_mul/mat_mul.py>`__
   ``mat_mul.py``, éditez les lignes avec des ``...``. Essentiellement, le
   processus racine :

   #. Crée la matrice ``A`` et **diffuse** cette matrice aux autres processus.
   #. Crée des portions plus ou moins égales de ``B`` dans ``b_list`` et
      **distribue** une portion à chaque processus.
   #. **Regroupe** les multiplications partielles dans ``c_list`` et génère la
      matrice résultante ``C``.

#. Chargez un module ``scipy-stack`` pour avoir accès à NumPy.
#. Lancez le programme avec deux (2), trois (3) et quatre (4) processus.

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
