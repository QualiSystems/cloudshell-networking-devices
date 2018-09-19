import unittest

from cloudshell.devices.standards.traffic.virtual.autoload_structure import Chassis, Module, Port


class TestChassis(unittest.TestCase):
    def test_creating(self):
        cs_family_type = Chassis.AVAILABLE_CS_FAMILY_TYPES[-1]
        self.resource = Chassis('test shell name', 'test name', 'test uniq id', cs_family_type)

    def test_raise_exception_if_unavailable_cs_family_type(self):
        cs_family_type = 'unavailable_cs_family_type'

        self.assertRaisesRegexp(
            Exception,
            'Unavailable CS Family Type',
            Chassis,
            'test shell name',
            'test name',
            'test uniq id',
            cs_family_type,
        )

    def test_no_shell_name(self):
        shell_name = ''
        name = 'test name'
        unique_id = 'uniq id'
        cs_family_type = 'test shell type'

        self.assertRaisesRegexp(
            DeprecationWarning,
            '1gen Shells doesn\'t supported',
            Chassis,
            shell_name,
            name,
            unique_id,
            cs_family_type,
        )


class TestModule(unittest.TestCase):
    def setUp(self):
        self.shell_name = 'test shell name'
        self.name = 'test name'
        self.unique_id = 'test unique id'
        self.resource = Module(self.shell_name, self.name, self.unique_id)

    def test_model_getter(self):
        expected_val = 'test value'
        self.resource.attributes = {
            '{}.{}'.format(self.resource.namespace, 'Model'): expected_val
        }

        self.assertEqual(self.resource.device_model, expected_val)

    def test_model_setter(self):
        attr_value = 'test value'
        self.resource.device_model = attr_value
        attr_key = '{}.{}'.format(self.resource.namespace, 'Model')

        self.assertIn(attr_key, self.resource.attributes)
        self.assertEqual(attr_value, self.resource.attributes[attr_key])


class TestPort(unittest.TestCase):
    def setUp(self):
        self.shell_name = 'test shell name'
        self.name = 'test name'
        self.unique_id = 'test unique id'
        self.cs_family_type = Port.AVAILABLE_CS_FAMILY_TYPES[-1]
        self.resource = Port(self.shell_name, self.name, self.unique_id, self.cs_family_type)

    def test_logical_name_getter(self):
        expected_val = 'test value'
        self.resource.attributes = {
            '{}.{}'.format(self.resource.CS_FAMILY_TYPE, 'Logical Name'): expected_val
        }

        self.assertEqual(self.resource.logical_name, expected_val)

    def test_logical_name_setter(self):
        attr_value = 'test value'
        self.resource.logical_name = attr_value
        attr_key = '{}.{}'.format(self.resource.CS_FAMILY_TYPE, 'Logical Name')

        self.assertIn(attr_key, self.resource.attributes)
        self.assertEqual(attr_value, self.resource.attributes[attr_key])

    def test_mac_address_getter(self):
        expected_val = 'test value'
        self.resource.attributes = {
            '{}.{}'.format(self.resource.CS_FAMILY_TYPE, 'MAC Address'): expected_val
        }

        self.assertEqual(self.resource.mac_address, expected_val)

    def test_mac_address_setter(self):
        attr_value = 'test value'
        self.resource.mac_address = attr_value
        attr_key = '{}.{}'.format(self.resource.CS_FAMILY_TYPE, 'MAC Address')

        self.assertIn(attr_key, self.resource.attributes)
        self.assertEqual(attr_value, self.resource.attributes[attr_key])

    def test_requested_vnic_name_getter(self):
        expected_val = 'test value'
        self.resource.attributes = {
            '{}.{}'.format(self.resource.CS_FAMILY_TYPE, 'Requested vNIC Name'): expected_val
        }

        self.assertEqual(self.resource.requested_vnic_name, expected_val)

    def test_requested_vnic_name_setter(self):
        attr_value = 'test value'
        self.resource.requested_vnic_name = attr_value
        attr_key = '{}.{}'.format(self.resource.CS_FAMILY_TYPE, 'Requested vNIC Name')

        self.assertIn(attr_key, self.resource.attributes)
        self.assertEqual(attr_value, self.resource.attributes[attr_key])

    def test_raise_exception_if_unavailable_cs_family_type(self):
        cs_family_type = 'unavailable_cs_family_type'

        self.assertRaisesRegexp(
            Exception,
            'Unavailable CS Family Type',
            Port,
            self.shell_name,
            self.name,
            self.unique_id,
            cs_family_type,
        )

    def test_no_shell_name(self):
        shell_name = ''

        self.assertRaisesRegexp(
            DeprecationWarning,
            '1gen Shells doesn\'t supported',
            Port,
            shell_name,
            self.name,
            self.unique_id,
            self.cs_family_type,
        )
