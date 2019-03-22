import os
import sys
from exceptions.cli import *


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
        print("There is no passed path to configuration file. Default one will be used.")
        args.config = os.path.abspath("./config/default.json")

    print("Configuration file path = {}".format(args.config))
    if args.config:
        if os.path.isfile(args.config):
            print("Configuration file was found.")
        else:
            raise ConfigurationFileNotFoundException()


def validate_text_source(args):
    """
    Validates existence of text source.

    :raises:
        * NoSourceTextException - if there is no source text.
        * SeveralSourceTextsException - if there are several source texts.
        * SourceTextFileNotFoundException - if source text file does not exist.
    :param args: parsed arguments.
    :return: None (args can be modified).
    """
    if not args.text and not args.file:
        raise NoSourceTextException()

    if args.text and args.file:
        raise SeveralSourceTextsException()
    elif args.file:
        print("Text file path = {}".format(args.file))
        if os.path.isfile(args.file):
            print("Text file was found.")
        else:
            raise SourceTextFileNotFoundException()
    elif args.text:
        pass
    print("Text to speech was provided.")


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
    parser.add_argument('-t', '--text', type=str, help="text to synthesise speech.")
    parser.add_argument('-f', '--file', type=str, help="path to text file with content to synthesise speech.")
    parser.add_argument('-c', '--config', type=str, help="path to TTS configuration file.")
    args = parser.parse_args()

    try:
        validate_configuration_file_path(args)
        validate_text_source(args)
    except RobotisOP2TTSException as e:
        sys.exit(str(e))

    return vars(args)