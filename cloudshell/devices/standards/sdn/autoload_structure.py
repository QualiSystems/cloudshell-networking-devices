from cloudshell.devices.standards.base import AbstractResource
from cloudshell.devices.standards.validators import attr_length_validator

AVAILABLE_SHELL_TYPES = ["CS_SDNController"]


class SDNControllerResource(AbstractResource):
    RESOURCE_MODEL = "SDN Controller"
    RELATIVE_PATH_TEMPLATE = ""

    def __init__(self, shell_name, name, unique_id, shell_type="CS_SDNController"):
        super(SDNControllerResource, self).__init__(shell_name, name, unique_id)

        if shell_name:
            self.shell_name = "{}.".format(shell_name)
            if shell_type in AVAILABLE_SHELL_TYPES:
                self.shell_type = "{}.".format(shell_type)
            else:
                raise Exception(self.__class__.__name__, "Unavailable shell type {shell_type}."
                                                         "Shell type should be one of: {avail}"
                                .format(shell_type=shell_type, avail=", ".join(AVAILABLE_SHELL_TYPES)))
        else:
            self.shell_name = ""
            self.shell_type = ""

    def _parse_ports(self, ports):
        """Parse ports string into the list

        :param str ports:
        :rtype: list[tuple[str, str]]
        """
        if not ports:
            return []

        return [tuple(port_pair.split("::")) for port_pair in ports.strip(";").split(";")]

    @property
    def user(self):
        """SDN Controller user

        :rtype: str
        """
        return self.attributes.get("{}User".format(self.shell_type), None)

    @user.setter
    @attr_length_validator
    def user(self, value):
        """Set SDN Controller user"""
        self.attributes["{}User".format(self.shell_type)] = value

    @property
    def password(self):
        """SDN Controller password

        :rtype: str
        """
        return self.attributes.get("{}Password".format(self.shell_type), None)

    @password.setter
    @attr_length_validator
    def password(self, value):
        """Set SDN Controller password"""
        self.attributes["{}Password".format(self.shell_type)] = value

    @property
    def port(self):
        """SDN Controller port

        :rtype: str
        """
        return self.attributes.get("{}Controller TCP Port".format(self.shell_type), None)

    @port.setter
    @attr_length_validator
    def port(self, value):
        """Set SDN Controller port"""
        self.attributes["{}Controller TCP Port".format(self.shell_type)] = value

    @property
    def scheme(self):
        """SDN Controller scheme

        :rtype: str
        """
        return self.attributes.get("{}Scheme".format(self.shell_type), None)

    @scheme.setter
    @attr_length_validator
    def scheme(self, value):
        """Set SDN Controller scheme"""
        self.attributes["{}Scheme".format(self.shell_type)] = value

    @property
    def add_trunk_ports(self):
        """SDN Controller enable trunk ports

        :rtype: list[tuple[str, str]]
        """
        ports = self.attributes.get("{}Enable Full Trunk Ports".format(self.shell_type), None)
        return self._parse_ports(ports=ports)

    @add_trunk_ports.setter
    @attr_length_validator
    def add_trunk_ports(self, value):
        """Set SDN Controller enable trunk ports"""
        self.attributes["{}Enable Full Trunk Ports".format(self.shell_type)] = value

    @property
    def remove_trunk_ports(self):
        """SDN Controller disable trunk ports

        :rtype: list[tuple[str, str]]
        """
        ports = self.attributes.get("{}Disable Full Trunk Ports".format(self.shell_type), None)
        return self._parse_ports(ports=ports)

    @remove_trunk_ports.setter
    @attr_length_validator
    def remove_trunk_ports(self, value):
        """Set SDN Controller disable trunk ports"""
        self.attributes["{}Disable Full Trunk Ports".format(self.shell_type)] = value

    @property
    def model_name(self):
        """SDN Controller model name

        :rtype: str
        """
        return self.attributes.get("{}Model Name".format(self.shell_type), None)

    @model_name.setter
    @attr_length_validator
    def model_name(self, value):
        """Set SDN Controller model name"""
        self.attributes["{}Model Name".format(self.shell_type)] = value

    @classmethod
    def from_context(cls, context, shell_name=None):
        """Create an instance of SDN Resource from the given context

        :param cloudshell.shell.core.driver_context.ResourceCommandContext context:
        :param str shell_name: shell Name
        :rtype: GenericSDNResource
        """
        result = cls(address=context.resource.address,
                     shell_name=shell_name,
                     name=context.resource.name)

        result.attributes = context.resource.attributes.copy()
        return result


class GenericSDNSwitch(AbstractResource):
    RESOURCE_MODEL = "Generic SDN Switch"
    RELATIVE_PATH_TEMPLATE = "OF"

    @property
    def model_name(self):
        """SDN Switch model name

        :rtype: str
        """
        return self.attributes.get("{}Model Name".format(self.namespace), None)

    @model_name.setter
    @attr_length_validator
    def model_name(self, value):
        """Set SDN Switch model name"""
        self.attributes["{}Model Name".format(self.namespace)] = value


class GenericSDNPort(AbstractResource):
    RESOURCE_MODEL = "Generic SDN Port"
    RELATIVE_PATH_TEMPLATE = "P"

    @property
    def mac_address(self):
        """

        :rtype: str
        """
        return self.attributes.get("{}MAC Address".format(self.namespace), None)

    @mac_address.setter
    @attr_length_validator
    def mac_address(self, value=""):
        """

        :type value: str
        """
        self.attributes["{}MAC Address".format(self.namespace)] = value

    @property
    def ipv4_address(self):
        """

        :rtype: str
        """
        return self.attributes.get("{}IPv4 Address".format(self.namespace), None)

    @ipv4_address.setter
    @attr_length_validator
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
    @attr_length_validator
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
    @attr_length_validator
    def port_description(self, value):
        """The description of the port as configured in the device.

        :type value: str
        """
        self.attributes["{}Port Description".format(self.namespace)] = value

    @property
    def adjacent(self):
        """

        :rtype: str
        """
        return self.attributes.get("{}Adjacent".format(self.namespace), None)

    @adjacent.setter
    @attr_length_validator
    def adjacent(self, value):
        """The adjacent device (system name) and port, based on LLDP or CDP protocol

        :type value: str
        """
        self.attributes["{}Adjacent".format(self.namespace)] = value
