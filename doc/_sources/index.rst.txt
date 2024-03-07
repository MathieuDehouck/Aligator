.. toctree::
   :maxdepth: 2


------


.. py:module:: app.v1_1.main

app.v1_1.main.py
^^^^^^^^^^^^^^^^

Contains the **hinge** between the Python pun-generating back-end application the HTML/JavaScript front-end website.
The **hinge** itself is written in Python using the FastAPI

------

app.v1_1.aligator_core.py
^^^^^^^^^^^^^^^^^^^^^^^^^

Contains functions that support joke generation for AliGator version 1.1 (lemmas taken from Wiktionary and most inflected forms discarded).

.. automodule:: app.v1_1.aligator_core
   :members:


------

app.core.Trie.py
^^^^^^^^^^^^^^^^

.. 
	.. automodule:: app.core.Trie
.. autoclass:: app.core.Trie.Trie
   :members:
   
.. autoclass:: app.core.Trie.Node
   :members:
	
------
	
app.core.Pronunciation_state_machine.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: app.core.Pronunciation_state_machine
   :members:
   
------

..  app.core.Load_trees.py
..	^^^^^^^^^^^^^^^^^^^^^^
..
  	.. automodule:: app.core.Load_trees
  	   :members:
   
   
