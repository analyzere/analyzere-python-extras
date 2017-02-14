
Analyzere Python Client Extras  |travis|
========================================


An extension to the analyzere python library that facilitates "extras"
including visualizations of Analyze Re LayerView objects.

.. |travis| image:: https://travis-ci.org/analyzere/analyzere-python-extras.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/analyzere/analyzere-python-extras

Installation
------------

::

   pip install analyzere_extras


Graphing Options
----------------

This graphing utility provides some methods of controlling the style and format of the rendered image.

rankdir='XX'
  Option that controls the orientation of the graph. Options include:

  - 'BT' bottom to top (default)
  - 'TB' top to bottom
  - 'LR' left to right
  - 'RL' right to left

compact=True|False
  Controls if duplicate nodes should be omitted (default=True).  This option tends to produce smaller graphs, which should be easier to read.

with_terms=True|False
  Specify that a Layer's terms are included in each node of the graph (default=True).

warnings=True|False
  Highlight nodes with suspicious terms by coloring the node red. Warning nodes are generated when any of the following conditions are true:

  - ``participation = 0.0``
  - ``invert = true`` and ``filters = []``
  - ``attachment`` or ``aggregate_attachment`` = unlimited


**Sample LayerView Images:**

+------------------------------------------------+-----------------------------------------------------------------------------------------------------+
| ``LayerViewDigraph(lv, ...)``                  |         ``render(...)``                                                                             |
+--------------+-----------------+---------------+--------------------------------------------------+--------------------------------------------------+
| ``compact=`` | ``with_terms=`` | ``warnings=`` |      ``rankdir='BT'``                            | ``rankdir='LR'``                                 |
+==============+=================+===============+==================================================+==================================================+
| *True*       | *True*          | *True*        | |BT_compact_with-terms_warnings-enabled|         | |LR_compact_with-terms_warnings-enabled|         |
+--------------+-----------------+---------------+--------------------------------------------------+--------------------------------------------------+
| *True*       | *True*          | **False**     | |BT_compact_with-terms_warnings-disabled|        | |LR_compact_with-terms_warnings-disabled|        |
+--------------+-----------------+---------------+--------------------------------------------------+--------------------------------------------------+
| *True*       | **False**       | *True*        | |BT_compact_without-terms_warnings-enabled|      | |LR_compact_without-terms_warnings-enabled|      |
+--------------+-----------------+---------------+--------------------------------------------------+--------------------------------------------------+
| **False**    | **False**       | **False**     | |BT_not-compact_without-terms_warnings-disabled| | |LR_not-compact_without-terms_warnings-disabled| |
+--------------+-----------------+---------------+--------------------------------------------------+--------------------------------------------------+

.. |BT_compact_with-terms_warnings-enabled| image:: /examples/BT_compact_with-terms_warnings-enabled.png
   :width: 40pt
.. |LR_compact_with-terms_warnings-enabled| image:: /examples/LR_compact_with-terms_warnings-enabled.png
   :width: 40pt
.. |BT_compact_with-terms_warnings-disabled| image:: /examples/BT_compact_with-terms_warnings-disabled.png
   :width: 40pt
.. |LR_compact_with-terms_warnings-disabled| image:: /examples/LR_compact_with-terms_warnings-disabled.png
   :width: 40pt
.. |BT_compact_without-terms_warnings-enabled| image:: /examples/BT_compact_without-terms_warnings-enabled.png
   :width: 40pt
.. |LR_compact_without-terms_warnings-enabled| image:: /examples/LR_compact_without-terms_warnings-enabled.png
   :width: 40pt
.. |BT_not-compact_without-terms_warnings-disabled| image:: /examples/BT_not-compact_without-terms_warnings-disabled.png
   :width: 40pt
.. |LR_not-compact_without-terms_warnings-disabled| image:: /examples/LR_not-compact_without-terms_warnings-disabled.png
   :width: 40pt


Usage
-----

In order to make use of the visualization tools in the `analyzere_extras`
module you will need to import the `analyzere` module.

First you will need to define your connection information::

   import analyzere
   analyzere.base_url = '<your server url>'
   analyzere.username = '<your userid>'
   analyzere.password = '<your password>'

Then you will need to query a LayerView that you would like to graph::

   from analyzere import LayerView

   lv = analyzere.LayerView.retrieve('011785b1-203b-696e-424e-7da9b0ec779a')

Now you can generate a graph of your LayerView::

   from analyzere_extras.visualizations import LayerViewDigraph

   g = LayerViewDigraph(lv)  # defaults: with_terms=True, compact=True, rankdir='TB', warnings=True
   g = LayerViewDigraph(lv, with_terms=False)  # omit Layer terms from nodes
   g = LayerViewDigraph(lv, compact=False) # graph duplicate nodes
   g = LayerViewDigraph(lv, rankdir='LR')  # render the graph from Left to Right
   g = LayerViewDigraph(lv, warnings=False)  # disable error node highlighting

Then to render your graph::

   g.render()  # defaults: filename=None, view=True, format=None, rankdir=None
   g.render(filename='mygraph') # write graph to 'mygraph'
   g.render(view=True)     # attempt to auto display the graph
   g.render(format='pdf')  # change the output format 'pdf'
   g.render(rankdir='LR')  # render the graph from Left to Right

Shortcut: generate a graph for a given LayerView Id::

   graph = LayerViewDigraph.from_id('011785b1-203b-696e-424e-7da9b0ec779a')


Testing
-------

We currently commit to being compatible with Python 2.7 and Python 3.4. In
order to run tests against against each environment we use
`tox <http://tox.readthedocs.org/>`_ and `py.test <http://pytest.org/>`_. You'll
need an interpreter installed for each of the versions of Python we test.
You can find these via your system's package manager or
`on the Python site <https://www.python.org/downloads/>`_.

To start, install tox::

    pip install tox

Then, run the full test suite::

    tox

To run tests for a specific module, test case, or single test, you can pass
arguments to py.test through tox with ``--``. E.g.::

    tox -- tests/test_base_resources.py::TestReferences::test_known_resource

See ``tox --help`` and ``py.test --help`` for more information.

Publishing
----------

1. Install `twine <https://pypi.python.org/pypi/twine>`_ and
   `wheel <https://pypi.python.org/pypi/wheel>`_::

    pip install twine wheel

2. Increment version number in ``setup.py`` according to
   `PEP 440 <https://www.python.org/dev/peps/pep-0440/>`_.

3. Commit your change to ``setup.py`` and create a tag for it with the version
   number. e.g.::

    git tag 0.1.0
    git push origin 0.1.0

4. Register the package::

    python setup.py register

5. Package source and wheel distributions::

    python setup.py sdist bdist_wheel

6. Upload to PyPI with twine::

    twine upload dist/*
