# -*- coding: utf-8 -*-

from b3j0f.utils.ut import UTCase
from unittest import main

from link.dbrequest.expression import E, F


class ExpressionTest(UTCase):
    def test_simple_expr(self):
        e = E('propname')
        ast = e.get_ast()

        self.assertEqual(
            ast,
            {
                'name': 'ref',
                'val': 'propname'
            }
        )

    def test_expr_math(self):
        e = E('propname') * 5
        ast = e.get_ast()

        self.assertEqual(
            ast,
            [
                {
                    'name': 'ref',
                    'val': 'propname'
                },
                {
                    'name': 'op',
                    'val': '*'
                },
                {
                    'name': 'val',
                    'val': 5
                }
            ]
        )

    def test_expr_func(self):
        e = F('funcname', E('propname'), E('propname') * 5)
        ast = e.get_ast()

        self.assertEqual(
            ast,
            {
                'name': 'func',
                'val': 'funcname',
                'args': [
                    {
                        'name': 'ref',
                        'val': 'propname'
                    },
                    [
                        {
                            'name': 'ref',
                            'val': 'propname'
                        },
                        {
                            'name': 'op',
                            'val': '*'
                        },
                        {
                            'name': 'val',
                            'val': 5
                        }
                    ]
                ]
            }
        )


if __name__ == '__main__':
    main()
