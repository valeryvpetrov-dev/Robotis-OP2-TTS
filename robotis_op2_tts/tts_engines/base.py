from base import InterfaceTTSClient


class AbstractTTSClient(InterfaceTTSClient):
    """
    Abstract TTS client class.
        - Declares abstract structure of TTS client.
        - Behaves like TTS client.
        - Should be used as parent of all TTS clients.
    """
    _config_tts = None               # configuration of specific TTS client
    _str_path_output_dir = None      # audio output directory
    _str_format_file_audio = None    # audio file format

    def __init__(self, dict_config):
        """
        Constructs instance of AbstractTTSClient class.

        :param dict_config: configuration of TTS client.
        """
        super().__init__()
        self.set_configuration(dict_config)

    def set_configuration(self, dict_config):
        """
        Sets configuration of client instance.

        :param dict_config: dict - configuration of TTS client.
        :return: None (fields will be initialized).
        """
        if self.validate_configuration(dict_config):
            from os import makedirs
            from os.path import abspath

            self._str_format_file_audio = dict_config['audio_file_format']      # audio file format configuration
            dict_config.pop('audio_file_format', None)                          # to not to duplicate data
            self._config_tts = dict_config

            self._str_path_output_dir = abspath(self._str_path_output_dir)  # creates audio output directory
            try:
                makedirs(self._str_path_output_dir)
            except FileExistsError:
                pass


class AbstractTTSClientDelegate(InterfaceTTSClient):
    """
    Abstract TTS client delegate class.
        - Declares abstract structure of TTS client delegates.
        - Behaves like TTS client.
        - Should be used as parent of all TTS client delegates.
    """
    _config_tts = None              # configuration of specific TTS client
    _client_tts = None              # specific TTS client
    _str_command_play_audio = None  # command to call audio player

    def __init__(self, dict_config):
        """
        Constructs instance of AbstractTTSClientDelegate class.

        :param dict_config: configuration of TTS client.
        """
        super().__init__()
        self.set_configuration(dict_config)

    def set_configuration(self, dict_config):
        """
        Sets configuration of delegate instance.
            - Sets input configuration as _config_tts field.

        * Validates passed configuration before set.

        :param dict_config: dict - configuration of TTS client.
        :return: None (fields will be initialized).
        """
        if self.validate_configuration(dict_config):
            self._str_command_play_audio = dict_config['audio_file_player']['command']
            dict_config.pop('audio_file_player')    # to not to duplicate data
            self._config_tts = dict_config
