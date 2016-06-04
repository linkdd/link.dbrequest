# -*- coding: utf-8 -*-

from b3j0f.conf import Configurable, category

from link.middleware.core import Middleware
from link.dbrequest import CONF_BASE_PATH
from link.dbrequest.tree import Node, Value
from link.dbrequest.comparison import C
from link.dbrequest.ast import AST

from copy import deepcopy


@Configurable(
    paths='{0}/manager.conf'.format(CONF_BASE_PATH),
    conf=category('QUERY')
)
class QueryManager(Middleware):

    __protocols__ = ['query']

    def __init__(self, backend, *args, **kwargs):
        super(QueryManager, self).__init__(*args, **kwargs)

        if not isinstance(backend, Middleware):
            raise TypeError('Provided backend is not a middleware')

        self.backend = backend

    def all(self):
        return _Query(self)

    def get(self, condition):
        if not isinstance(condition, C):
            raise TypeError(
                'Supplied condition is not supported: {0}'.format(
                    type(condition)
                )
            )

        return self._execute(AST('get', condition.get_ast()))

    def _execute(self, ast):
        raise NotImplementedError('TODO')


class _Query(object):
    def __init__(self, manager, *args, **kwargs):
        super(_Query, self).__init__(*args, **kwargs)

        self.manager = manager
        self.ast = []

    def get(self, condition):
        c = deepcopy(self)

        if not isinstance(condition, C):
            raise TypeError(
                'Supplied condition is not supported: {0}'.format(
                    type(condition)
                )
            )

        c.ast.append(AST('get', condition.get_ast()))

        return self.manager._execute(c.ast)

    def filter(self, condition):
        c = deepcopy(self)

        if not isinstance(condition, C):
            raise TypeError(
                'Supplied condition is not supported: {0}'.format(
                    type(condition)
                )
            )

        c.ast.append(AST('filter', condition.get_ast()))

        return c

    def exclude(self, condition):
        c = deepcopy(self)

        if not isinstance(condition, C):
            raise TypeError(
                'Supplied condition is not supported: {0}'.format(
                    type(condition)
                )
            )

        c.ast.append(AST('exclude', condition.get_ast()))

        return c

    def __getitem__(self, s):
        c = deepcopy(self)

        if not isinstance(s, slice):
            s = slice(s)

        c.ast.append(AST('slice', s))

        return c

    def __iter__(self):
        result = self.manager._execute(self.ast)

        return iter(result)

    def update(self, **fields):
        c = deepcopy(self)

        update_fields = {}

        for propname, field in fields.items():
            propname = propname.replace('__', '.')

            if not isinstance(field, Node):
                field = Value(field)

            update_fields[propname] = field.get_ast()

        c.ast.append(AST('update', update_fields))

        return self.manager._execute(c.ast)
