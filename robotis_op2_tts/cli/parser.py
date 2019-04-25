import os
from sys import exit
from _exceptions.cli import *
from base import LoggableInterface


class CLIParser(LoggableInterface):
    """
    CLI parser class.
        - It is responsible for CLI interaction with operator.
    """

    def __init__(self):
        super(CLIParser, self).__init__(name=self.__class__.__name__)

    def parse_arguments(self):
        """
        Parses program input arguments to dict.

        Arguments dictionary keys:
        - config - string path to configuration file.
        - text - source text to speech.
        - file - file with source text to speech.

        * argparse module is responsible for parsing input arguments.
        * All passed params will be validated.
        * With regard to passed arguments text or file will be available, not both.

        :return: dict - parsed arguments.
        """
        import argparse

        parser = argparse.ArgumentParser(description="Robotis OP2 Text-to-Speech (TTS) client. "
                                                     "To learn more visit: https://github.com/valera0798/Robotis-OP2-TTS")
        parser.add_argument('operation', type=str, choices=["play", "save"],
                            default="play",  # default choice
                            nargs='?',  # allows not to provide value, default will be used
                            help="operation to do with passed text source.")
        parser.add_argument('-t', '--text', type=str, help="text to synthesize speech.")
        parser.add_argument('-f', '--file', type=str, help="path to text file with content to synthesize speech.")
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
            bool_result = self._validate_configuration_file_path(args) and \
                          self._validate_text_source(args)
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
        import re
        from os.path import abspath

        if not args.text and not args.file:
            raise NoSourceTextException()

        if args.text and args.file:
            raise SeveralSourceTextsException()

        if args.file:
            self.logger.debug("Text file path %s" % args.file)

            # process ./input directory files
            regex_file_local = re.compile(r'(\.?[\/|\w|\.]*?\.[\w:]+)')

            if regex_file_local.match(args.file):  # if path to source text file is given
                if args.file[0] == '.':  # if source file is located in local input directory
                    args.file = args.file.replace('.', abspath('./input/'), 1)

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
