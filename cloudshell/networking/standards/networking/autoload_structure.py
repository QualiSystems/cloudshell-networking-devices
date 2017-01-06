#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import defaultdict

AVAILABLE_SHELL_TYPES = ["CS_Switch",
                         "CS_Router",
                         "CS_Controller"]

__all__ = ["GenericResource", "GenericChassis",
           "GenericModule", "GenericSubModule",
           "GenericPortChannel", "GenericPowerPort", "GenericPort"]


class AbstractResource(object):
    RESOURCE_MODEL = ""
    RELATIVE_PATH_TEMPLATE = ""

    def __init__(self, shell_name, name, unique_id):
        """  """

        self._name = name
        self.shell_name = shell_name
        if self.shell_name:
            self.namespace = "{shell_name}.{resource_model}.".format(shell_name=self.shell_name,
                                                                     resource_model=self.RESOURCE_MODEL)
        else:
            self.namespace = ""
        self._cloudshell_model_name = "{shell_name}.{shell_model_name}".format(shell_name=self.shell_name,
                                                                               shell_model_name=self.__class__.__name__)
        self.unique_id = unique_id
        self.attributes = {}
        self.resources = {}

    def add_sub_resource(self, relative_id, sub_resource):
        """ Add sub resource """

        existing_sub_resources = self.resources.get(sub_resource.RELATIVE_PATH_TEMPLATE, defaultdict(list))
        existing_sub_resources[relative_id].append(sub_resource)
        self.resources.update({sub_resource.RELATIVE_PATH_TEMPLATE: existing_sub_resources})

    @property
    def cloudshell_model_name(self):
        """ Return the name of the CloudShell model """

        return self.RESOURCE_MODEL

    @property
    def name(self):
        """ Return resource name """

        return self._name

    @name.setter
    def name(self, value):
        """ Set resource name """

        self._name = value

    @property
    def unique_identifier(self):
        """ Return resource uniq identifier """

        return self.unique_id

    @unique_identifier.setter
    def unique_identifier(self, value):
        """ Set resource uniq identifier """

        self.unique_id = value


class GenericResource(AbstractResource):
    RESOURCE_MODEL = ""
    RELATIVE_PATH_TEMPLATE = ""

    def __init__(self, shell_name, name, unique_id, shell_type="CS_Switch"):
        super(GenericResource, self).__init__(shell_name, name, unique_id)
        if shell_type in AVAILABLE_SHELL_TYPES:
            self.shell_type = shell_type
        else:
            raise Exception(self.__class__.__name__, "Unavailable shell type {shell_type}."
                                                     "Shell type should be one of: {avail}"
                            .format(shell_type=shell_type, avail=", ".join(AVAILABLE_SHELL_TYPES)))

    @property
    def contact_name(self):
        """ Return the name of a contact registered in the device """

        return self.attributes.get("{}.Contact Name".format(self.shell_name), None)

    @contact_name.setter
    def contact_name(self, value):
        """ Set the name of a contact registered in the device """

        self.attributes["{}.Contact Name".format(self.shell_name)] = value

    @property
    def os_version(self):
        """ Return version of the Operating System """

        return self.attributes.get("{}.OS Version".format(self.shell_type), None)

    @os_version.setter
    def os_version(self, value):
        """ Set version of the Operating System """

        self.attributes["{}.OS Version".format(self.shell_type)] = value

    @property
    def system_name(self):
        """ Set device system name """

        return self.attributes.get("{}.System Name".format(self.shell_type), None)

    @system_name.setter
    def system_name(self, value):
        """ Set device system name """

        self.attributes["{}.System Name".format(self.shell_type)] = value

    @property
    def vendor(self):
        """ Return The name of the device manufacture """

        return self.attributes.get("{}.Vendor".format(self.shell_type), None)

    @vendor.setter
    def vendor(self, value=""):
        """ Set The name of the device manufacture """

        self.attributes["{}.Vendor".format(self.shell_type)] = value

    @property
    def location(self):
        """ The device physical location identifier. For example Lab1/Floor2/Row5/Slot4 """

        return self.attributes.get("{}.Location".format(self.shell_type), None)

    @location.setter
    def location(self, value=""):
        """ Set The device physical location identifier """

        self.attributes["{}.Location".format(self.shell_type)] = value

    @property
    def model(self):
        """ Return the device model. This information is typically used for abstract resource filtering """

        return self.attributes.get("{}.Model".format(self.shell_type), None)

    @model.setter
    def model(self, value=""):
        """ Set the device model. This information is typically used for abstract resource filtering """

        self.attributes["{}.Model".format(self.shell_type)] = value


