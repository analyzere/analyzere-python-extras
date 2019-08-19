
Analyzere Python Client Extras  |travis| |Code Health|
======================================================


An extension to the analyzere python library that facilitates "extras"
including visualizations of Analyze Re LayerView objects.

.. |travis| image:: https://travis-ci.org/analyzere/analyzere-python-extras.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/analyzere/analyzere-python-extras
.. |Code Health| image:: https://landscape.io/github/analyzere/analyzere-python-extras/master/landscape.svg?style=flat
   :target: https://landscape.io/github/analyzere/analyzere-python-extras/master
   :alt: Code Health

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


max_depth=0
  The maximum depth of the graph to process.  For very deeply nested structures this can reduce the size.  (default=0 == all levels).

max_sources=0
  The maximum number of Loss sources to graph in detail for a single node. (default=0 == all sources).

colors=[1-12]
  The number of colors to be used when coloring nodes and edges. (default=1 == black, max=12).

color_mode=['breadth'|'depth']
  The mode to use when applying colors. Options include: ['breadth', 'depth'], default: 'breadth'.


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


**Colorization:**

+------------------------------------------------+-------------------------------------------------------------------+
| ``LayerViewDigraph(lv, ...)``                  |         ``render(...)``                                           |
+--------------+-------------+-------------------+-------------------------------------------------------------------+
| ``compact=`` | ``colors=`` | ``color_mode=``   |      ``rankdir='BT'``                                             |
+==============+=============+===================+===================================================================+
| *True*       | **4**       | *breadth*         | |BT_compact_with-terms_warnings-disabled_4-colors-by-breadth|     |
+--------------+-------------+-------------------+-------------------------------------------------------------------+
| *True*       | **4**       | **depth**         | |BT_compact_with-terms_warnings-disabled_4-colors-by-depth|       |
+--------------+-------------+-------------------+-------------------------------------------------------------------+
| **False**    | **4**       | *breadth*         | |BT_not-compact_with-terms_warnings-disabled_4-colors-by-breadth| |
+--------------+-------------+-------------------+-------------------------------------------------------------------+
| **False**    | **4**       | **depth**         | |BT_not-compact_with-terms_warnings-disabled_4-colors-by-depth|   |
+--------------+-------------+-------------------+-------------------------------------------------------------------+

.. |BT_compact_with-terms_warnings-disabled_4-colors-by-breadth| image:: /examples/BT_compact_with-terms_warnings-disabled_4-colors-by-breadth.png
   :width: 40pt
.. |BT_compact_with-terms_warnings-disabled_4-colors-by-depth| image:: /examples/BT_compact_with-terms_warnings-disabled_4-colors-by-depth.png
   :width: 40pt
.. |BT_not-compact_with-terms_warnings-disabled_4-colors-by-breadth| image:: /examples/BT_not-compact_with-terms_warnings-disabled_4-colors-by-breadth.png
   :width: 40pt
.. |BT_not-compact_with-terms_warnings-disabled_4-colors-by-depth| image:: /examples/BT_not-compact_with-terms_warnings-disabled_4-colors-by-depth.png
   :width: 40pt


Usage
-----

In order to make use of the tools in the `analyzere_extras`
module you will need to import the `analyzere` module.

You will need to define your connection information::

   import analyzere
   analyzere.base_url = '<your server url>'
   analyzere.username = '<your userid>'
   analyzere.password = '<your password>'

Visualization
~~~~~~~~~~~~~

To make use of the visualization tool, you will need to query a LayerView
that you would like to graph::

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

ELT Combination
~~~~~~~~~~~~~~~

To make use of the ELT combiner tool, you will need to define the list of
uuids representing the resources with ELTs that you would like to combine::

   uuid_list = ['26a8f73b-0fbb-46c7-8dcf-f4de1e222994', 'cd67ba03-302b-45e5-9341-a4267875c1f8']

You will need to indicate which catalog these ELTs correspond to::

  catalog_uuid = '61378251-ce85-4b6e-a63c-f5d67c4e4877'

Then to combine the ELTs into a single ELT::

  from analyzere_extras.combine_elts import ELTCombiner

  elt_combiner = ELTCombiner()

  combined_elt = elt_combiner.combine_elts_from_resources(
    uuid_list,
    catalog_uuid,
    uuid_type='all',
    description='My Combined ELT'
  )

``uuid_type`` specifies which the type of resources in ``uuid_list``. Valid
values for ``uuid_type`` are:

  - ``'Portfolio'``
  - ``'PortfolioView'``
  - ``'Layer'``
  - ``'LayerView'``
  - ``'LossSet'``
  - ``'all'``

If ``uuid_type='all'`` is set, then the resources in ``uuid_list`` can be a mix
of Portfolios, PortfolioViews, Layers, LayerViews, and LossSets. The default
value of ``uuid_type`` is ``'all'``.

``description`` defines the description for the uploaded combined ELT. If not
set, the default is ``'analyzere-python-extras: Combined ELT'``.

Testing
-------

We currently commit to being compatible with Python 2.7 and Python 3.4 to 3.7.
In order to run tests against against each environment we use
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

4. Package source and wheel distributions::

    python setup.py sdist bdist_wheel

5. Upload to PyPI with twine::

    twine upload dist/*
