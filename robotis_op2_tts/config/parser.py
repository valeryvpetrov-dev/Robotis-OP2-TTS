from exceptions.config import *
from sys import exit
import subprocess


LIST_AVAILABLE_AUDIO_FORMAT = ["mp3", "wav", "ogg", "gsm", "dct", "au", "aiff", "flac", "vox", "raw"]


def validate_audio_file_format(str_format_file_audio):
    """
    Validates tts configuration audio file format field.

    * Supported formats (Note! Your audio file player must be able to play this format):
        - mp3, wav, ogg, gsm, dct, au, aiff, flac, vox, raw.

    :raises
        * AudioFileFormatException - audio_file_format field is invalid.
    :param str_format_file_audio: string-value from configuration dictionary.
    :return: bool - validation result. (True - valid, False - invalid)
    """
    if str_format_file_audio in LIST_AVAILABLE_AUDIO_FORMAT:
        return True
    else:
        raise AudioFileFormatException()


def validate_audio_file_player(dict_audio_file_player_config):
    """
    Validates availability of audio player.

    * Audio player program should be pre-installed.
    * which command is used to check player installation.

    :raises
        * AudioFilePlayerException - audio player is not available.
    :param dict_audio_file_player_config: configuration of audio file player.
    :return: bool - validation result. (True - valid, False - invalid)
    """
    if len(subprocess.check_output(["which", dict_audio_file_player_config["name"]])) > 0:
        return True
    else:
        raise AudioFilePlayerException()


def validate_tts_engines(dict_engines_tts):
    """
    Validates tts engines declared in configuration.

    * Each TTS service is responsible for self-validation.

    :raises
        * TTS services specific exceptions.
        * TTSEnginesNoProvidedException - tts engines where not provided.
    :param dict_engines_tts: dictionary with tts engines descriptions.
    :return: bool - validation result. (True - valid, False - invalid)
    """
    pass    # TODO implement after tts engines implementation


def parse_configuration(str_path_file_config):
    """
    Parses configuration file.

    Configuration file format (You can see example in ./default.json):

        {
          "audio_file_format": "<value>",       - generated audio file format
          "audio_file_player": {                - system program what can play generated audio.
            "name": "<value>",                  - name of program
            "command": "<value>"                - command that will be used to play audio file.
                                                    Mark place were audio file should be passed as "{file}"
          },,
          "tts_engines": {                      - TTS engines description.
                                                    There are 2 options (at least 1 must be provided):
                                                        cloud - requires Internet access.
                                                        onboard - requires pre-installation. No need to Internet access.
            "cloud": {                          - description of cloud TTS.
              "<engine_name>": {                - name of service.
                "<field_1>": "<value_1>,        - field name and value required to work of service.
                "<field_2>": "<value_2>",
                ...
                "<filed_n>": "<value_n>"
              }
            },
            "onboard": {                        - description of onboard TTS.
              "<engine_name>": {                - name of service.
                "<field_1>": "<value_1>,        - field name and value required to work of service.
                "<field_2>": "<value_2>",
                ...
                "<filed_n>": "<value_n>"
              }
            }
          }
        }

    * Path to config file must be validated beforehand.
    * Parsed configuration dictionary will be validated. But TTS engines details will not be touched.

    :param str_path_file_config: string path to configuration file.
    :return: dict - parsed configuration.
    """
    import json

    file_config = open(str_path_file_config, 'r')
    dict_config_tts = json.load(file_config)
    file_config.close()

    try:
        if validate_audio_file_format(dict_config_tts["audio_file_format"]) and \
            validate_audio_file_player(dict_config_tts["audio_file_player"]) and \
                validate_tts_engines(dict_config_tts["tts_engines"]):
                    return dict_config_tts
    except RobotisOP2TTSException as e:
        exit(str(e))