class GenericChassis(AbstractResource):
    RESOURCE_MODEL = "GenericChassis"
    RELATIVE_PATH_TEMPLATE = "CH"

    @property
    def model(self):
        """ Return the chassis model """

        return self.attributes.get("{}Model".format(self.namespace), None)

    @model.setter
    def model(self, value=""):
        """ Set the chassis model """

        self.attributes["{}Model".format(self.namespace)] = value

    @property
    def serial_number(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}Serial Number".format(self.namespace), None)

    @serial_number.setter
    def serial_number(self, value=""):
        """

        :type value: str
        """
        self.attributes["{}Serial Number".format(self.namespace)] = value


class GenericModule(AbstractResource):
    RESOURCE_MODEL = "GenericModule"
    RELATIVE_PATH_TEMPLATE = "M"

    @property
    def model(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}Model".format(self.namespace), None)

    @model.setter
    def model(self, value=""):
        """

        :type value: str
        """
        self.attributes["{}Model".format(self.namespace)] = value

    @property
    def version(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}Version".format(self.namespace), None)

    @version.setter
    def version(self, value=""):
        """

        :type value: str
        """
        self.attributes["{}Version".format(self.namespace)] = value

    @property
    def serial_number(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}Serial Number".format(self.namespace), None)

    @serial_number.setter
    def serial_number(self, value=""):
        """

        :type value: str
        """
        self.attributes["{}Serial Number".format(self.namespace)] = value


class GenericSubModule(AbstractResource):
    RESOURCE_MODEL = "GenericSubModule"
    RELATIVE_PATH_TEMPLATE = "SM"

    @property
    def model(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}Model".format(self.namespace), None)

    @model.setter
    def model(self, value=""):
        """

        :type value: str
        """
        self.attributes["{}Model".format(self.namespace)] = value

    @property
    def version(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}Version".format(self.namespace), None)

    @version.setter
    def version(self, value=""):
        """

        :type value: str
        """
        self.attributes["{}Version".format(self.namespace)] = value

    @property
    def serial_number(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}Serial Number".format(self.namespace), None)

    @serial_number.setter
    def serial_number(self, value=""):
        """

        :type value: str
        """
        self.attributes["{}Serial Number".format(self.namespace)] = value


class GenericPort(AbstractResource):
    RESOURCE_MODEL = "GenericPort"
    RELATIVE_PATH_TEMPLATE = "P"

    @property
    def mac_address(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}MAC Address".format(self.namespace), None)

    @mac_address.setter
    def mac_address(self, value=""):
        """

        :type value: str
        """
        self.attributes["{}MAC Address".format(self.namespace)] = value

    @property
    def l2_protocol_type(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}L2 Protocol Type".format(self.namespace), None)

    @l2_protocol_type.setter
    def l2_protocol_type(self, value):
        """
        Such as POS, Serial
        :type value: str
        """
        self.attributes["{}L2 Protocol Type".format(self.namespace)] = value

    @property
    def ipv4_address(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}IPv4 Address".format(self.namespace), None)

    @ipv4_address.setter
    def ipv4_address(self, value):
        """

        :type value: str
        """
        self.attributes["{}IPv4 Address".format(self.namespace)] = value

    @property
    def ipv6_address(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}IPv6 Address".format(self.namespace), None)

    @ipv6_address.setter
    def ipv6_address(self, value):
        """

        :type value: str
        """
        self.attributes["{}IPv6 Address".format(self.namespace)] = value

    @property
    def port_description(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}Port Description".format(self.namespace), None)

    @port_description.setter
    def port_description(self, value):
        """
        The description of the port as configured in the device.
        :type value: str
        """
        self.attributes["{}Port Description".format(self.namespace)] = value

    @property
    def bandwidth(self):
        """
        :rtype: float
        """
        return self.attributes.get("{}Bandwidth".format(self.namespace), None)

    @bandwidth.setter
    def bandwidth(self, value):
        """
        The current interface bandwidth, in MB.
        :type value: float
        """
        self.attributes["{}Bandwidth".format(self.namespace)] = value

    @property
    def mtu(self):
        """
        :rtype: float
        """
        return self.attributes.get("{}MTU".format(self.namespace), None)

    @mtu.setter
    def mtu(self, value):
        """
        The current MTU configured on the interface.
        :type value: float
        """
        self.attributes["{}MTU".format(self.namespace)] = value

    @property
    def duplex(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}Duplex".format(self.namespace), None)

    @duplex.setter
    def duplex(self, value):
        """
        The current duplex configuration on the interface. Possible values are Half or Full.
        :type value: str
        """
        self.attributes["{}Duplex".format(self.namespace)] = value

    @property
    def adjacent(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}Adjacent".format(self.namespace), None)

    @adjacent.setter
    def adjacent(self, value):
        """
        The adjacent device (system name) and port, based on LLDP or CDP protocol.
        :type value: str
        """
        self.attributes["{}Adjacent".format(self.namespace)] = value

    @property
    def protocol_type(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}Protocol Type".format(self.namespace), None)

    @protocol_type.setter
    def protocol_type(self, value="0"):
        """
        Default values is Transparent (="0")
        :type value: str
        """
        self.attributes["{}Protocol Type".format(self.namespace)] = value

    @property
    def auto_negotiation(self):
        """
        :rtype: bool
        """
        return self.attributes.get("{}Auto Negotiation".format(self.namespace), None)

    @auto_negotiation.setter
    def auto_negotiation(self, value):
        """
        The current auto negotiation configuration on the interface.
        :type value: bool
        """
        self.attributes["{}GenericPort.Auto Negotiation".format(self.namespace)] = value


