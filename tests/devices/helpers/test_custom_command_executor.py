import unittest
from collections import OrderedDict

from mock import Mock, patch, call

from cloudshell.devices.helpers.custom_command_executor import ComplexCommand, CustomCommandExecutor


class TestComplexCommand(unittest.TestCase):
    def setUp(self):
        self.logger = Mock()
        self.command = Mock()
        self.error_map = Mock()
        self.action_map = Mock()

    def _initialize_without_args(self):
        return ComplexCommand(self.command)

    def _initialize_with_args(self):
        return ComplexCommand(self.command, self.action_map, self.error_map)

    def test_init_without_error_action_map_args(self):
        instance = self._initialize_without_args()
        self.command.strip.assert_called_once()
        self.assertIsInstance(instance.error_map, OrderedDict)
        self.assertIsInstance(instance.action_map, OrderedDict)

    def test_init_with_error_action_map_args(self):
        instance = self._initialize_with_args()
        self.command.strip.assert_called_once()
        self.assertIs(instance.action_map, self.action_map)
        self.assertIs(instance.error_map, self.error_map)

    def test_add_error(self):
        instance = self._initialize_without_args()
        pattern_value = Mock()
        pattern = Mock(strip=Mock(return_value=pattern_value))
        error_value = Mock()
        error = Mock(strip=Mock(return_value=error_value))
        instance.add_error(pattern, error)
        self.assertTrue(instance.error_map.get(pattern_value) == error_value)

    def test_add_action(self):
        instance = self._initialize_without_args()
        pattern_value = Mock()
        pattern = Mock(strip=Mock(return_value=pattern_value))
        action_value = Mock()
        action = Mock(strip=Mock(return_value=action_value))
        instance.add_action(pattern, action)
        action_func = instance.action_map.get(pattern_value, None)
        self.assertIsNotNone(action_func)
        session_result = Mock()
        session = Mock(send_line=Mock(return_value=session_result))
        self.assertIs(action_func(session, self.logger), session_result)
        session.send_line.assert_called_once_with(action_value, self.logger)

    def test_execute(self):
        command_value = Mock()
        self.command.strip.return_value = command_value
        instance = self._initialize_with_args()
        result = Mock()
        cli_service = Mock(send_command=Mock(return_value=result))
        self.assertIs(instance.execute(cli_service, self.logger), result)
        cli_service.send_command.assert_called_once_with(command_value, action_map=self.action_map,
                                                         error_map=self.error_map, logger=self.logger)


