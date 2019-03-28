def parse_configuration(str_path_file_config):
    """
    Parses configuration file.

    Configuration file format (You can see example in ./default.json):

        {
          "audio_file_format": "<value>",                   - generated audio file format
          "audio_file_player": {                            - system program what can play generated audio.
            "name": "<value>",                              - name of program
            "command": "<value>"                            - command that will be used to play audio file.
                                                                Mark place were audio file should be passed as "{file}"
          },,
          "tts_engines": {                                  - TTS engines description.
                                                                There are 2 options (at least 1 must be provided):
                                                                    cloud - requires Internet access.
                                                                    onboard - requires pre-installation. No need of Internet access.
            "cloud": {                                      - description of cloud TTS.
              "priority" : <int_value>                      - priority number of synthesis method. Bigger value - more preferable to use.
              "<engine_name>": {                            - name of service.
                "call_params": {                            - engine call parameters
                  "<field_1>": <value_1>,                   - field name and value required to work of service.
                  "<field_2>": <value_2>,
                  ...
                  "<filed_n>": <value_n>
                },
                "network": {                                - network check parameters
                  "test_ping_destination": "<value>",       - destination to ping to check access to resource
                  "test_download_destination": "<value>"    - destination to download to check download speed
                }
              }
            },
            "onboard": {                                    - description of onboard TTS.
              "priority" : <int_value>                      - priority number of synthesis method. Bigger value - more preferable to use.
              "<engine_name>": {                            - name of service.
                "call_params": {                            - engine call params
                  "<field_1>": <value_1>,                   - field name and value required to work of service.
                  "<field_2>": <value_2>,
                  ...
                  "<filed_n>": <value_n>
                }
              }
            }
          }
        }

    * Path to config file must be validated beforehand.

    :param str_path_file_config: string path to configuration file.
    :return: dict - parsed configuration.
    """
    import json

    file_config = open(str_path_file_config, 'r')
    dict_config_tts = json.load(file_config)
    file_config.close()

    return dict_config_tts
