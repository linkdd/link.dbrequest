# -*- coding: utf-8 -*-

from b3j0f.utils.ut import UTCase
from unittest import main

from link.dbrequest.comparison import C


class ComparisonTest(UTCase):
    def test_property_exists(self):
        c = C('prop')
        ast = c.get_ast()

        self.assertEqual(ast, ['prop', '?', True])

    def test_property_doesnt_exists(self):
        c = ~C('prop')
        ast = c.get_ast()

        self.assertEqual(ast, ['prop', '?', False])

    def test_property_less_than(self):
        c = C('i') < 5
        ast = c.get_ast()

        self.assertEqual(ast, ['i', '<', 5])

    def test_property_less_than_or_equal(self):
        c = C('i') <= 5
        ast = c.get_ast()

        self.assertEqual(ast, ['i', '<=', 5])

    def test_property_equal(self):
        c = C('foo') == 'bar'
        ast = c.get_ast()

        self.assertEqual(ast, ['foo', '==', 'bar'])

    def test_property_greater_than_or_equal(self):
        c = C('i') >= 5
        ast = c.get_ast()

        self.assertEqual(ast, ['i', '>=', 5])

    def test_property_greater_than(self):
        c = C('i') > 5
        ast = c.get_ast()

        self.assertEqual(ast, ['i', '>', 5])

    def test_property_like(self):
        c = C('foo') % r'bar.*'
        ast = c.get_ast()

        self.assertEqual(ast, ['foo', '~=', r'bar.*'])

    def test_property_and(self):
        c = (C('foo') == 'bar') & (C('bar') > 5)
        ast = c.get_ast()

        self.assertEqual(
            ast,
            [
                ['foo', '==', 'bar'],
                '&',
                ['bar', '>', 5]
            ]
        )

    def test_property_or(self):
        c = (C('foo') == 'bar') | (C('bar') > 5)
        ast = c.get_ast()

        self.assertEqual(
            ast,
            [
                ['foo', '==', 'bar'],
                '|',
                ['bar', '>', 5]
            ]
        )

    def test_property_andor(self):
        c = ((C('foo') == 'bar') & (C('bar') > 5)) | (~C('baz'))
        ast = c.get_ast()

        self.assertEqual(
            ast,
            [
                [
                    ['foo', '==', 'bar'],
                    '&',
                    ['bar', '>', 5]
                ],
                '|',
                ['baz', '?', False]
            ]
        )

    def test_wrong_combination(self):
        with self.assertRaises(TypeError):
            C('foo') & 5


if __name__ == '__main__':
    main()
