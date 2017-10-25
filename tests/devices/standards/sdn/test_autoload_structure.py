import unittest

import mock

from cloudshell.devices.standards.sdn.autoload_structure import AVAILABLE_SHELL_TYPES
from cloudshell.devices.standards.sdn.autoload_structure import SDNControllerResource
from cloudshell.devices.standards.sdn.autoload_structure import GenericSDNSwitch
from cloudshell.devices.standards.sdn.autoload_structure import GenericSDNPort


class TestSDNControllerResource(unittest.TestCase):
    def setUp(self):
        self.shell_name = "test shell name"
        self.name = "test name"
        self.unique_id = "test unique id"
        self.shell_type = AVAILABLE_SHELL_TYPES[-1]
        self.resource = SDNControllerResource(shell_name=self.shell_name,
                                              name=self.name,
                                              unique_id=self.unique_id,
                                              shell_type=self.shell_type)

    def test_generic_resource_no_shell_name(self):
        name = "test name"
        unique_id = "test unique id"
        shell_type = ""
        resource = SDNControllerResource(shell_name="",
                                         name=name,
                                         unique_id=unique_id,
                                         shell_type=shell_type)
        self.assertEqual(resource.shell_name, "")
        self.assertEqual(resource.shell_type, "")

    def test_parse_ports(self):
        """Check that method will parse ports string into the list"""
        # act
        result = self.resource._parse_ports(ports="openflow:1::eth1;openflow:2::eth2")
        # verify
        self.assertEqual(result, [("openflow:1", "eth1"), ("openflow:2", "eth2")])

    def test_parse_ports_empty_ports(self):
        """Check that method will return an empty list if ports string is empty"""
        # act
        result = self.resource._parse_ports(ports="")
        # verify
        self.assertEqual(result, [])

    def test_user_getter(self):
        """Check that property will return needed attribute value from the internal attributes dictionary"""
        expected_val = "test value"
        self.resource.attributes = {
            "{}{}".format(self.resource.shell_type, "User"): expected_val
        }
        # act
        result = self.resource.user
        # verify
        self.assertEqual(result, expected_val)

    def test_user_setter(self):
        """Check that property setter will correctly add attribute value into the internal attributes dictionary"""
        attr_value = "test value"
        # act
        self.resource.user = attr_value
        # verify
        attr_key = "{}{}".format(self.resource.shell_type, "User")
        self.assertIn(attr_key, self.resource.attributes)
        self.assertEqual(attr_value, self.resource.attributes[attr_key])

    def test_password_setter(self):
        """Check that property setter will correctly add attribute value into the internal attributes dictionary"""
        attr_value = "test value"
        # act
        self.resource.password = attr_value
        # verify
        attr_key = "{}{}".format(self.resource.shell_type, "Password")
        self.assertIn(attr_key, self.resource.attributes)
        self.assertEqual(attr_value, self.resource.attributes[attr_key])

    def test_password_getter(self):
        """Check that property will return needed attribute value from the internal attributes dictionary"""
        expected_val = "test value"
        self.resource.attributes = {
            "{}{}".format(self.resource.shell_type, "Password"): expected_val
        }
        # act
        result = self.resource.password
        # verify
        self.assertEqual(result, expected_val)

    def test_port_setter(self):
        """Check that property setter will correctly add attribute value into the internal attributes dictionary"""
        attr_value = "test value"
        # act
        self.resource.port = attr_value
        # verify
        attr_key = "{}{}".format(self.resource.shell_type, "Controller TCP Port")
        self.assertIn(attr_key, self.resource.attributes)
        self.assertEqual(attr_value, self.resource.attributes[attr_key])

    def test_port_getter(self):
        """Check that property will return needed attribute value from the internal attributes dictionary"""
        expected_val = "test value"
        self.resource.attributes = {
            "{}{}".format(self.resource.shell_type, "Controller TCP Port"): expected_val
        }
        # act
        result = self.resource.port
        # verify
        self.assertEqual(result, expected_val)

    def test_scheme_setter(self):
        """Check that property setter will correctly add attribute value into the internal attributes dictionary"""
        attr_value = "test value"
        # act
        self.resource.scheme = attr_value
        # verify
        attr_key = "{}{}".format(self.resource.shell_type, "Scheme")
        self.assertIn(attr_key, self.resource.attributes)
        self.assertEqual(attr_value, self.resource.attributes[attr_key])

    def test_scheme_getter(self):
        """Check that property will return needed attribute value from the internal attributes dictionary"""
        expected_val = "test value"
        self.resource.attributes = {
            "{}{}".format(self.resource.shell_type, "Scheme"): expected_val
        }
        # act
        result = self.resource.scheme
        # verify
        self.assertEqual(result, expected_val)

    def test_add_trunk_ports_setter(self):
        """Check that property setter will correctly add attribute value into the internal attributes dictionary"""
        attr_value = "test value"
        # act
        self.resource.add_trunk_ports = attr_value
        # verify
        attr_key = "{}{}".format(self.resource.shell_type, "Enable Full Trunk Ports")
        self.assertIn(attr_key, self.resource.attributes)
        self.assertEqual(attr_value, self.resource.attributes[attr_key])

    def test_add_trunk_ports_getter(self):
        """Check that property will return needed attribute value from the internal attributes dictionary"""
        expected_val = "test parsed ports"
        self.resource._parse_ports = mock.MagicMock(return_value=expected_val)
        self.resource.attributes = {
            "{}{}".format(self.resource.shell_type, "Enable Full Trunk Ports"): "test ports"
        }
        # act
        result = self.resource.add_trunk_ports
        # verify
        self.assertEqual(result, expected_val)

    def test_remove_trunk_ports_setter(self):
        """Check that property setter will correctly add attribute value into the internal attributes dictionary"""
        attr_value = "test value"
        # act
        self.resource.remove_trunk_ports = attr_value
        # verify
        attr_key = "{}{}".format(self.resource.shell_type, "Disable Full Trunk Ports")
        self.assertIn(attr_key, self.resource.attributes)
        self.assertEqual(attr_value, self.resource.attributes[attr_key])

    def test_remove_trunk_ports_getter(self):
        """Check that property will return needed attribute value from the internal attributes dictionary"""
        expected_val = "test parsed ports"
        self.resource._parse_ports = mock.MagicMock(return_value=expected_val)
        self.resource.attributes = {
            "{}{}".format(self.resource.shell_type, "Disable Full Trunk Ports"): "test ports"
        }
        # act
        result = self.resource.remove_trunk_ports
        # verify
        self.assertEqual(result, expected_val)

    def test_model_name_setter(self):
        """Check that property setter will correctly add attribute value into the internal attributes dictionary"""
        attr_value = "test value"
        # act
        self.resource.model_name = attr_value
        # verify
        attr_key = "{}{}".format(self.resource.shell_type, "Model Name")
        self.assertIn(attr_key, self.resource.attributes)
        self.assertEqual(attr_value, self.resource.attributes[attr_key])

    def test_model_name_getter(self):
        """Check that property will return needed attribute value from the internal attributes dictionary"""
        expected_val = "test value"
        self.resource.attributes = {
            "{}{}".format(self.resource.shell_type, "Model Name"): expected_val
        }
        # act
        result = self.resource.model_name
        # verify
        self.assertEqual(result, expected_val)


