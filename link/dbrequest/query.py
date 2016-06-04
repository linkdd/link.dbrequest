# -*- coding: utf-8 -*-

from b3j0f.conf import Configurable, category

from link.middleware.core import Middleware
from link.dbrequest import CONF_BASE_PATH
from link.dbrequest.comparison import C
from link.dbrequest.ast import AST


@Configurable(
    paths='{0}/manager.conf'.format(CONF_BASE_PATH),
    conf=category('QUERY')
)
class QueryManager(Middleware):

    __protocols__ = ['query']

    def __init__(self, backend, *args, **kwargs):
        super(Query, self).__init__(*args, **kwargs)

        if not isinstance(backend, Middleware):
            raise TypeError('Provided backend is not a middleware')

        self.backend = backend

    def new(self):
        return Query(self)

    def execute(self, ast):
        raise NotImplementedError('TODO')


class Query(object):
    def __init__(self, manager, *args, **kwargs):
        super(Query, self).__init__(*args, **kwargs)

        self.manager = manager
        self.ast = []

    def all(self):
        return self

    def get(self, key):
        self.ast.append(AST('get', key))
        return self

    def filter(self, condition):
        if not isinstance(condition, C):
            raise TypeError(
                'Supplied condition is not supported: {0}'.format(
                    type(condition)
                )
            )

        self.ast.append(AST('filter', condition.get_ast()))
        return self

    def exclude(self, condition):
        if not isinstance(condition, C):
            raise TypeError(
                'Supplied condition is not supported: {0}'.format(
                    type(condition)
                )
            )

        self.ast.append(AST('exclude', condition.get_ast()))
        return self

    def limit(self, n):
        self.ast.append(AST('limit', n))
        return self

    def offset(self, n):
        self.ast.append(AST('offset', n))
        return self

    def __iter__(self):
        result = self.manager.execute(self.ast)

        return iter(result)