class GenericPowerPort(AbstractResource):
    RESOURCE_MODEL = "GenericPowerPort"
    RELATIVE_PATH_TEMPLATE = "PP"

    @property
    def model(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}Model".format(self.namespace), None)

    @model.setter
    def model(self, value):
        """
        The device model. This information is typically used for abstract resource filtering.
        :type value: str
        """
        self.attributes["{}Model".format(self.namespace)] = value

    @property
    def serial_number(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}Serial Number".format(self.namespace), None)

    @serial_number.setter
    def serial_number(self, value):
        """

        :type value: str
        """
        self.attributes["{}Serial Number".format(self.namespace)] = value

    @property
    def version(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}Version".format(self.namespace), None)

    @version.setter
    def version(self, value):
        """
        The firmware version of the resource.
        :type value: str
        """
        self.attributes["{}Version".format(self.namespace)] = value

    @property
    def port_description(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}Port Description".format(self.namespace), None)

    @port_description.setter
    def port_description(self, value):
        """
        The description of the port as configured in the device.
        :type value: str
        """
        self.attributes["{}Port Description".format(self.namespace)] = value


class GenericPortChannel(AbstractResource):
    RESOURCE_MODEL = "GenericPortChannel"
    RELATIVE_PATH_TEMPLATE = "PC"

    @property
    def associated_ports(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}Associated Ports".format(self.namespace), None)

    @associated_ports.setter
    def associated_ports(self, value):
        """ Ports associated with this port channel.
        The value is in the format ???[portResourceName],??????, for example ???GE0-0-0-1,GE0-0-0-2???
        :type value: str
        """
        self.attributes["{}Associated Ports".format(self.namespace)] = value

    @property
    def ipv4_address(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}IPv4 Address".format(self.namespace), None)

    @ipv4_address.setter
    def ipv4_address(self, value):
        """

        :type value: str
        """
        self.attributes["{}IPv4 Address".format(self.namespace)] = value

    @property
    def ipv6_address(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}IPv6 Address".format(self.namespace), None)

    @ipv6_address.setter
    def ipv6_address(self, value):
        """

        :type value: str
        """
        self.attributes["{}IPv6 Address".format(self.namespace)] = value

    @property
    def port_description(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}Port Description".format(self.namespace), None)

    @port_description.setter
    def port_description(self, value):
        """
        The description of the port as configured in the device.
        :type value: str
        """
        self.attributes["{}Port Description".format(self.namespace)] = value

    @property
    def protocol_type(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}Protocol Type".format(self.namespace), None)

    @protocol_type.setter
    def protocol_type(self, value="0s"):
        """
        Default values is Transparent (="0")
        :type value: str
        """
        self.attributes["{}Protocol Type".format(self.namespace)] = value
