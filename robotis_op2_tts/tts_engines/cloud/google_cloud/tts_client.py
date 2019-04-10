from tts_engines._base import AbstractTTSClient
from .._base import InterfaceTTSCloudClient
from _exceptions.tts_engines.cloud.google_cloud import *

import os

from google.cloud import texttospeech
from google.api_core.exceptions import GoogleAPICallError


class TTSGoogleCloudClient(AbstractTTSClient, InterfaceTTSCloudClient):
    """
    Google Cloud TTS client class.
        - Google Cloud TTS specification of InterfaceTTSCloudClient.
        - Has structure like AbstractTTSClient.
        - Behaves like InterfaceTTSCloudClient.
    """
    # required params to call Google Cloud TTS
    LIST_CALL_PARAMS_REQUIRED = ['language_code', 'name', 'speaking_rate', 'pitch', 'effects_profile_id']
    # required params to check network for Google Cloud TTS
    LIST_NETWORK_PARAMS_REQUIRED = ['test_ping_destination', 'test_download_destination']

    # network connection limits
    FLOAT_LATENCY_MAX = 2000.0          # 2 seconds
    FLOAT_SPEED_DOWNLOAD_MIN = 40960    # 5 Kbytes/s * 1024 * 8 -> bits/sec

    _client_tts = None                                          # Google Cloud TTS client
    _speed_test = None  # instance of speed test validator

    def set_configuration(self, dict_config):
        """
        Overrides corresponding method of abstract parent class.

        Extends:
            - Creates instance of TextToSpeechClient and sets it as _client_tts.
        """
        self._str_path_output_dir = "./data/cloud/google_cloud/audio"
        super(TTSGoogleCloudClient, self).set_configuration(dict_config)
        self._client_tts = texttospeech.TextToSpeechClient()

    def _str_to_audioencoding(self, str_format_file_audio):
        """
        Maps string to texttospeech.enums.AudioEncoding.

        :param str_format_file_audio: string - audio file format.
        :return: texttospeech.enums.AudioEncoding value.
        """
        enum_audio_encoding = None
        if str_format_file_audio == 'mp3':
            enum_audio_encoding = texttospeech.enums.AudioEncoding.MP3
        elif str_format_file_audio == 'ogg':
            enum_audio_encoding = texttospeech.enums.AudioEncoding.OGG_OPUS
        else:
            pass
        self.logger.debug("Convert result: '%s' to '%s'", str_format_file_audio, enum_audio_encoding)
        return enum_audio_encoding

    def synthesize_audio(self, source_text):
        """
        Implements corresponding method of interface parent class.

        Google Cloud TTS input params:
            Logical params:
                - language_code: language tag from BCP-47.
                - name: google_cloud voice name.
                * Description: https://cloud.google.com/text-to-speech/docs/reference/rpc/google.cloud.texttospeech.v1beta1#voiceselectionparams
                * List of available values: https://cloud.google.com/text-to-speech/docs/voices
            Technical params:
                - speaking_rate: speed of pronunciation.
                - pitch: voice pitch value.
                - effects_profile_id: audio effect profile.
                * Description: https://cloud.google.com/text-to-speech/docs/reference/rpc/google.cloud.texttospeech.v1beta1#audioconfig
        """
        import urllib3
        urllib3.disable_warnings()

        # generate output file path and name
        str_path_file_audio = self._get_path_file_audio(source_text)

        # check if audio file is already synthesized
        if self._is_audio_file_exist(str_path_file_audio):
            self.logger.info("Audio file with synthesized speech already exists. Get it %s.", str_path_file_audio)
            return str_path_file_audio
        else:
            # creates audio file corresponding to source text
            file_audio = open(str_path_file_audio, 'wb')
            self.logger.debug("Speech will be written to %s.", str_path_file_audio)

            if hasattr(source_text, 'read'):  # if source_text is represented as file
                try:
                    source_text = source_text.read()
                except UnicodeDecodeError as e:      # if source text file is not text file
                    self.logger.error(msg=str(e), exc_info=True)
                    exit()
                self.logger.debug("Source text is represented as file, read content.")

            # set the text input to be synthesized
            synthesis_input = texttospeech.types.SynthesisInput(text=source_text)

            # select voice params
            voice = texttospeech.types.VoiceSelectionParams(
                language_code=self._config_tts['call_params']['language_code'],
                name=self._config_tts['call_params']['name'])
            self.logger.debug("Voice params: \n%s", voice)

            # select the type of audio file you want returned
            audio_config = texttospeech.types.AudioConfig(
                audio_encoding=self._str_to_audioencoding(self._str_format_file_audio),
                speaking_rate=self._config_tts['call_params']['speaking_rate'],
                pitch=self._config_tts['call_params']['pitch'],
                effects_profile_id=self._config_tts['call_params']['effects_profile_id']
            )
            self.logger.debug("Audio params: \n%s", audio_config)

            # perform the text-to-speech request on the text input with the selected voice parameters and audio file type
            # the response's audio_content is binary
            try:
                response = self._client_tts.synthesize_speech(synthesis_input, voice, audio_config)
            except GoogleAPICallError as e:
                self.logger.error(msg=str(e), exc_info=True)
                exit()

            self.logger.debug("Response is gotten.")

            # write the response to the output file
            file_audio.write(response.audio_content)
            self.logger.debug("Response is writen to file.")

            return str_path_file_audio

    def synthesize_speech(self, source_text):
        """
        Implements corresponding method of interface parent class.

        * Google Cloud TTS does not support real time synthesis
        """
        pass

    def _validate_enviroment_variable(self, dict_config):
        """
        Validates GOOGLE_APPLICATION_CREDENTIALS environment variable set.

        * Details: https://cloud.google.com/docs/authentication/getting-started

        :raises:
            * GoogleApplicationCredentialsNotProvided - if required credentials are not provided.
        :param dict_config: configuration of Google Cloud TTS.
        :return: bool - true (valid) / false (invalid).
        """
        _str_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if _str_path is None:
            raise GoogleApplicationCredentialsNotProvided()
        self.logger.debug("GOOGLE_APPLICATION_CREDENTIALS file location = %s", _str_path)
        return True

    def _validate_call_params(self, dict_config):
        """
        Validates call params.

        :raises:
            * RequiredCallParamNotProvidedException - if required call param is not provided.
            * CallParamValueNotProvidedException - if call params value is not provided.
        :param dict_config: configuration of Google Cloud TTS.
        :return: bool - true (valid) / false (invalid).
        """
        _list_params_call_actual = dict_config['call_params'].keys()
        for _str_name_param_call in self.LIST_CALL_PARAMS_REQUIRED:
            if _str_name_param_call not in _list_params_call_actual:
                raise RequiredCallParamNotProvidedException(_str_name_param_call)

        for _str_name_param_call, _value in dict_config['call_params'].items():
            if not str(_value):     # if value is empty
                raise CallParamValueNotProvidedException(_str_name_param_call)

        self.logger.debug("Required call params are valid.")
        return True

    def _validate_network_params(self, dict_config):
        """
        Validates network params.

        :raises:
            * RequiredNetworkParamNotProvidedException - if required network param is not provided.
            * NetworkParamValueNotProvidedException - if required network param value is not provided.
        :param dict_config: configuration of Google Cloud TTS.
        :return: bool - true (valid) / false (invalid).
        """
        _list_params_call_actual = dict_config['network_params'].keys()
        for _str_name_param_call in self.LIST_NETWORK_PARAMS_REQUIRED:
            if _str_name_param_call not in _list_params_call_actual:
                raise RequiredNetworkParamNotProvidedException(_str_name_param_call)

        for _str_name_param_call, _value in dict_config['network_params'].items():
            if not str(_value):     # if value is empty
                raise NetworkParamValueNotProvidedException(_str_name_param_call)

        self.logger.debug("Required network params are valid.")
        return True

    def validate_configuration(self, dict_config):
        """
        Overrides corresponding method of interface parent class.
            - Responsible for full validation of configuration.
        Extends:
            - Validates specification of Google Cloud TTS.
            - Raises Google Cloud TTS exceptions.
        Checks:
            - Environment variable GOOGLE_APPLICATION_CREDENTIALS is set.
            - Call params are provided.
            - Network params are provided.
        """
        try:
            bool_result = self._validate_enviroment_variable(dict_config) and \
                   self._validate_call_params(dict_config) and \
                   self._validate_network_params(dict_config)
            if bool_result:
                self.logger.info("Specific validation of configuration succeeds.")
            else:
                self.logger.info("Specific validation of configuration fails.")
            return bool_result
        except RobotisOP2TTSException as e:
            self.logger.error(msg=str(e), exc_info=True)
            exit()

    def validate_network(self):
        """
        Overrides corresponding method of interface parent class.
            - Responsible for full validation of configuration.
        Extends:
            - Raises exceptions if validation was failed.
        Checks:
            - Internet access.
            - Download speed.
        :raises:
            * NetworkNotAccessibleException - if network connection is not set.
            * NetworkSpeedNotApplicableException - if network speed is too low.
        """
        from pyspeedtest import SpeedTest, init_logging

        if self._speed_test is None:
            init_logging()
            self._speed_test = SpeedTest(host=self._config_tts['network_params']['test_download_destination'], runs=1)

        self.logger.debug("SpeedTest instance is ready.")
        try:
            # returns latency in ms
            float_latency = self._speed_test.ping(self._config_tts['network_params']['test_ping_destination'])
            if float_latency > self.FLOAT_LATENCY_MAX:
                raise NetworkNotAccessibleException()
            self.logger.debug("Ping latency = %s, ms", float_latency)

            # returns download speed in bits/sec
            float_download_speed = self._speed_test.download()
            if float_download_speed < self.FLOAT_SPEED_DOWNLOAD_MIN:
                raise NetworkSpeedNotApplicableException()
            self.logger.debug("Download speed = %s, bits/sec", float_download_speed)
        except Exception as e:  # connection to Internet is not established
            self.logger.warn("No access to Internet.")
            return False

        self.logger.debug("Network validation succeeds.")
        return True
