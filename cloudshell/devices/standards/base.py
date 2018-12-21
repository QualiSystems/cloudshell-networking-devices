from collections import defaultdict

from cloudshell.devices.standards.validators import attr_length_validator, ValidatedAttribute


class AbstractResource(object):
    RESOURCE_MODEL = ''
    RELATIVE_PATH_TEMPLATE = ''
    CS_FAMILY_TYPE = ''

    name = ValidatedAttribute()
    unique_identifier = ValidatedAttribute()

    def __init__(self, shell_name, name, unique_id, cs_family_type=CS_FAMILY_TYPE):
        """

        :param str shell_name:
        :param str name:
        :param str unique_id:
        """

        if not shell_name:
            raise DeprecationWarning('1gen Shells doesn\'t supported')

        if ' ' in self.RESOURCE_MODEL:
            raise ValueError('Resource Model must be without spaces')

        self.name = name
        self.shell_name = shell_name
        self.namespace = '{shell_name}.{resource_model}'.format(
            shell_name=self.shell_name, resource_model=self.RESOURCE_MODEL)
        self.unique_identifier = unique_id
        self.CS_FAMILY_TYPE = cs_family_type
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

        return self.namespace


class ResourceAttr(object):

    class LVL(object):
        NAMESPACE = 'namespace'
        CS_FAMILY_TYPE = 'CS_FAMILY_TYPE'

    def __init__(self, prefix_attr, name, default=None):
        self.prefix_attr = prefix_attr
        self.name = name
        self.default = default

    def get_key(self, instance):
        return '{}.{}'.format(getattr(instance, self.prefix_attr), self.name)

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return instance.attributes.get(self.get_key(instance), self.default)

    @attr_length_validator
    def __set__(self, instance, value):
        value = value if value is not None else self.default

        instance.attributes[self.get_key(instance)] = value


class BaseResource(AbstractResource):
    AVAILABLE_CS_FAMILY_TYPES = []

    def __init__(self, shell_name, name, unique_id, cs_family_type):
        super(BaseResource, self).__init__(shell_name, name, unique_id, cs_family_type)

        if cs_family_type not in self.AVAILABLE_CS_FAMILY_TYPES:
            msg = 'Unavailable CS Family Type {}. CS Family Type should be one of: {}'.format(
                    cs_family_type, ', '.join(self.AVAILABLE_CS_FAMILY_TYPES))
            raise Exception(self.__class__.__name__, msg)


class BasePhysicalResource(BaseResource):
    RESOURCE_MODEL = 'GenericResource'
    RELATIVE_PATH_TEMPLATE = ''

    contact_name = ResourceAttr(ResourceAttr.LVL.CS_FAMILY_TYPE, 'Contact Name')
    location = ResourceAttr(ResourceAttr.LVL.CS_FAMILY_TYPE, 'Location')
    model = ResourceAttr(ResourceAttr.LVL.CS_FAMILY_TYPE, 'Model')
    os_version = ResourceAttr(ResourceAttr.LVL.CS_FAMILY_TYPE, 'OS Version')
    system_name = ResourceAttr(ResourceAttr.LVL.CS_FAMILY_TYPE, 'System Name')
    vendor = ResourceAttr(ResourceAttr.LVL.CS_FAMILY_TYPE, 'Vendor')


class BaseGenericPort(AbstractResource):
    RESOURCE_MODEL = 'GenericPort'
    RELATIVE_PATH_TEMPLATE = 'P'
    CS_FAMILY_TYPE = 'CS_Port'

    adjacent = ResourceAttr(ResourceAttr.LVL.NAMESPACE, 'Adjacent')
    ipv4_address = ResourceAttr(ResourceAttr.LVL.NAMESPACE, 'IPv4 Address')
    ipv6_address = ResourceAttr(ResourceAttr.LVL.NAMESPACE, 'IPv6 Address')
    mac_address = ResourceAttr(ResourceAttr.LVL.NAMESPACE, 'MAC Address')
    port_description = ResourceAttr(ResourceAttr.LVL.NAMESPACE, 'Port Description')


class BaseGenericNetworkPort(BaseGenericPort):
    auto_negotiation = ResourceAttr(ResourceAttr.LVL.NAMESPACE, 'Auto Negotiation')
    bandwidth = ResourceAttr(ResourceAttr.LVL.NAMESPACE, 'Bandwidth', 0)
    duplex = ResourceAttr(ResourceAttr.LVL.NAMESPACE, 'Duplex', 'Half')
    l2_protocol_type = ResourceAttr(ResourceAttr.LVL.NAMESPACE, 'L2 Protocol Type')
    mtu = ResourceAttr(ResourceAttr.LVL.NAMESPACE, 'MTU', 0)


class GenericChassis(AbstractResource):
    RESOURCE_MODEL = 'GenericChassis'
    RELATIVE_PATH_TEMPLATE = 'CH'
    CS_FAMILY_TYPE = 'CS_Chassis'

    model = ResourceAttr(ResourceAttr.LVL.NAMESPACE, 'Model')
    serial_number = ResourceAttr(ResourceAttr.LVL.NAMESPACE, 'Serial Number')


class GenericModule(AbstractResource):
    RESOURCE_MODEL = 'GenericModule'
    RELATIVE_PATH_TEMPLATE = 'M'
    CS_FAMILY_TYPE = 'CS_Module'

    model = ResourceAttr(ResourceAttr.LVL.NAMESPACE, 'Model')
    serial_number = ResourceAttr(ResourceAttr.LVL.NAMESPACE, 'Serial Number')
    version = ResourceAttr(ResourceAttr.LVL.NAMESPACE, 'Version')


class GenericSubModule(GenericModule):
    RESOURCE_MODEL = 'GenericSubModule'
    RELATIVE_PATH_TEMPLATE = 'SM'
    CS_FAMILY_TYPE = 'CS_SubModule'


class GenericPowerPort(AbstractResource):
    RESOURCE_MODEL = 'GenericPowerPort'
    RELATIVE_PATH_TEMPLATE = 'PP'
    CS_FAMILY_TYPE = 'CS_PowerPort'

    model = ResourceAttr(ResourceAttr.LVL.NAMESPACE, 'Model')
    port_description = ResourceAttr(ResourceAttr.LVL.NAMESPACE, 'Port Description')
    serial_number = ResourceAttr(ResourceAttr.LVL.NAMESPACE, 'Serial Number')
    version = ResourceAttr(ResourceAttr.LVL.NAMESPACE, 'Version')


class GenericPortChannel(AbstractResource):
    RESOURCE_MODEL = 'GenericPortChannel'
    RELATIVE_PATH_TEMPLATE = 'PC'
    CS_FAMILY_TYPE = 'CS_PortChannel'

    associated_ports = ResourceAttr(ResourceAttr.LVL.NAMESPACE, 'Associated Ports')
    ipv4_address = ResourceAttr(ResourceAttr.LVL.NAMESPACE, 'IPv4 Address')
    ipv6_address = ResourceAttr(ResourceAttr.LVL.NAMESPACE, 'IPv6 Address')
    port_description = ResourceAttr(ResourceAttr.LVL.NAMESPACE, 'Port Description')
