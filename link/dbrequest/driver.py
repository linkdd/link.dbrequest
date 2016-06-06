# -*- coding: utf-8 -*-

from b3j0f.conf import Configurable, category
from link.middleware.core import Middleware
from link.dbrequest import CONF_BASE_PATH


@Configurable(
    paths='{0}/driver.conf'.format(CONF_BASE_PATH),
    conf=category('DRIVER')
)
class Driver(Middleware):

    __protocols__ = ['storage']

    def _find(self, conn, ast):
        raise NotImplementedError()

    def find_elements(self, ast):
        return self._find(self.conn, ast)

    def _insert(self, conn, ast):
        raise NotImplementedError()

    def put_element(self, ast):
        return self._insert(self.conn, ast)

    def _update(self, conn, ast):
        raise NotImplementedError()

    def update_elements(self, ast):
        return self._update(self.conn, ast)

    def _delete(self, conn, ast):
        raise NotImplementedError()

    def remove_elements(self, ast):
        return self._delete(self.conn, ast)
