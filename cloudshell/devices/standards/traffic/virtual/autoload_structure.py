from cloudshell.devices.standards.base import AbstractResource, ResourceAttr, BaseResource


class Chassis(BaseResource):
    RESOURCE_MODEL = "VirtualTrafficGeneratorChassis"
    RELATIVE_PATH_TEMPLATE = "CH"
    AVAILABLE_CS_FAMILY_TYPES = [
        "CS_VirtualTrafficGeneratorChassis", "CS_VirtualTrafficGeneratorPort"]
    CS_FAMILY_TYPE = 'CS_VirtualTrafficGeneratorChassis'


class Module(AbstractResource):
    RESOURCE_MODEL = "Virtual Traffic Generator Module"
    RELATIVE_PATH_TEMPLATE = "M"
    CS_FAMILY_TYPE = 'CS_VirtualTrafficGeneratorModule'

    device_model = ResourceAttr(ResourceAttr.LVL.NAMESPACE, 'Model')


class Port(BaseResource):
    RESOURCE_MODEL = "VirtualTrafficGeneratorPort"
    RELATIVE_PATH_TEMPLATE = "P"
    AVAILABLE_CS_FAMILY_TYPES = [
        "CS_VirtualTrafficGeneratorChassis", "CS_VirtualTrafficGeneratorPort"]
    CS_FAMILY_TYPE = 'CS_VirtualTrafficGeneratorPort'

    logical_name = ResourceAttr(ResourceAttr.LVL.CS_FAMILY_TYPE, 'Logical Name')
    mac_address = ResourceAttr(ResourceAttr.LVL.CS_FAMILY_TYPE, 'MAC Address')
    requested_vnic_name = ResourceAttr(ResourceAttr.LVL.CS_FAMILY_TYPE, 'Requested vNIC Name')
