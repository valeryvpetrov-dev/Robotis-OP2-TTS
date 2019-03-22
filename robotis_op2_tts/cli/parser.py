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
    pass


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
    pass


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
    pass
