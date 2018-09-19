#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.devices.standards.base import GenericChassis, GenericModule, GenericSubModule,\
    GenericPowerPort, GenericPortChannel, BasePhysicalResource
from cloudshell.devices.standards.base import BaseGenericNetworkPort as GenericPort


__all__ = ['GenericResource', 'GenericChassis', 'GenericModule', 'GenericSubModule',
           'GenericPortChannel', 'GenericPowerPort', 'GenericPort']


class GenericResource(BasePhysicalResource):
    AVAILABLE_CS_FAMILY_TYPES = ['CS_Firewall']
    CS_FAMILY_TYPE = 'CS_Firewall'
