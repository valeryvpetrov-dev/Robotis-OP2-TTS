from base import InterfaceTTSClient, LoggableInterface
from exceptions.base import RobotisOP2TTSException
from exceptions.config import AudioFileFormatException, AudioFilePlayerException, \
            TTSEnginesNotProvidedException, \
            TTSEnginePriorityNotNumberException, TTSEnginePriorityNotProvidedException
from tts_engines.cloud.tts_delegate import TTSCloudClientDelegate
from tts_engines.onboard.tts_delegate import TTSOnboardClientDelegate


class RobotisOP2TTSClient(InterfaceTTSClient, LoggableInterface):
    """
    Robotis OP 2 Text-to-Speech (TTS) client class.
        - Behaves like InterfaceTTSClient.
        - Supports logging feature.
    """
    _config_tts = None              # general configuration of Robotis OP2 TTS.
    _client_tts_cloud = None        # TTS cloud client
    _client_tts_onboard = None      # TTS onboard client
    _client_tts_preferable = None   # preferable TTS client

    def __init__(self, str_path_file_config):
        """
        Constructor of TTS client object.

        1. Initializes object;
        2. Processes passed configuration.
        3. Interacts .
        """
        super().__init__(name=self.__class__.__name__)
        self.set_configuration(str_path_file_config)
        self.logger.info("Instance initialization succeeds.")

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

        dict_config_tts = parse_configuration(str_path_file_config)
        self.logger.debug("Configuration is parsed.")
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
            if dict_config_onboard_tts:
                dict_config_onboard_tts.pop('priority', None) # information about priority is not valuable for TTS client
                dict_config_onboard_tts['audio_file_format'] = self._config_tts['audio_file_format']
                dict_config_onboard_tts['audio_file_player'] = self._config_tts['audio_file_player']
                self._client_tts_onboard = TTSOnboardClientDelegate(dict_config_onboard_tts)
            self.logger.debug("All TTS client delegates are initialized.")

    def _get_preferable_tts_client(self):
        """
        Returns TTS client with highest priority.

        :return: Implementation of InterfaceTTSClient (actually, child of AbstractTTSClientDelegate).
        """
        if self._client_tts_preferable is None:
            if self._config_tts['tts_engines']['cloud']['priority'] < \
                    self._config_tts['tts_engines']['onboard']['priority']:
                self._client_tts_preferable = self._client_tts_cloud
            elif self._config_tts['tts_engines']['cloud']['priority'] > \
                    self._config_tts['tts_engines']['onboard']['priority']:
                self._client_tts_preferable = self._client_tts_onboard
            else:  # for equal priorities prefer cloud method
                self._client_tts_preferable = self._client_tts_cloud
        self.logger.debug("%s is chosen as preferable.", self._client_tts_preferable)
        return self._client_tts_preferable

    def _get_unpreferable_tts_client(self):
        """
        Returns TTS client opposite to client with highest priority.

        :return: Implementation of InterfaceTTSClient (actually, child of AbstractTTSClientDelegate).
        """
        if self._client_tts_preferable is None:
            self._get_preferable_tts_client()

        if isinstance(self._client_tts_preferable, TTSCloudClientDelegate):
            self.logger.debug("%s is chosen as unpreferable.", self._client_tts_onboard)
            return self._client_tts_onboard
        elif isinstance(self._client_tts_preferable, TTSOnboardClientDelegate):
            self.logger.debug("%s is chosen as unpreferable.", self._client_tts_cloud)
            return self._client_tts_cloud

    def synthesize_audio(self, source_text):
        """
        Implements corresponding method of interface parent class.
        """
        _tts_client_preferable = self._get_preferable_tts_client()
        self.logger.debug("It redirects call to %s", _tts_client_preferable)
        str_path_file_audio = _tts_client_preferable.synthesize_audio(source_text)
        if str_path_file_audio is None:      # preferable TTS has not done job
            self.logger.info("%s does not succeed audio synthesis, now it tries another TTS.",
                             self._client_tts_preferable.__class__.__name__)
            _tts_client_unpreferable = self._get_unpreferable_tts_client()
            self.logger.debug("It redirects call to %s", _tts_client_unpreferable)
            return _tts_client_unpreferable.synthesize_audio(source_text)    # ! loop
        self.logger.info("Audio synthesis succeeds. Output file path = %s", str_path_file_audio)
        return str_path_file_audio

    def synthesize_speech(self, source_text):
        """
        Implements corresponding method of interface parent class.
        """
        _tts_client_preferable = self._get_preferable_tts_client()
        self.logger.debug("It redirects call to %s", _tts_client_preferable)
        if _tts_client_preferable.synthesize_speech(source_text):
            self.logger.info("Speech synthesis succeeds. You can hear it.")
            return True
        else:       # preferable TTS has not done job
            self.logger.info("%s does not succeed speech synthesis, now it tries another TTS.",
                             self._client_tts_preferable.__class__.__name__)
            _tts_client_unpreferable = self._get_unpreferable_tts_client()
            self.logger.debug("It redirects call to %s", _tts_client_unpreferable)
            return _tts_client_unpreferable.synthesize_speech(source_text)   # ! loop

    def _validate_audio_file_format(self, str_format_file_audio):
        """
        Validates TTS configuration audio file format field.

        * Supported formats:
            - mp3.

        ! Your audio file player must be able to play this format)

        :raises
            * AudioFileFormatException - audio_file_format field is invalid.
        :param str_format_file_audio: string-value from configuration dictionary.
        :return: bool - validation result. (True - valid, False - invalid)
        """
        LIST_AVAILABLE_AUDIO_FORMAT = ["mp3"]

        if str_format_file_audio in LIST_AVAILABLE_AUDIO_FORMAT:
            self.logger.debug("%s audio file format is valid.", str_format_file_audio)
            return True
        else:
            raise AudioFileFormatException(str_format_file_audio)

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

        str_name_audio_file_player = dict_audio_file_player_config["name"]
        try:
            if len(subprocess.check_output(["which", str_name_audio_file_player])) > 0:
                self.logger.debug("%s audio file player is available.", str_name_audio_file_player)
                return True
        except subprocess.CalledProcessError as e:
            pass
        raise AudioFilePlayerException(str_name_audio_file_player)

    def _validate_tts_engines_presence(self, dict_engines_tts):
        """
        Validates presence of TTS engines.

        * It is acceptable what one TTS engine is not provided.

        :raises
            * TTSEnginesNotProvidedException - if there is no engines provided.
        :param dict_engines_tts: dictionary with TTS engines descriptions.
        :return: bool - validation result. (True - valid, False - invalid).
        """
        int_count_engines_priority_provided = 0
        for str_name_engine, dict_config in dict_engines_tts.items():
            int_count_engines_priority_provided += 1

        if int_count_engines_priority_provided == 0:
            raise TTSEnginesNotProvidedException()

        self.logger.debug("At least one TTS engine is provided.")
        return True

    def _validate_tts_engines_priority(self, dict_engines_tts):
        """
        Validates presence of priority field for TTS synthesis methods (cloud/onboard).

        :raises
            * TTSEnginePriorityNotNumberException - if priority is not a number.
            * TTSEnginePriorityNotProvidedException - if priority is not provided.
        :param dict_engines_tts: dictionary with TTS engines descriptions.
        :return: bool - validation result. (True - valid, False - invalid).
        """
        for str_name_engine, dict_config in dict_engines_tts.items():
            bool_is_value_error = False
            bool_is_key_error = False
            try:
                try:
                    if int(dict_config['priority']):
                        pass
                except ValueError or TypeError:  # provided priority is not a number or not provided
                    bool_is_value_error = True
                if bool_is_value_error:     # to ignore source error
                    raise TTSEnginePriorityNotNumberException()
            except KeyError:
                bool_is_key_error = True
            if bool_is_key_error:  # to ignore source error
                raise TTSEnginePriorityNotProvidedException()

        self.logger.debug("All TTS engines provide priority.")
        return True

    def _validate_tts_engines(self, dict_engines_tts):
        """
        Validates TTS engines declared in configuration.
            - Superficial validation (does not focus on specification of particular TTS).

        * Each TTS service is responsible for self-validation.

        :param dict_engines_tts: dictionary with TTS engines descriptions.
        :return: bool - validation result. (True - valid, False - invalid).
        """
        if self._validate_tts_engines_presence(dict_engines_tts) and \
                self._validate_tts_engines_priority(dict_engines_tts):
            return True

    def validate_configuration(self, dict_config):
        """
        Implements corresponding method of interface parent class.

        Validates configuration superficially. TTS clients details will not be touched.
        """
        try:
            bool_result = self._validate_audio_file_format(dict_config["audio_file_format"]) and \
                   self._validate_audio_file_player(dict_config["audio_file_player"]) and \
                   self._validate_tts_engines(dict_config["tts_engines"])
            if bool_result:
                self.logger.info("Superficial validation of configuration succeeds.")
            else:
                self.logger.info("Superficial validation of configuration fails.")
            return bool_result
        except RobotisOP2TTSException as e:
            self.logger.error(msg=str(e), exc_info=True)
            exit()
