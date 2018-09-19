import unittest

from cloudshell.devices.standards.base_configuration_attr_structure import ROResourceAttr


class TestROResourceAttribute(unittest.TestCase):
    def setUp(self):
        class TestedClass(object):
            attr_name = 'Test Attr Name'
            test_prefix = 'test val.'
            attribute = ROResourceAttr('test_prefix', attr_name)

            def __init__(self, attributes=None):
                self.attributes = attributes or {}

        self.tested_class = TestedClass

    def test_get_descriptor_from_class(self):
        descriptor = self.tested_class.attribute
        self.assertIsInstance(descriptor, ROResourceAttr)

    def test_get_val(self):
        expected_val = 'expected'
        key = '{}.{}'.format(self.tested_class.test_prefix, self.tested_class.attr_name)
        tested_instance = self.tested_class({key: expected_val})

        self.assertEqual(tested_instance.attribute, expected_val)
