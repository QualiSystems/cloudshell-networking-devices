from cloudshell.devices.standards.base import AbstractResource, ResourceAttr, BaseGenericPort,\
    BaseResource


class SDNControllerResource(BaseResource):
    RESOURCE_MODEL = 'SDNController'
    RELATIVE_PATH_TEMPLATE = ''
    AVAILABLE_CS_FAMILY_TYPES = ['CS_SDNController']
    CS_FAMILY_TYPE = 'CS_SDNController'

    model_name = ResourceAttr(ResourceAttr.LVL.CS_FAMILY_TYPE, 'Model Name')


class GenericSDNSwitch(AbstractResource):
    RESOURCE_MODEL = 'GenericSDNSwitch'
    RELATIVE_PATH_TEMPLATE = 'OF'

    model_name = ResourceAttr(ResourceAttr.LVL.NAMESPACE, 'Model Name')


class GenericSDNPort(BaseGenericPort):
    RESOURCE_MODEL = 'GenericSDNPort'