class TestCustomCommandExecutor(unittest.TestCase):
    def setUp(self):
        self.block1 = Mock()
        self.block2 = Mock()
        self.command_value = Mock(split=Mock(return_value=[self.block1, self.block2]))
        self.command = Mock(strip=Mock(return_value=self.command_value))

    def _initialize_instance(self):
        return CustomCommandExecutor(self.command)

    @patch("cloudshell.devices.helpers.custom_command_executor.CustomCommandExecutor._process_command")
    def test_init(self, _process_command):
        instance = self._initialize_instance()
        self.assertIs(instance.command, self.command_value)
        self.assertIsInstance(instance.commands, list)
        _process_command.assert_called_once_with()

    @patch("cloudshell.devices.helpers.custom_command_executor.CustomCommandExecutor._process_command_block")
    def test_process_command(self, _process_command_block):
        commands = [Mock(), Mock()]
        _process_command_block.side_effect = commands
        block1_value = Mock()
        block2_value = Mock()
        self.block1.strip.return_value = block1_value
        self.block2.strip.return_value = block2_value
        instance = self._initialize_instance()
        self.command_value.split.assert_called_once_with(CustomCommandExecutor.COMMAND_SEPARATOR)
        _process_command_block.assert_has_calls([call(block1_value), call(block2_value)])
        self.assertEqual(instance.commands, commands)

    @patch("cloudshell.devices.helpers.custom_command_executor.ComplexCommand")
    @patch("cloudshell.devices.helpers.custom_command_executor.CustomCommandExecutor._process_command")
    @patch("cloudshell.devices.helpers.custom_command_executor.CustomCommandExecutor._deserialize_action")
    @patch("cloudshell.devices.helpers.custom_command_executor.re")
    def test_process_command_block_command_partial_string(self, _re, _deserialize_action, _process_command,
                                                          complex_command):
        command_block = Mock()
        command_value = Mock()
        command_match = Mock(group=Mock(return_value=command_value))
        _re.search.return_value = command_match
        instance = self._initialize_instance()
        instance._process_command_block(command_block)
        _re.search.assert_called_once_with(instance.COMMAND_PATTERN, command_block, _re.IGNORECASE)
        command_match.group.assert_called_once_with(1)
        complex_command.assert_called_once_with(command_value)

    @patch("cloudshell.devices.helpers.custom_command_executor.ComplexCommand")
    @patch("cloudshell.devices.helpers.custom_command_executor.CustomCommandExecutor._process_command")
    @patch("cloudshell.devices.helpers.custom_command_executor.CustomCommandExecutor._deserialize_action")
    @patch("cloudshell.devices.helpers.custom_command_executor.re")
    def test_process_command_block_command_whole_string(self, _re, _deserialize_action, _process_command,
                                                        complex_command):
        command_block = Mock()
        _re.search.return_value = None
        instance = self._initialize_instance()
        instance._process_command_block(command_block)
        _re.search.assert_called_once_with(instance.COMMAND_PATTERN, command_block, _re.IGNORECASE)
        complex_command.assert_called_once_with(command_block)

    @patch("cloudshell.devices.helpers.custom_command_executor.ComplexCommand")
    @patch("cloudshell.devices.helpers.custom_command_executor.CustomCommandExecutor._process_command")
    @patch("cloudshell.devices.helpers.custom_command_executor.CustomCommandExecutor._deserialize_action")
    @patch("cloudshell.devices.helpers.custom_command_executor.re")
    def test_process_command_block_error_marker(self, _re, _deserialize_action, _process_command, complex_command):
        command = Mock()
        complex_command.return_value = command
        command_block = Mock()
        key = CustomCommandExecutor.ERROR_MARKER
        value = Mock()
        _re.findall.return_value = [(key, value)]
        pattern = Mock()
        action = Mock()
        _deserialize_action.return_value = {pattern: action}
        instance = self._initialize_instance()
        self.assertIs(instance._process_command_block(command_block), command)
        _re.findall.assert_called_once_with(instance.ACTION_ERROR_PATTERN, command_block, _re.IGNORECASE | _re.DATALL)
        _deserialize_action.assert_called_once_with(value)
        command.add_error.assert_called_once_with(pattern, action)

    @patch("cloudshell.devices.helpers.custom_command_executor.ComplexCommand")
    @patch("cloudshell.devices.helpers.custom_command_executor.CustomCommandExecutor._process_command")
    @patch("cloudshell.devices.helpers.custom_command_executor.CustomCommandExecutor._deserialize_action")
    @patch("cloudshell.devices.helpers.custom_command_executor.re")
    def test_process_command_block_action_marker(self, _re, _deserialize_action, _process_command, complex_command):
        command = Mock()
        complex_command.return_value = command
        command_block = Mock()
        key = CustomCommandExecutor.ACTION_MARKER
        value = Mock()
        _re.findall.return_value = [(key, value)]
        pattern = Mock()
        action = Mock()
        _deserialize_action.return_value = {pattern: action}
        instance = self._initialize_instance()
        self.assertIs(instance._process_command_block(command_block), command)
        _re.findall.assert_called_once_with(instance.ACTION_ERROR_PATTERN, command_block, _re.IGNORECASE | _re.DATALL)
        _deserialize_action.assert_called_once_with(value)
        command.add_action.assert_called_once_with(pattern, action)

    @patch("cloudshell.devices.helpers.custom_command_executor.ComplexCommand")
    @patch("cloudshell.devices.helpers.custom_command_executor.CustomCommandExecutor._process_command")
    @patch("cloudshell.devices.helpers.custom_command_executor.CustomCommandExecutor._deserialize_action")
    @patch("cloudshell.devices.helpers.custom_command_executor.re")
    def test_process_command_block_exception(self, _re, _deserialize_action, _process_command, complex_command):
        command = Mock()
        complex_command.return_value = command
        command_block = Mock()
        key = Mock()
        value = Mock()
        _re.findall.return_value = [(key, value)]
        pattern = Mock()
        action = Mock()
        _deserialize_action.return_value = {pattern: action}
        instance = self._initialize_instance()
        with self.assertRaisesRegexp(Exception, "Cannot determine key"):
            instance._process_command_block(command_block)
        _re.findall.assert_called_once_with(instance.ACTION_ERROR_PATTERN, command_block, _re.IGNORECASE | _re.DATALL)
        _deserialize_action.assert_called_once_with(value)

    @patch("cloudshell.devices.helpers.custom_command_executor.CustomCommandExecutor._process_command")
    @patch("cloudshell.devices.helpers.custom_command_executor.re")
    def test_deserialize_action(self, _re, _process_command):
        block = Mock()
        c_block = Mock()
        sub_block = Mock()
        key = Mock()
        value = Mock()
        _re.sub.return_value = c_block
        _re.split.side_effect = [[sub_block], (key, value)]
        instance = self._initialize_instance()
        self.assertEqual(instance._deserialize_action(block), OrderedDict([(key, value)]))
        _re.sub.assert_called_once_with(r'\{\s*[\'\"]{1}|[\'\"]{1}\}', '', block)
        _re.split.assert_has_calls(
            [call(r'[\"\']{1}\s*\,\s*[\"\']{1}', c_block), call(r'[\'\"]{1}\s*\:\s*[\'\"]{1}', sub_block)])

    @patch("cloudshell.devices.helpers.custom_command_executor.CustomCommandExecutor._process_command")
    def test_execute_command(self, _process_command):
        command_otput = 'test_output'
        command = Mock(execute=Mock(return_value=command_otput))
        cli_service = Mock()
        logger = Mock()
        instance = self._initialize_instance()
        instance.commands = [command]
        self.assertEqual(instance.execute_commands(cli_service, logger), command_otput)
        command.execute.assert_called_once_with(cli_service, logger)
