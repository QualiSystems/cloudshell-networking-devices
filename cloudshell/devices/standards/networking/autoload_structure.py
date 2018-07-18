#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.devices.standards.base import ResourceAttribute, GenericChassis, GenericModule, \
    GenericPowerPort, GenericPortChannel, BasePhysicalResource
from cloudshell.devices.standards.base import BaseGenericNetworkPort as GenericPort


__all__ = ["GenericResource", "GenericChassis",
           "GenericModule", "GenericSubModule",
           "GenericPortChannel", "GenericPowerPort", "GenericPort"]


class GenericResource(BasePhysicalResource):
    AVAILABLE_SHELL_TYPES = ['CS_Switch', 'CS_Router', 'CS_WirelessController']

    model_name = ResourceAttribute('shell_type', 'Model Name')

    def __init__(self, shell_name, name, unique_id, shell_type='CS_Switch'):
        super(GenericResource, self).__init__(shell_name, name, unique_id, shell_type)


class GenericSubModule(GenericModule):
    RESOURCE_MODEL = "Generic Sub Module"
    RELATIVE_PATH_TEMPLATE = "SM"
