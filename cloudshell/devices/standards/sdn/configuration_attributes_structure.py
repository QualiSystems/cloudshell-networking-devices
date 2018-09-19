from cloudshell.devices.standards.base_configuration_attr_structure import BaseGenericResource, \
    ROResourceAttr


class GenericSDNResource(BaseGenericResource):
    user = ROResourceAttr(ROResourceAttr.LVL.NAMESPACE, 'User')
    password = ROResourceAttr(ROResourceAttr.LVL.NAMESPACE, 'Password')
    port = ROResourceAttr(ROResourceAttr.LVL.NAMESPACE, 'Controller TCP Port')
    scheme = ROResourceAttr(ROResourceAttr.LVL.NAMESPACE, 'Scheme')

    @staticmethod
    def _parse_ports(ports):
        """Parse ports string into the list

        :param str ports:
        :rtype: list[tuple[str, str]]
        """
        if not ports:
            return []

        return [tuple(port_pair.split("::")) for port_pair in ports.strip(";").split(";")]

    @property
    def add_trunk_ports(self):
        """SDN Controller enable trunk ports

        :rtype: list[tuple[str, str]]
        """
        ports = self.attributes.get("{}.Enable Full Trunk Ports".format(self.namespace_prefix), None)
        return self._parse_ports(ports=ports)

    @property
    def remove_trunk_ports(self):
        """SDN Controller disable trunk ports

        :rtype: list[tuple[str, str]]
        """
        ports = self.attributes.get("{}.Disable Full Trunk Ports".format(self.namespace_prefix), None)
        return self._parse_ports(ports=ports)
