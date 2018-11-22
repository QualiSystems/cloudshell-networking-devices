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
    # PATTERN_SEPARATOR = '='

    COMMAND_PATTERN = r'^\s*(.*?)\s*({})'.format('|'.join([ERROR_MARKER, ACTION_MARKER]))

    ACTION_ERROR_PATTERN = r'(%s)\s*=\s*(\{.+?\})' % ('|'.join([ACTION_MARKER, ERROR_MARKER]))

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
        action_blocks = re.findall(self.ACTION_ERROR_PATTERN, command_block, re.IGNORECASE | re.DOTALL)
        for key, value in action_blocks:
            action_dict = self._deserialize_action(value)
            for pattern, action_error in action_dict.iteritems():
                if key.lower() == self.ERROR_MARKER:
                    command.add_error(pattern, action_error)
                elif key.lower() == self.ACTION_MARKER:
                    command.add_action(pattern, action_error)
                else:
                    raise Exception(self.__class__.__name__, 'Cannot determine key {}'.format(key))
        return command

    def _deserialize_action(self, block):
        """
        :param block: Block of Actions or errors {'pattern':'action', 'error_pattern':'error'}
        :type block: str
        :rtype: dict
        """
        result_dict = OrderedDict()
        c_block = re.sub('\{\s*[\'\"]{1}|[\'\"]{1}\}', '', block)
        for sub_block in re.split(r'[\"\']{1}\s*\,\s*[\"\']{1}', c_block):
            key, value = re.split(r'[\'\"]{1}\s*\:\s*[\'\"]{1}', sub_block)
            result_dict[key] = value
        return result_dict

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
