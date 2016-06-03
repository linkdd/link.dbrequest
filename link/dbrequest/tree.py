# -*- coding: utf-8 -*-


class Node(object):
    def __init__(self, name, *args, **kwargs):
        super(Node, self).__init__(*args, **kwargs)

        self.name = name

    def get_ast(self):
        return self.name
