from cloudshell.devices.standards.base_configuration_attr_structure import BaseGenericResource, \
    ROResourceAttr


class TrafficGeneratorVChassisResource(BaseGenericResource):
    user = ROResourceAttr(ROResourceAttr.LVL.NAMESPACE, 'User')
    password = ROResourceAttr(ROResourceAttr.LVL.NAMESPACE, 'Password')
    license_server = ROResourceAttr('shell_type', 'License Server')
    cli_connection_type = ROResourceAttr(ROResourceAttr.LVL.NAMESPACE, 'CLI Connection Type', 'SSH')
    cli_tcp_port = ROResourceAttr(ROResourceAttr.LVL.NAMESPACE, 'CLI TCP Port', 22)
    sessions_concurrency_limit = ROResourceAttr(
        ROResourceAttr.LVL.NAMESPACE, 'Sessions Concurrency Limit', 1)

    def __init__(self, address=None, family=None, shell_type=None, shell_name=None,
                 fullname=None, name=None, attributes=None):
        super(TrafficGeneratorVChassisResource, self).__init__(
            shell_name=shell_name, name=name, fullname=fullname, address=address, family=family,
            attributes=attributes,
        )

        self.shell_type = "{}.".format(shell_type)

    @classmethod
    def from_context(cls, shell_name, context, supported_os=None, shell_type=None):
        """Create an instance of TrafficGeneratorVBladeResource from the given context

        :param str shell_name: shell name
        :param cloudshell.shell.core.driver_context.ResourceCommandContext context:
        :param list supported_os:
        :param str shell_type: shell type
        :rtype: TrafficGeneratorVChassisResource
        """

        return cls(address=context.resource.address,
                   family=context.resource.family,
                   shell_type=shell_type,
                   shell_name=shell_name,
                   fullname=context.resource.fullname,
                   attributes=dict(context.resource.attributes),
                   name=context.resource.name)
