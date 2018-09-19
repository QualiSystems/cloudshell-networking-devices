from cloudshell.devices.standards.base_configuration_attr_structure import BaseGenericResource


class TrafficGeneratorVBladeResource(BaseGenericResource):
    def __init__(self, address=None, family=None, shell_type=None, shell_name=None,
                 fullname=None, name=None, attributes=None):
        super(TrafficGeneratorVBladeResource, self).__init__(
            shell_name=shell_name, name=name, fullname=fullname, address=address, family=family,
            attributes=attributes,
        )

        self.shell_type = shell_type

    @classmethod
    def from_context(cls, shell_name, context, supported_os=None, shell_type=None):
        """Create an instance of TrafficGeneratorVBladeResource from the given context

        :param str shell_name: shell name
        :param cloudshell.shell.core.driver_context.ResourceCommandContext context:
        :param list supported_os:
        :param str shell_type: shell type
        :rtype: TrafficGeneratorVBladeResource
        """

        return cls(address=context.resource.address,
                   family=context.resource.family,
                   shell_type=shell_type,
                   shell_name=shell_name,
                   fullname=context.resource.fullname,
                   attributes=dict(context.resource.attributes),
                   name=context.resource.name)
