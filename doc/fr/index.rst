Programmation parallèle avec MPI4py
===================================

`English <../en/index.html>`_

À propos
--------

- Cet atelier de formation est de niveau intermédiaire.
- L’objectif principal est d’apprendre à utiliser une **bibliothèque de
  communication entre processus** pour faire du calcul parallèle distribué.
- Les différents concepts sont montrés avec des exemples en langage Python,
  mais ils sont classiquement programmés en C/C++ et en Fortran.

Table des matières
------------------

#. :doc:`introduction`

   #. Machine à mémoire distribuée
   #. Des questions à se poser
   #. Stratégies de division du calcul

#. :doc:`mpi`

   #. Qu’est-ce que MPI?
   #. Structure d’un code MPI
   #. Parallélisation explicite
   #. Environnement requis pour utiliser MPI
   #. Les communications via MPI

#. :doc:`point-a-point`

   #. Envois et réceptions de données
   #. Éviter les situations d’interblocage
   #. Communications non bloquantes

#. :doc:`collectives`

   #. Déplacements de données
   #. Calculs collectifs

#. :doc:`conclusion`

   #. MPI dans les autres langages
   #. Défis de parallélisation supplémentaires
   #. Bonus - Notions avancées

.. note::
    
    Cet atelier a été conçu pour être guidé par un formateur ou une
    formatrice de Calcul Québec sur notre plateforme infonuagique.
    Les fichiers nécessaires pour les exercices sont dans votre répertoire
    personnel sur la plateforme.

    Si vous suivez cet atelier par vous-même, vous pouvez télécharger
    `les fichiers nécessaires
    <https://github.com/calculquebec/mpi201>`__ et réaliser les
    exercices sur n’importe quelle grappe de Calcul Québec ou de l’Alliance de
    recherche numérique du Canada. Le temps d’attente pour l’exécution des
    tâches sera toutefois plus long que sur la plateforme infonuagique.

.. toctree::
    :caption: Chapitres
    :maxdepth: 2
    :titlesonly:
    :hidden:

    introduction
    mpi
    point-a-point
    collectives
    conclusion

.. toctree::
    :caption: Référence
    :maxdepth: 2
    :titlesonly:
    :hidden:

    aide-memoire
    bibliographie

.. toctree::
    :caption: Liens externes
    :hidden:

    Documentation technique de l’Alliance <https://docs.alliancecan.ca/wiki/Technical_documentation/fr>
    Formations de Calcul Québec <https://www.calculquebec.ca/services-aux-chercheurs/formation/>
