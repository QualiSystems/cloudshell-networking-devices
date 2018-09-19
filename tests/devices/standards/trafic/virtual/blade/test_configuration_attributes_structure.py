import unittest

import mock

from cloudshell.devices.standards.traffic.virtual.blade.configuration_attributes_structure import \
    TrafficGeneratorVBladeResource


class TestTrafficGeneratorVBladeResource(unittest.TestCase):
    def test_create_resource_from_context(self):
        shell_name = 'test shell name'
        context = mock.MagicMock()

        result = TrafficGeneratorVBladeResource.from_context(shell_name, context)

        self.assertIsInstance(result, TrafficGeneratorVBladeResource)

    def test_no_shell_name(self):
        self.assertRaisesRegexp(
            DeprecationWarning,
            '1gen Shells doesn\'t supported',
            TrafficGeneratorVBladeResource,
            shell_name='',
        )
