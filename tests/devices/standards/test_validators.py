import unittest

import mock

from cloudshell.devices.standards.validators import attr_length_validator, ValidatedAttribute


class TestValidators(unittest.TestCase):

    @mock.patch("cloudshell.devices.standards.validators.MAX_STR_ATTR_LENGTH", 2)
    def test_attr_length_validator(self):
        """Check that decorator will trim args and kwargs"""
        @attr_length_validator
        def tested_func(*args, **kwargs):
            return args, kwargs
        # act
        result = tested_func("arg", [], test_kwarg=u"kwarg", test_kwarg2={})
        # verify
        self.assertEqual(result, (("ar", []), {"test_kwarg": u"kw", "test_kwarg2": {}}))


class TestValidatedAttribute(unittest.TestCase):
    def setUp(self):
        class TestedClass(object):
            attribute = ValidatedAttribute()

        self.tested_class = TestedClass

    def test_get_descriptor_from_class(self):
        descriptor = self.tested_class.attribute
        self.assertIsInstance(descriptor, ValidatedAttribute)

    @mock.patch("cloudshell.devices.standards.validators.MAX_STR_ATTR_LENGTH", 2)
    def test_get_validated_attr(self):
        tested_instance = self.tested_class()
        tested_instance.attribute = 'arg'

        self.assertEqual(tested_instance.attribute, 'ar')