class TestGenericSDNSwitch(unittest.TestCase):
    def setUp(self):
        self.shell_name = "test shell name"
        self.name = "test name"
        self.unique_id = "test unique id"
        self.resource = GenericSDNSwitch(shell_name=self.shell_name,
                                         name=self.name,
                                         unique_id=self.unique_id)

    def test_model_name_getter(self):
        """Check that property will return needed attribute value from the internal attributes dictionary"""
        expected_val = "test value"
        self.resource.attributes = {
            "{}{}".format(self.resource.namespace, "Model Name"): expected_val
        }
        # act
        result = self.resource.model_name
        # verify
        self.assertEqual(result, expected_val)

    def test_model_setter(self):
        """Check that property setter will correctly add attribute value into the internal attributes dictionary"""
        attr_value = "test value"
        # act
        self.resource.model_name = attr_value
        # verify
        attr_key = "{}{}".format(self.resource.namespace, "Model Name")
        self.assertIn(attr_key, self.resource.attributes)
        self.assertEqual(attr_value, self.resource.attributes[attr_key])


class TestGenericSDNPort(unittest.TestCase):
    def setUp(self):
        self.shell_name = "test shell name"
        self.name = "test name"
        self.unique_id = "test unique id"
        self.resource = GenericSDNPort(shell_name=self.shell_name,
                                       name=self.name,
                                       unique_id=self.unique_id)

    def test_mac_address_getter(self):
        """Check that property will return needed attribute value from the internal attributes dictionary"""
        expected_val = "test value"
        self.resource.attributes = {
            "{}{}".format(self.resource.namespace, "MAC Address"): expected_val
        }
        # act
        result = self.resource.mac_address
        # verify
        self.assertEqual(result, expected_val)

    def test_mac_address_setter(self):
        """Check that property setter will correctly add attribute value into the internal attributes dictionary"""
        attr_value = "test value"
        # act
        self.resource.mac_address = attr_value
        # verify
        attr_key = "{}{}".format(self.resource.namespace, "MAC Address")
        self.assertIn(attr_key, self.resource.attributes)
        self.assertEqual(attr_value, self.resource.attributes[attr_key])

    def test_ipv4_address_getter(self):
        """Check that property will return needed attribute value from the internal attributes dictionary"""
        expected_val = "test value"
        self.resource.attributes = {
            "{}{}".format(self.resource.namespace, "IPv4 Address"): expected_val
        }
        # act
        result = self.resource.ipv4_address
        # verify
        self.assertEqual(result, expected_val)

    def test_ipv4_address_setter(self):
        """Check that property setter will correctly add attribute value into the internal attributes dictionary"""
        attr_value = "test value"
        # act
        self.resource.ipv4_address = attr_value
        # verify
        attr_key = "{}{}".format(self.resource.namespace, "IPv4 Address")
        self.assertIn(attr_key, self.resource.attributes)
        self.assertEqual(attr_value, self.resource.attributes[attr_key])

    def test_ipv6_address_getter(self):
        """Check that property will return needed attribute value from the internal attributes dictionary"""
        expected_val = "test value"
        self.resource.attributes = {
            "{}{}".format(self.resource.namespace, "IPv6 Address"): expected_val
        }
        # act
        result = self.resource.ipv6_address
        # verify
        self.assertEqual(result, expected_val)

    def test_ipv6_address_setter(self):
        """Check that property setter will correctly add attribute value into the internal attributes dictionary"""
        attr_value = "test value"
        # act
        self.resource.ipv6_address = attr_value
        # verify
        attr_key = "{}{}".format(self.resource.namespace, "IPv6 Address")
        self.assertIn(attr_key, self.resource.attributes)
        self.assertEqual(attr_value, self.resource.attributes[attr_key])

    def test_port_description_getter(self):
        """Check that property will return needed attribute value from the internal attributes dictionary"""
        attr_value = "test value"
        self.resource.attributes = {
            "{}{}".format(self.resource.namespace, "Port Description"): attr_value
        }
        # act
        result = self.resource.port_description
        # verify
        self.assertEqual(result, attr_value)

    def test_port_description_setter(self):
        """Check that property setter will correctly add attribute value into the internal attributes dictionary"""
        attr_value = "test value"
        # act
        self.resource.port_description = attr_value
        # verify
        attr_key = "{}{}".format(self.resource.namespace, "Port Description")
        self.assertIn(attr_key, self.resource.attributes)
        self.assertEqual(attr_value, self.resource.attributes[attr_key])

    def test_adjacent_getter(self):
        """Check that property will return needed attribute value from the internal attributes dictionary"""
        attr_value = "test value"
        self.resource.attributes = {
            "{}{}".format(self.resource.namespace, "Adjacent"): attr_value
        }
        # act
        result = self.resource.adjacent
        # verify
        self.assertEqual(result, attr_value)

    def test_adjacent_setter(self):
        """Check that property setter will correctly add attribute value into the internal attributes dictionary"""
        attr_value = "test value"
        # act
        self.resource.adjacent = attr_value
        # verify
        attr_key = "{}{}".format(self.resource.namespace, "Adjacent")
        self.assertIn(attr_key, self.resource.attributes)
        self.assertEqual(attr_value, self.resource.attributes[attr_key])
