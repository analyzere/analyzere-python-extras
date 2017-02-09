
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

   g = LayerViewDigraph(lv)  # defaults: with_terms=True, compact=True, rankdir='TB'
   g = LayerViewDigraph(lv, with_terms=False)  # omit Layer terms from nodes
   g = LayerViewDigraph(lv, compact=False) # graph duplicate nodes
   g = LayerViewDigraph(lv, rankdir='LR')  # render the graph from Left to Right
   g = LayerViewDigraph(lv, warnings=False)  # disable error node highlighting

Then to render your graph::

   g.render()  # defaults: filename=None, view=True, format=None, rankdir=None
   g.render(filename='mygraph') # write graph to 'mygraph'
   g.render(view=True)    # attempt to auto display the graph
   g.render(format='pdf')  # change the output format 'pdf'
   g.render(rankdir='LR')  # render the graph from Left to Right

Shortcut: generate a graph for a given LayerView Id::

   graph = LayerViewDigraph.from_id('011785b1-203b-696e-424e-7da9b0ec779a')

Sample images:

+----------+----------+-------------+-----------+---------------------------------------------------------------------+
| rankdir= | compact= | with_terms= | warnings= | sample image                                                        |
+==========+==========+=============+===========+=====================================================================+
| 'BT'     | True     | True        | True      | `</examples/BT_compact_with-terms_warnings-enabled.png>`_           |
+----------+----------+-------------+-----------+---------------------------------------------------------------------+
| 'LR'     | True     | True        | True      | `</examples/LR_compact_with-terms_warnings-enabled.png>`_           |
+----------+----------+-------------+-----------+---------------------------------------------------------------------+
| 'BT'     | True     | True        | False     | `</examples/BT_compact_with-terms_warnings-disabled.png>`_          |
+----------+----------+-------------+-----------+---------------------------------------------------------------------+
| 'LR'     | True     | True        | False     | `</examples/LR_compact_with-terms_warnings-disabled.png>`_          |
+----------+----------+-------------+-----------+---------------------------------------------------------------------+
| 'BT'     | True     | False       | True      | `</examples/BT_compact_without-terms_warnings-enabled.png>`_        |
+----------+----------+-------------+-----------+---------------------------------------------------------------------+
| 'LR'     | True     | False       | True      | `</examples/LR_compact_without-terms_warnings-enabled.png>`_        |
+----------+----------+-------------+-----------+---------------------------------------------------------------------+
| 'BT'     | False    | False       | False     | `</examples/BT_not-compact_without-terms_warnings-disabled.png>`_   |
+----------+----------+-------------+-----------+---------------------------------------------------------------------+
| 'LR'     | False    | False       | False     | `</examples/LR_not-compact_without-terms_warnings-disabled.png>`_   |
+----------+----------+-------------+-----------+---------------------------------------------------------------------+


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
