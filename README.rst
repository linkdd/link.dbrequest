link.dbrequests
==========

**link.dbrequests** is a database agnostic query system.

See documentation_ for more informations.

.. _documentation: https://linkutils.readthedocs.io

.. image:: https://img.shields.io/pypi/l/link.dbrequests.svg?style=flat-square
   :target: https://pypi.python.org/pypi/link.dbrequests/
   :alt: License

.. image:: https://img.shields.io/pypi/status/link.dbrequests.svg?style=flat-square
   :target: https://pypi.python.org/pypi/link.dbrequests/
   :alt: Development Status

.. image:: https://img.shields.io/pypi/v/link.dbrequests.svg?style=flat-square
   :target: https://pypi.python.org/pypi/link.dbrequests/
   :alt: Latest release

.. image:: https://img.shields.io/pypi/pyversions/link.dbrequests.svg?style=flat-square
   :target: https://pypi.python.org/pypi/link.dbrequests/
   :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/implementation/link.dbrequests.svg?style=flat-square
   :target: https://pypi.python.org/pypi/link.dbrequests/
   :alt: Supported Python implementations

.. image:: https://img.shields.io/pypi/wheel/link.dbrequests.svg?style=flat-square
   :target: https://travis-ci.org/linkdd/link.dbrequests
   :alt: Download format

.. image:: https://travis-ci.org/linkdd/link.dbrequests.svg?branch=master&style=flat-square
   :target: https://travis-ci.org/linkdd/link.dbrequests
   :alt: Build status

.. image:: https://coveralls.io/repos/github/linkdd/link.dbrequests/badge.png?style=flat-square
   :target: https://coveralls.io/r/linkdd/link.dbrequests
   :alt: Code test coverage

.. image:: https://img.shields.io/pypi/dm/link.dbrequests.svg?style=flat-square
   :target: https://pypi.python.org/pypi/link.dbrequests/
   :alt: Downloads

.. image:: https://landscape.io/github/linkdd/link.dbrequests/master/landscape.svg?style=flat-square
   :target: https://landscape.io/github/linkdd/link.dbrequests/master
   :alt: Code Health

.. image:: https://www.quantifiedcode.com/api/v1/project/d2ac1cf45f6f4cdeb938f34fcb2f2214/badge.svg
  :target: https://www.quantifiedcode.com/app/project/d2ac1cf45f6f4cdeb938f34fcb2f2214
  :alt: Code issues

Installation
------------

.. code-block:: text

   pip install link.dbrequests

Features
--------

 * database agnostic
 * lazy query resolving
 * cached queries
 * queries are unique

Exapmle
-------

.. code-block:: python

   from link.middleware.core import Middleware

   from link.dbrequest.comparison import C
   from link.dbrequest.expression import E, F

   # Will open a QueryManager using a MongoDB backend
   manager = Middleware.get_middleware_by_uri('query+mongo://localhost:27107/mydatabase/mycollection')
   # Will open a QueryManager using a SQLAlchemy backend
   manager = Middleware.get_middleware_by_uri('query+sql://localhost:5432/mydatabase/mytable')

   q1 = manager.all()

   # all documents with foo = bar
   q2 = q1.filter(C('foo') == 'bar')
   # all documents without a field named bar
   q3 = q2.exclude(~C('bar'))
   # all documents with "weight > 5" and "prop1 < prop2 * 5"
   q4 = q3.filter((C('weight') > 5) & (C('prop1') < (E('prop2') * 5)))

   # execute query
   result = list(q4)
   # get cached query
   result = list(q4)

   # create a new document:
   doc = manager.create(
      A('foo', 'bar'),
      A('weight', 5),
      A('prop1', E('weight') * 5)
   )

   # update documents:
   docs = q2.update(A('prop3', E('prop1') + E('prop2')))

   # delete documents
   q3.delete()

   doc.save()
