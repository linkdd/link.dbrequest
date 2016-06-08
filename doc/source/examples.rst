Examples
========

Getting a backend
-----------------

.. code-block:: python

   from link.middleware.core import Middleware

   # Will open a QueryManager using a MongoDB backend
   manager = Middleware.get_middleware_by_uri('query+mongo://localhost:27107/mydatabase/mycollection')
   # Will open a QueryManager using a SQL backend
   manager = Middleware.get_middleware_by_uri('query+sql://localhost:5432/mydatabase/mytable')


Operations on the backend
-------------------------

.. code-block:: python

   from link.dbrequest.expression import E, F
   from link.dbrequest.assignment import A
   from link.dbrequest.comparison import C


   query = manager.all()  # get an iterable over all elements

   manager.create(A('foo', 'bar'))  # put document {'foo': 'bar'} into database

   doc = manager.get(C('foo') != 'bar')  # get single element, or None

Operations on queries
---------------------

.. code-block:: python

   docs = list(query)  # iterate over query to execute the request
   docs = list(query)  # use cache when iterating again

   # create a new query from the first one
   q2 = query.filter(C('foo') == 'bar')
   assert query is not q2

   # exclude documents without a field named "bar"
   q3 = q2.exclude(~C('bar'))

   # filter documents "weight > 5" and "prop1 < prop2 * 5"
   q4 = q3.filter((C('weight') > 5) & (C('prop1') < (E('prop2') * 5)))

   # set "prop3 = prop1 + prop2" on q2 result
   docs = q2.update(A('prop3', E('prop1') + E('prop2')))

   # delete documents
   q3.delete()

Operations on documents
-----------------------

.. code-block:: python

   # save/delete a single document
   doc.save()
   doc.delete()
