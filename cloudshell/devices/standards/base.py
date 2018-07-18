from collections import defaultdict

from cloudshell.devices.standards.validators import attr_length_validator, ValidatedAttribute


class AbstractResource(object):
    RESOURCE_MODEL = ""
    RELATIVE_PATH_TEMPLATE = ""

    name = ValidatedAttribute()
    unique_identifier = ValidatedAttribute()

    def __init__(self, shell_name, name, unique_id):
        """

        :param str shell_name:
        :param str name:
        :param str unique_id:
        """

        if not shell_name:
            raise DeprecationWarning('1gen Shells doesn\'t supported')

        self.name = name
        self.shell_name = shell_name
        self.namespace = "{shell_name}.{resource_model}.".format(
            shell_name=self.shell_name, resource_model=self.RESOURCE_MODEL.replace(" ", ""))
        self.unique_identifier = unique_id
        self.attributes = {}
        self.resources = {}

    def add_sub_resource(self, relative_id, sub_resource):
        """Add sub resource"""
        existing_sub_resources = self.resources.get(sub_resource.RELATIVE_PATH_TEMPLATE, defaultdict(list))
        existing_sub_resources[relative_id].append(sub_resource)
        self.resources.update({sub_resource.RELATIVE_PATH_TEMPLATE: existing_sub_resources})

    @property
    def cloudshell_model_name(self):
        """Return the name of the CloudShell model"""
        if self.shell_name:
            return "{shell_name}.{resource_model}".format(shell_name=self.shell_name,
                                                          resource_model=self.RESOURCE_MODEL.replace(" ", ""))
        else:
            return self.RESOURCE_MODEL


class ResourceAttribute(object):
    def __init__(self, prefix_attr, name, default=None):
        self.prefix_attr = prefix_attr
        self.name = name
        self.default = default

    def get_key(self, instance):
        return '{}{}'.format(getattr(instance, self.prefix_attr), self.name)

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return instance.attributes.get(self.get_key(instance), self.default)

    @attr_length_validator
    def __set__(self, instance, value):
        value = value if value is not None else self.default

        instance.attributes[self.get_key(instance)] = value


class BaseResource(AbstractResource):
    AVAILABLE_SHELL_TYPES = []

    def __init__(self, shell_name, name, unique_id, shell_type):
        super(BaseResource, self).__init__(shell_name, name, unique_id)

        if shell_type not in self.AVAILABLE_SHELL_TYPES:
            raise Exception(
                self.__class__.__name__,
                'Unavailable shell type {shell_type}.Shell type should be one of: {avail}'.format(
                    shell_type=shell_type, avail=', '.join(self.AVAILABLE_SHELL_TYPES)))

        self.shell_name = '{}.'.format(shell_name)
        self.shell_type = "{}.".format(shell_type)


class BasePhysicalResource(BaseResource):
    RESOURCE_MODEL = 'Generic Resource'
    RELATIVE_PATH_TEMPLATE = ''

    contact_name = ResourceAttribute('shell_type', 'Contact Name')
    location = ResourceAttribute('shell_type', 'Location')
    model = ResourceAttribute('shell_type', 'Model')
    os_version = ResourceAttribute('shell_type', 'OS Version')
    system_name = ResourceAttribute('shell_type', 'System Name')
    vendor = ResourceAttribute('shell_type', 'Vendor')


class BaseGenericPort(AbstractResource):
    RESOURCE_MODEL = 'Generic Port'
    RELATIVE_PATH_TEMPLATE = 'P'

    adjacent = ResourceAttribute('namespace', 'Adjacent')
    ipv4_address = ResourceAttribute('namespace', 'IPv4 Address')
    ipv6_address = ResourceAttribute('namespace', 'IPv6 Address')
    mac_address = ResourceAttribute('namespace', 'MAC Address')
    port_description = ResourceAttribute('namespace', 'Port Description')


class BaseGenericNetworkPort(BaseGenericPort):
    auto_negotiation = ResourceAttribute('namespace', 'Auto Negotiation')
    bandwidth = ResourceAttribute('namespace', 'Bandwidth', 0)
    duplex = ResourceAttribute('namespace', 'Duplex', 'Half')
    l2_protocol_type = ResourceAttribute('namespace', 'L2 Protocol Type')
    mtu = ResourceAttribute('namespace', 'MTU', 0)


class GenericChassis(AbstractResource):
    RESOURCE_MODEL = 'Generic Chassis'
    RELATIVE_PATH_TEMPLATE = 'CH'

    model = ResourceAttribute('namespace', 'Model')
    serial_number = ResourceAttribute('namespace', 'Serial Number')


class GenericModule(AbstractResource):
    RESOURCE_MODEL = 'Generic Module'
    RELATIVE_PATH_TEMPLATE = 'M'

    model = ResourceAttribute('namespace', 'Model')
    serial_number = ResourceAttribute('namespace', 'Serial Number')
    version = ResourceAttribute('namespace', 'Version')


class GenericPowerPort(AbstractResource):
    RESOURCE_MODEL = 'GenericPowerPort'
    RELATIVE_PATH_TEMPLATE = 'PP'

    model = ResourceAttribute('namespace', 'Model')
    port_description = ResourceAttribute('namespace', 'Port Description')
    serial_number = ResourceAttribute('namespace', 'Serial Number')
    version = ResourceAttribute('namespace', 'Version')


class GenericPortChannel(AbstractResource):
    RESOURCE_MODEL = 'Generic Port Channel'
    RELATIVE_PATH_TEMPLATE = 'PC'

    associated_ports = ResourceAttribute('namespace', 'Associated Ports')
    ipv4_address = ResourceAttribute('namespace', 'IPv4 Address')
    ipv6_address = ResourceAttribute('namespace', 'IPv6 Address')
    port_description = ResourceAttribute('namespace', 'Port Description')
