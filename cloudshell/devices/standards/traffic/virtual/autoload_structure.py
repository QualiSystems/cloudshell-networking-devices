from cloudshell.devices.standards.base import AbstractResource, ResourceAttribute, BaseResource


class Chassis(BaseResource):
    RESOURCE_MODEL = "Virtual Traffic Generator Chassis"
    RELATIVE_PATH_TEMPLATE = "CH"
    AVAILABLE_SHELL_TYPES = ["CS_VirtualTrafficGeneratorChassis", "CS_VirtualTrafficGeneratorPort"]


class Module(AbstractResource):
    RESOURCE_MODEL = "VirtualTrafficGeneratorModule"
    RELATIVE_PATH_TEMPLATE = "M"

    device_model = ResourceAttribute('namespace', 'Model')


class Port(BaseResource):
    RESOURCE_MODEL = "Virtual Traffic Generator Port"
    RELATIVE_PATH_TEMPLATE = "P"
    AVAILABLE_SHELL_TYPES = ["CS_VirtualTrafficGeneratorChassis", "CS_VirtualTrafficGeneratorPort"]

    logical_name = ResourceAttribute('shell_type', 'Logical Name')
    mac_address = ResourceAttribute('shell_type', 'MAC Address')
    requested_vnic_name = ResourceAttribute('shell_type', 'Requested vNIC Name')
