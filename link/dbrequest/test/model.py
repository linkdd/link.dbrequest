# -*- coding: utf-8 -*-

from b3j0f.utils.ut import UTCase
from mock import Mock
from unittest import main

from link.dbrequest.model import Model


class ModelTest(UTCase):
    def setUp(self):
        self.driver = Mock()

        self.doc = {
            'foo': 'bar',
            'bar': 'baz'
        }
        self.model = Model(self.driver, self.doc)

    def test_model_access(self):
        self.assertEqual(self.model.data, self.doc)
        self.assertEqual(self.model.foo, self.doc['foo'])
        self.assertEqual(self.model['foo'], self.doc['foo'])

        self.model.baz = 'biz'

        self.assertEqual(self.model.baz, 'biz')
        self.assertEqual(self.model['baz'], 'biz')

        del self.model.baz

        with self.assertRaises(AttributeError):
            self.model.baz

        with self.assertRaises(KeyError):
            self.model['baz']

    def test_model_str_repr(self):
        self.assertEqual(
            str(self.model),
            '{"foo": "bar", "bar": "baz"}'
        )
        self.assertEqual(
            repr(self.model),
            'Model({"foo": "bar", "bar": "baz"})'
        )

    def test_model_get_filter(self):
        c = self.model._get_filter()
        ast = c.get_ast()

        self.assertEqual(
            ast,
            [
                [
                    {
                        'name': 'prop',
                        'val': 'foo'
                    },
                    {
                        'name': 'cond',
                        'val': '=='
                    },
                    {
                        'name': 'val',
                        'val': 'bar'
                    }
                ],
                {
                    'name': 'join',
                    'val': '&'
                },
                [
                    {
                        'name': 'prop',
                        'val': 'bar'
                    },
                    {
                        'name': 'cond',
                        'val': '=='
                    },
                    {
                        'name': 'val',
                        'val': 'baz'
                    }
                ]
            ]
        )

    def test_model_get_update(self):
        a = self.model._get_update()
        ast = [_a.get_ast() for _a in a]

        self.assertEqual(
            ast,
            [
                [
                    {
                        'name': 'prop',
                        'val': 'foo'
                    },
                    {
                        'name': 'assign',
                        'val': {
                            'name': 'val',
                            'val': 'bar'
                        }
                    }
                ],
                [
                    {
                        'name': 'prop',
                        'val': 'bar'
                    },
                    {
                        'name': 'assign',
                        'val': {
                            'name': 'val',
                            'val': 'baz'
                        }
                    }
                ]
            ]
        )

    def test_model_save(self):
        attrs = {
            'put_element.return_value': Model(self.driver, {
                '_id': 'some id',
                'foo': 'bar',
                'bar': 'baz'
            })
        }
        ast = [
            [
                {
                    'name': 'prop',
                    'val': 'foo'
                },
                {
                    'name': 'assign',
                    'val': {
                        'name': 'val',
                        'val': 'bar'
                    }
                }
            ],
            [
                {
                    'name': 'prop',
                    'val': 'bar'
                },
                {
                    'name': 'assign',
                    'val': {
                        'name': 'val',
                        'val': 'baz'
                    }
                }
            ]
        ]
        self.driver.configure_mock(**attrs)

        new_model = self.model.save()

        self.assertEqual(new_model._id, 'some id')
        self.driver.put_element.assert_called_with(ast)

    def test_model_remove(self):
        attrs = {
            'remove_elements.return_value': None
        }
        self.driver.configure_mock(**attrs)
        ast = [
            {
                'name': 'filter',
                'val': [
                    [
                        {
                            'name': 'prop',
                            'val': 'foo'
                        },
                        {
                            'name': 'cond',
                            'val': '=='
                        },
                        {
                            'name': 'val',
                            'val': 'bar'
                        }
                    ],
                    {
                        'name': 'join',
                        'val': '&'
                    },
                    [
                        {
                            'name': 'prop',
                            'val': 'bar'
                        },
                        {
                            'name': 'cond',
                            'val': '=='
                        },
                        {
                            'name': 'val',
                            'val': 'baz'
                        }
                    ]
                ]
            }
        ]

        self.model.delete()

        self.driver.remove_elements.assert_called_with(ast)


if __name__ == '__main__':
    main()
