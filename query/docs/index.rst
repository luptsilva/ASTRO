.. query_hyperleda documentation master file, created by
   sphinx-quickstart on Tue Mar 23 12:34:35 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Query HyperLEDA (query.hyperleda) documentation
================================================


(NB: I’m making this module available for an early use, while waiting
for PR review `2023 <https://github.com/astropy/astroquery/pull/2023>`_ to `astroquery <https://github.com/astropy/astroquery>`_).

Brief description
-----------------

This module can be used to query from the `HyperLEDA <http://leda.univ-lyon1.fr/>`_ web service. The
queries will return the resultsin an astropy `Table <https://docs.astropy.org/en/stable/api/astropy.table.Table.html#astropy.table.Table>`_. Below are two
working examples illustrating how to retrieve data for a single
object,or using an SQL query request to the `HyperLEDA SQL data access
service <http://leda.univ-lyon1.fr/fullsql.html>`_.

.. toctree::
   :maxdepth: 4
   :caption: Contents:
   
   examples.rst

API query.hyperleda
===================
.. automodule:: query
   :members: hyperleda, HyperLEDAClass

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
