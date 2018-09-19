#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.devices.standards.base import ResourceAttr, GenericChassis, GenericModule, \
    GenericSubModule, GenericPowerPort, GenericPortChannel, BasePhysicalResource
from cloudshell.devices.standards.base import BaseGenericNetworkPort as GenericPort


__all__ = ['GenericResource', 'GenericChassis', 'GenericModule', 'GenericSubModule',
           'GenericPortChannel', 'GenericPowerPort', 'GenericPort']


class GenericResource(BasePhysicalResource):
    AVAILABLE_CS_FAMILY_TYPES = ['CS_Switch', 'CS_Router', 'CS_WirelessController']
    CS_FAMILY_TYPE = AVAILABLE_CS_FAMILY_TYPES[0]

    model_name = ResourceAttr(ResourceAttr.LVL.CS_FAMILY_TYPE, 'Model Name')
