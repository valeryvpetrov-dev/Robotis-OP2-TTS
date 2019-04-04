import os
from sys import exit
from exceptions.cli import *
from base import LoggableInterface

logger = LoggableInterface(name=__name__).logger     # logger instance


def validate_configuration_file_path(args):
    """
    Validates path to configuration file.

    * If path was not provided then default one will be used.

    :raises:
        * ConfigurationFileNotFoundException - if configuration file does not exist.
    :param args: parsed arguments.
    :return: None (args can be modified).
    """
    if not args.config:
        logger.info("There is no passed path to configuration file. Default one will be used.")
        args.config = os.path.abspath("./config/default.json")

    logger.info("Configuration file path = {}".format(args.config))
    if args.config:
        if os.path.isfile(args.config):
            if args.config.endswith(".json"):
                if os.stat(args.config).st_size > 0:
                    logger.info("Configuration file was found.")
                else:
                    raise ConfigurationFileEmptyException()
            else:
                raise ConfigurationFileWrongFormatException(args.config.split(".")[-1])
        else:
            raise ConfigurationFileNotFoundException()


def validate_text_source(args):
    """
    Validates existence of text source.

    :raises:
        * NoSourceTextException - if there is no source text.
        * SeveralSourceTextsException - if there are several source texts.
        * SourceTextEmptyException - if text source is empty.
        * SourceTextFileNotFoundException - if source text file does not exist.
    :param args: parsed arguments.
    :return: None (args can be modified).
    """
    if not args.text and not args.file:
        raise NoSourceTextException()

    if args.text and args.file:
        raise SeveralSourceTextsException()

    if args.file:
        logger.info("Text file path = {}".format(args.file))
        if os.path.isfile(args.file):
            if os.stat(args.file).st_size > 0:
                logger.info("Text file was found.")
            else:
                raise SourceTextEmptyException()
        else:
            raise SourceTextFileNotFoundException()

    if args.text:
        pass
    logger.info("Text to speech was provided.")


def validate_operation(args):
    """
    ""
    Validates operation to do with passed text source.

    :param args: parsed arguments.
    :return: None (args can be modified).
    """
    return True


def parse_arguments():
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
                        default="play",     # default choice
                        nargs='?',          # allows not to provide value, default will be used
                        help="operation to do with passed text source.")
    parser.add_argument('-t', '--text', type=str, help="text to synthesize speech.")
    parser.add_argument('-f', '--file', type=str, help="path to text file with content to synthesize speech.")
    parser.add_argument('-c', '--config', type=str, help="path to TTS configuration file.")
    args = parser.parse_args()

    try:
        validate_text_source(args)
        validate_configuration_file_path(args)
        validate_operation(args)
    except RobotisOP2TTSException as e:
        logger.error(msg=str(e), exc_info=True)
        exit()

    return vars(args)
