import os
import re
from collections import OrderedDict


class ComplexCommand(object):
    def __init__(self, command, action_map=None, error_map=None):
        self.command = command.strip()
        self.action_map = action_map or OrderedDict()
        self.error_map = error_map or OrderedDict()

    def add_error(self, pattern, error):
        """
        :type pattern: basestring
        :type error: basestring
        """
        self.error_map[pattern.strip()] = error.strip()

    def add_action(self, pattern, action):
        """
        :type pattern: basestring
        :type action: basestring
        """
        self.action_map[pattern.strip()] = lambda session, logger: session.send_line(action, logger)

    def execute(self, cli_service, logger):
        """
        :type cli_service: cloudshell.cli.cli_service_impl.CliServiceImpl
        :type logger: logging.Logger
        :rtype: basestring
        """
        output = cli_service.send_command(self.command, action_map=self.action_map, error_map=self.error_map,
                                          logger=logger)
        return output + os.linesep


class CustomCommandExecutor(object):
    ERROR_MARKER = 'error_map'
    ACTION_MARKER = 'action_map'
    COMMAND_SEPARATOR = ';'
    PATTERN_SEPARATOR = ':'

    COMMAND_PATTERN = r'^\s*(.*?)\s*({})'.format('|'.join([ERROR_MARKER, ACTION_MARKER]))

    ACTION_ERROR_PATTERN = r'(%s)\s*=\s*\{(.+?)\}' % ('|'.join([ERROR_MARKER, ACTION_MARKER]))

    def __init__(self, command):
        """
        :type command: basestring
        """
        self.command = command.strip(self.COMMAND_SEPARATOR)
        self.commands = []
        self.action_map = OrderedDict()
        self.error_map = OrderedDict()
        self._process_command()

    def _process_command(self):
        """
        Prepare commands with error_map and action_map
        """
        for block in self.command.split(self.COMMAND_SEPARATOR):
            command = self._process_command_block(block.strip())
            self.commands.append(command)

    def _process_command_block(self, command_block):
        """
        :type command_block: basestring
        :rtype: ComplexCommand
        """
        command_match = re.search(self.COMMAND_PATTERN, command_block, re.IGNORECASE)
        if command_match:
            command_string = command_match.group(1)
        else:
            command_string = command_block
        command = ComplexCommand(command_string)
        for key, value in re.findall(self.ACTION_ERROR_PATTERN, command_block, re.IGNORECASE):
            pattern, action_error = re.split(self.PATTERN_SEPARATOR, value)
            if key.lower() == self.ERROR_MARKER:
                command.add_error(pattern, action_error)
            elif key.lower() == self.ACTION_MARKER:
                command.add_action(pattern, action_error)
            else:
                raise Exception(self.__class__.__name__, 'Cannot determine key {}'.format(key))
        return command

    def execute_commands(self, cli_service, logger):
        """
        :type cli_service: cloudshell.cli.cli_service_impl.CliServiceImpl
        :type logger: logging.Logger
        :rtype: basestring
        """
        output = ''
        for command in self.commands:
            output += command.execute(cli_service, logger)
        return output
