import re
import time
from posixpath import join
from cloudshell.shell.core.interfaces.save_restore import OrchestrationSavedArtifact


class SaveConfigurationFlow(object):
    def __init__(self, cli_handler, logger, resource_name):
        self._cli_handler = cli_handler
        self._logger = logger
        self._mode = None
        self._command_actions = None
        self._resource_name = resource_name

    def execute_flow(self, folder_path, configuration_type, vrf_management_name=None):
        system_name = re.sub('\s+', '_', self._resource_name)[:23]
        time_stamp = time.strftime("%d%m%y-%H%M%S", time.localtime())
        destination_filename = '{0}-{1}-{2}'.format(system_name, configuration_type.lower(), time_stamp)

        full_path = join(folder_path, destination_filename)
        self.save_config(configuration_type=configuration_type,
                         full_path=full_path,
                         vrf_management_name=vrf_management_name)
        artifact_type = full_path.split(':')[0]
        identifier = full_path.replace("{0}:".format(artifact_type), "")
        return OrchestrationSavedArtifact(identifier=identifier, artifact_type=artifact_type)

    def save_config(self, configuration_type, full_path, vrf_management_name):
        pass



class RestoreConfigurationFlow(object):
    def __init__(self, cli_handler, logger):
        self._cli_handler = cli_handler
        self._logger = logger
        self._mode = None
        self._command_actions = None

    def execute_flow(self, path, restore_method, configuration, vrf):
        with self._cli_handler.get_session(self._cli_handler.EnableCommandMode) as session:
            if configuration == 'startup':
                if restore_method == 'override':

                    self._command_actions.override_startup(session, path, restore_method, configuration, vrf)
                else:
                    self._command_actions.copy(session, path, restore_method, configuration, vrf)
            
            if configuration == 'running':
                if restore_method == 'override':
                    self._command_actions.override_running(session, path, restore_method, configuration, vrf)
                    self._command_actions.reload(session)
                else:
                    self._command_actions.copy(session, path, restore_method, configuration, vrf)
            self._command_actions.verify_applied(session, self._logger)

    def override_startup(self):
        pass


class AddVlanFlow(object):
    def __init__(self, cli_handler, logger):
        self._cli_handler = cli_handler
        self._logger = logger
        self._mode = None
        self._command_actions = None

    def execute_flow(self, vlan_range, port_mode, port_name, qnq, c_tag):
        self._logger.info(self.__class__.__name__, 'Add Vlan configuration started')
        with self._cli_handler.get_session(self._cli_handler.enable_mode) as session:
            self._command_actions.create_vlan(session, self._logger, vlan_range, port_mode, qnq, c_tag)
            self._command_actions.set_vlan_to_interface(session, self._logger, vlan_range, port_mode, port_name, qnq, c_tag)
            self._command_actions.verify_vlan_added(session, vlan_range, port_name)
            self._logger.info(self.__class__.__name__, 'Add Vlan configuration successfully completed')
            return 'Vlan configuration successfully completed'


class RemoveVlanFlow(object):
    def __init__(self, cli_handler, logger):
        self._cli_handler = cli_handler
        self._logger = logger
        self._mode = None
        self._command_actions = None

    def execute_flow(self, vlan_range, port_mode, port_name, qnq, c_tag):
        self._logger.info(self.__class__.__name__, 'Remove Vlan configuration started')
        with self._cli_handler.get_session() as session:
            self._command_actions.remove_vlan_from_interface(session, self._logger, vlan_range, port_mode, port_name, qnq, c_tag)
            self._command_actions.verfiy(session, self._logger, vlan_range, port_name)
            self._logger.info(self.__class__.__name__, 'Remove Vlan configuration successfully completed')
            return 'Vlan configuration successfully completed'

class LoadFirmwareFlow(object):    
    def __init__(self, cli_handler, logger):
        self._cli_handler = cli_handler
        self._logger = logger
        self._mode = None
        self._command_actions = None

    def execute_flow(self, path, vrf, timeout):
        with self._cli_handler.get_session() as session:
            self._command_actions.install_firmware(session, self._logger, session, path, vrf)
            self._command_actions.reload(session, self._logger, session, timeout)
            self._command_actions.verfiy(session, self._logger, session)
            
            
class HealthCheckFlow(object):
    def __init__(self, cli_handler, logger):
        self._cli_handler = cli_handler
        self._logger = logger
        self._mode = None
        self._command_actions = None

    def execute_flow(self):
        with self._cli_handler.get_session() as session:
            self._command_actions.health_check(session)

class RunCommandFlow(object):
    def __init__(self, cli_handler, logger):
        self._cli_handler = cli_handler
        self._logger = logger
        self._mode = None
        self._command_actions = None
    
    def execute_flow(self, command):
        with self._cli_handler.get_session(self._mode) as session:
            self._command_actions.run_custom_command(session, command)
