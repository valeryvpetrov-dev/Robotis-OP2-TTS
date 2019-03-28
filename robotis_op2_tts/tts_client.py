from base import InterfaceTTSClient
from exceptions.base import RobotisOP2TTSException
from exceptions.config import AudioFileFormatException, AudioFilePlayerException, \
            TTSEnginesPriorityNotProvidedException, TTSEnginesNotProvidedException


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

    def get_preferable_tts_client(self):
        """
        Returns TTS client with highest priority.

        :return: Implementation of InterfaceTTSClient (actually, child of AbstractTTSClientDelegate).
        """
        if self._config_tts['tts_engines']['cloud']['priority'] < \
                self._config_tts['tts_engines']['onboard']['priority']:
            return self._client_tts_cloud
        elif self._config_tts['tts_engines']['cloud']['priority'] > \
                self._config_tts['tts_engines']['onboard']['priority']:
            return self._client_tts_onboard
        else:  # for equal priorities prefer cloud method
            return self._client_tts_cloud

    def synthesise_audio(self, source_text):
        """
        Implements corresponding method of interface parent class.
        """
        self.get_preferable_tts_client().synthesise_audio(source_text)

    def synthesise_speech(self, source_text):
        """
        Implements corresponding method of interface parent class.
        """
        self.get_preferable_tts_client().synthesise_speech(source_text)

    def _validate_audio_file_format(self, str_format_file_audio):
        """
        Validates TTS configuration audio file format field.

        * Supported formats:
            - mp3, wav, ogg, gsm, dct, au, aiff, flac, vox, raw.

        ! Your audio file player must be able to play this format)

        :raises
            * AudioFileFormatException - audio_file_format field is invalid.
        :param str_format_file_audio: string-value from configuration dictionary.
        :return: bool - validation result. (True - valid, False - invalid)
        """
        LIST_AVAILABLE_AUDIO_FORMAT = ["mp3", "wav", "ogg", "gsm", "dct", "au", "aiff", "flac", "vox", "raw"]

        if str_format_file_audio in LIST_AVAILABLE_AUDIO_FORMAT:
            return True
        else:
            raise AudioFileFormatException()

    def _validate_audio_file_player(self, dict_audio_file_player_config):
        """
        Validates availability of audio player.

        * Audio player program should be pre-installed.
        * which command is used to check player installation.

        :raises
            * AudioFilePlayerException - audio player is not available.
        :param dict_audio_file_player_config: configuration of audio file player.
        :return: bool - validation result. (True - valid, False - invalid).
        """
        import subprocess

        if len(subprocess.check_output(["which", dict_audio_file_player_config["name"]])) > 0:
            return True
        else:
            raise AudioFilePlayerException()

    def _validate_tts_engines_priority(self, dict_engines_tts):
        """
        Validates presence of priority field for TTS synthesis methods (cloud/onboard).

        :param dict_engines_tts: dictionary with TTS engines descriptions.
        :return: bool - validation result. (True - valid, False - invalid).
        """
        try:
            dict_engines_tts_cloud = dict_engines_tts['cloud']
            try:
                if int(dict_engines_tts_cloud['priority']):
                    pass
            except ValueError or TypeError:  # provided priority is not a number or not provided
                return False
        except KeyError:  # if configuration for TTS synthesis method is not provided
            pass

        try:
            dict_engines_tts_onboard = dict_engines_tts['onboard']
            try:
                if int(dict_engines_tts_onboard['priority']):
                    pass
            except ValueError or TypeError:  # provided priority is not a number or not provided
                return False
        except KeyError:  # if configuration for TTS synthesis method is not provided
            pass

        return True

    def _validate_tts_engines(self, dict_engines_tts):
        """
        Validates TTS engines declared in configuration.
            - Superficial validation (does not focus on specification of particular TTS).

        * Each TTS service is responsible for self-validation.

        :raises
            * TTSEnginesPriorityNotProvidedException - TTS engine priority is not provided.
            * TTSEnginesNotProvidedException - TTS engines are not provided.
        :param dict_engines_tts: dictionary with TTS engines descriptions.
        :return: bool - validation result. (True - valid, False - invalid).
        """
        if dict_engines_tts['cloud'] or dict_engines_tts['onboard']:
            if self._validate_tts_engines_priority(dict_engines_tts):
                return True
            else:
                raise TTSEnginesPriorityNotProvidedException()
        else:
            raise TTSEnginesNotProvidedException()

    def validate_configuration(self, dict_config):
        """
        Implements corresponding method of interface parent class.

        Validates configuration superficially. TTS clients details will not be touched.
        """
        try:
            return self._validate_audio_file_format(dict_config["audio_file_format"]) and \
                   self._validate_audio_file_player(dict_config["audio_file_player"]) and \
                   self._validate_tts_engines(dict_config["tts_engines"])
        except RobotisOP2TTSException as e:
            exit(str(e))
