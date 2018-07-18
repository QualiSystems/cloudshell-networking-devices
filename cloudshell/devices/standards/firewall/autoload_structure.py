#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.devices.standards.base import GenericChassis, GenericModule, GenericPowerPort, \
    GenericPortChannel, BasePhysicalResource
from cloudshell.devices.standards.base import BaseGenericNetworkPort as GenericPort


__all__ = ["GenericResource", "GenericChassis",
           "GenericModule", "GenericSubModule",
           "GenericPortChannel", "GenericPowerPort", "GenericPort"]


class GenericResource(BasePhysicalResource):
    AVAILABLE_SHELL_TYPES = ['CS_Firewall']

    def __init__(self, shell_name, name, unique_id, shell_type='CS_Firewall'):
        super(GenericResource, self).__init__(shell_name, name, unique_id, shell_type)


class GenericSubModule(GenericModule):
    RESOURCE_MODEL = "GenericSubModule"
    RELATIVE_PATH_TEMPLATE = "SM"
