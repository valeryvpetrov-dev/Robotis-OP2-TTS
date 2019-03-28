from base import InterfaceTTSClient


class RobotisOP2TTSClient(InterfaceTTSClient):
    """
    Robotis OP 2 Text-to-Speech (TTS) client class.
        - Behaves like InterfaceTTSClient.
    """
    _config_tts = None              # general configuration of Robotis OP2 TTS.
    _client_tts_cloud = None        # TTS cloud client
    _client_tts_onboard = None      # TTS onboard client

    def __init__(self, str_path_file_config):
        """
        Constructor of TTS client object.

        1. Initializes object;
        2. Processes passed configuration.
        3. Interacts .
        """
        super().__init__()
        self.set_configuration(str_path_file_config)

    def set_configuration(self, str_path_file_config):
        """
        Sets configuration of RobotisOP2TTSClient.

        * Configuration file will be parsed to dictionary.
        * Configuration dictionary will be validated superficially before set.
        * Corresponding TTS clients will be created as fields of RobotisOP2Client instance.
            - Actually, it is mediator to specific TTS client.

        :param str_path_file_config: path to TTS configuration file.
        :return: None (object field _config_tts will be set).
        """
        from config.parser import parse_configuration
        from tts_engines.cloud.tts_delegate import TTSCloudClientDelegate
        from tts_engines.onboard.tts_delegate import TTSOnboardClientDelegate

        dict_config_tts = parse_configuration(str_path_file_config)
        if self.validate_configuration(dict_config_tts):
            self._config_tts = dict_config_tts

            dict_engines_tts = self._config_tts['tts_engines']
            dict_config_cloud_tts = dict_engines_tts['cloud'].copy()
            dict_config_onboard_tts = dict_engines_tts['onboard'].copy()

            if dict_config_cloud_tts:
                dict_config_cloud_tts.pop('priority', None) # information about priority is not valuable for TTS client
                dict_config_cloud_tts['audio_file_format'] = self._config_tts['audio_file_format']
                dict_config_cloud_tts['audio_file_player'] = self._config_tts['audio_file_player']
                self._client_tts_cloud = TTSCloudClientDelegate(dict_config_cloud_tts)
            elif dict_config_onboard_tts:
                dict_config_onboard_tts.pop('priority', None) # information about priority is not valuable for TTS client
                dict_config_onboard_tts['audio_file_format'] = self._config_tts['audio_file_format']
                dict_config_onboard_tts['audio_file_player'] = self._config_tts['audio_file_player']
                self._client_tts_onboard = TTSOnboardClientDelegate(dict_config_onboard_tts)

    def synthesise_audio(self, source_text):
        """
        Implements corresponding method of interface parent class.
        """
        pass

    def synthesise_speech(self, source_text):
        """
        Implements corresponding method of interface parent class.
        """
        pass

    def validate_configuration(self, dict_config):
        """
        Implements corresponding method of interface parent class.

        Validates configuration superficially. TTS clients details will not be touched.
        """
        pass
