from cloudshell.devices.standards.base import AbstractResource, ResourceAttribute, BaseGenericPort,\
    BaseResource


class SDNControllerResource(BaseResource):
    RESOURCE_MODEL = "SDN Controller"
    RELATIVE_PATH_TEMPLATE = ""
    AVAILABLE_SHELL_TYPES = ["CS_SDNController"]

    model_name = ResourceAttribute('shell_type', 'Model Name')


class GenericSDNSwitch(AbstractResource):
    RESOURCE_MODEL = "GenericSDNSwitch"
    RELATIVE_PATH_TEMPLATE = "OF"

    model_name = ResourceAttribute('namespace', 'Model Name')


class GenericSDNPort(BaseGenericPort):
    RESOURCE_MODEL = "Generic SDN Port"
