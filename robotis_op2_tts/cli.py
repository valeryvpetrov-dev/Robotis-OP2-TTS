import os
from sys import exit
from _exceptions.cli import *
from base import LoggableInterface


class CLI(LoggableInterface):
    """
    CLI parser class.
        - It is responsible for CLI interaction with operator.
    """
    LIST_COMMANDS = ["say", "save", "exit", "help"]

    def __init__(self):
        super(CLI, self).__init__(name=self.__class__.__name__)

    def parse_arguments(self):
        """
        Parses program input arguments to dict.

        Arguments dictionary keys:
        - config - string path to configuration file.

        * argparse module is responsible for parsing input arguments.
        * All passed params will be validated.
        * With regard to passed arguments text or file will be available, not both.

        :return: dict - parsed arguments.
        """
        import argparse

        parser = argparse.ArgumentParser(description="Robotis OP2 Text-to-Speech (TTS) client. "
                                                     "To learn more visit: https://github.com/valera0798/Robotis-OP2-TTS")
        parser.add_argument('-c', '--config', type=str, help="path to TTS configuration file.")
        args = parser.parse_args()

        try:
            if self.validate_args(args):
                return vars(args)
        except RobotisOP2TTSException as e:
            self.logger.error(msg=str(e), exc_info=True)
            exit()

    def validate_args(self, args):
        """
        Validated arguments passed through CLI.
            - Aggregates all validation functions.

        :param args: arguments passed via CLI.
        :return: bool - validation result. (True - valid, False - invalid)
        """
        try:
            bool_result = self._validate_configuration_file_path(args)
            if bool_result:
                self.logger.info("Superficial validation of arguments succeeds.")
            else:
                self.logger.info("Superficial validation of arguments fails.")
            return bool_result
        except RobotisOP2TTSException as e:
            self.logger.error(msg=str(e), exc_info=True)
            exit()

    def _validate_configuration_file_path(self, args):
        """
        Validates path to configuration file.

        * If path was not provided then default one will be used.

        :raises:
            * ConfigurationFileNotFoundException - if configuration file does not exist.
        :param args: parsed arguments.
        :return: bool - validation result. (True - valid, False - invalid).
        """
        if not args.config:
            self.logger.info("There is no passed path to configuration file. Default one will be used.")
            args.config = os.path.abspath("./config/default.json")

        self.logger.info("Configuration file path = %s" % args.config)
        if args.config:
            if os.path.isfile(args.config):
                if args.config.endswith(".json"):
                    if os.stat(args.config).st_size > 0:
                        self.logger.debug("Configuration file was found.")
                        return True
                    else:
                        raise ConfigurationFileEmptyException()
                else:
                    raise ConfigurationFileWrongFormatException(args.config.split(".")[-1])
            else:
                raise ConfigurationFileNotFoundException()
        return False

    def _validate_text_source(self, args):
        """
        Validates existence of text source.

        :raises:
            * NoSourceTextException - if there is no source text.
            * SeveralSourceTextsException - if there are several source texts.
            * SourceTextEmptyException - if text source is empty.
            * SourceTextFileNotFoundException - if source text file does not exist.
        :param args: parsed arguments.
        :return: bool - validation result. (True - valid, False - invalid).
        """
        if not args.text and not args.file:
            raise NoSourceTextException()

        if args.text and args.file:
            raise SeveralSourceTextsException()

        if args.file:
            self.logger.debug("Text file path %s" % args.file)
            if os.path.isfile(args.file):
                if os.stat(args.file).st_size > 0:
                    self.logger.debug("Text file was found.")
                else:
                    raise SourceTextEmptyException()
            else:
                raise SourceTextFileNotFoundException()

        if args.text:
            pass
        self.logger.info("Text to speech was provided.")
        return True

    def read_command(self):
        """
        Reads user command from CLI.

        :return: tuple - (string command, list of arguments related ot command).
        """
        str_input = raw_input("tts> ")
        list_input = str_input.split(" ", 1)
        str_command = str(list_input[0])
        list_args = list_input[1:]

        try:
            if self._validate_command(str_command):
                return str_command, list_args
        except RobotisOP2TTSException as e:
            self.logger.error(msg=str(e), exc_info=False)
            return None

    def _validate_command(self, str_command):
        """
        Validates input command.

        :raises:
            * InvalidCommandException - if command is not valid.
        :param str_command: user input command.
        :return: bool - True (valid), False (invalid).
        """
        bool_result = str_command in self.LIST_COMMANDS
        if bool_result:
            self.logger.debug("Input command is valid.")
            return bool_result
        else:
            self.logger.debug("Input command is not valid.")
            raise InvalidCommandException(str_command)

    def print_prompt(self):
        """
        Prints prompt message.

        :return: None (prompt will be printed).
        """
        print "Robotis OP2 Text-to-Speech (TTS) client. To learn more visit:\n" \
              "https://github.com/valera0798/Robotis-OP2-TTS" \
              "usage: <command> [arguments] \n " \
              "Available commands:\n" \
              "\thelp                     - show this help message.\n" \
              "\tsay [source string/file path]   - speaks passed text from source.\n" \
              "\tsave [source string/file path]  - saves synthesized from source text to file.\n" \
              "\texit                     - ends current session.\n"
