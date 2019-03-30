from tts_engines.base import AbstractTTSClient
from ..base import InterfaceTTSCloudClient
from exceptions.tts_engines.cloud.google_cloud import *

import os
from io import TextIOBase

from google.cloud import texttospeech


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
    _speedTest = None  # instance of speed test validator

    def set_configuration(self, dict_config):
        """
        Overrides corresponding method of abstract parent class.

        Extends:
            - Creates instance of TextToSpeechClient and sets it as _client_tts.
        """
        self._str_path_output_dir = "./data/cloud/google_cloud/audio"
        super().set_configuration(dict_config)
        self._client_tts = texttospeech.TextToSpeechClient()

    def _str_to_audioencoding(self, str_format_file_audio):
        """
        Maps string to texttospeech.enums.AudioEncoding.

        :param str_format_file_audio: string - audio file format.
        :return: texttospeech.enums.AudioEncoding value.
        """
        if str_format_file_audio == 'mp3':
            return texttospeech.enums.AudioEncoding.MP3
        elif str_format_file_audio == 'ogg':
            return texttospeech.enums.AudioEncoding.OGG_OPUS
        else:
            pass

    def synthesise_audio(self, source_text):
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
        # creates audio file corresponding to source text
        _str_path_file_audio = self._get_path_file_audio(source_text)
        file_audio = open(_str_path_file_audio, 'wb')

        if isinstance(source_text, TextIOBase):  # if source_text is represented as file
            source_text = source_text.read()

        # set the text input to be synthesized
        synthesis_input = texttospeech.types.SynthesisInput(text=source_text)

        # select voice params
        voice = texttospeech.types.VoiceSelectionParams(
            language_code=self._config_tts['call_params']['language_code'],
            name=self._config_tts['call_params']['name'])

        # select the type of audio file you want returned
        audio_config = texttospeech.types.AudioConfig(
            audio_encoding=self._str_to_audioencoding(self._str_format_file_audio),
            speaking_rate=self._config_tts['call_params']['speaking_rate'],
            pitch=self._config_tts['call_params']['pitch'],
            effects_profile_id=self._config_tts['call_params']['effects_profile_id']
        )

        # perform the text-to-speech request on the text input with the selected voice parameters and audio file type
        # the response's audio_content is binary
        response = self._client_tts.synthesize_speech(synthesis_input, voice, audio_config)

        # write the response to the output file
        file_audio.write(response.audio_content)

        print('Audio file - {} was written.'.format(os.path.abspath(file_audio.name)))
        return _str_path_file_audio

    def synthesise_speech(self, source_text):
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
        if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") is None:
            raise GoogleApplicationCredentialsNotProvided()
        return True

    def _validate_call_params(self, dict_config):
        """
        Validates call params.

        :raises:
            * CallParamNotFoundException - if call params are not provided.
        :param dict_config: configuration of Google Cloud TTS.
        :return: bool - true (valid) / false (invalid).
        """
        for _str_name_param_call, _value in dict_config['call_params'].items():
            if _str_name_param_call not in self.LIST_CALL_PARAMS_REQUIRED or _value is None:
                raise CallParamNotFoundException()
        return True

    def _validate_network_params(self, dict_config):
        """
        Validates network params.

        :raises:
            * NetworkParamNotFoundException - if call network params are not provided.
        :param dict_config: configuration of Google Cloud TTS.
        :return: bool - true (valid) / false (invalid).
        """
        for _str_name_param_call, _value in dict_config['network'].items():
            if _str_name_param_call not in self.LIST_NETWORK_PARAMS_REQUIRED or _value is None:
                raise NetworkParamNotFoundException()
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
            return self._validate_enviroment_variable(dict_config) and \
                   self._validate_call_params(dict_config) and \
                   self._validate_network_params(dict_config)
        except RobotisOP2TTSException as e:
            exit(str(e))

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
        from pyspeedtest import SpeedTest

        if self._speedTest is None:
            self._speedTest = SpeedTest(host=self._config_tts['network']['test_download_destination'], runs=2)

        # returns latency in ms
        float_latency = self._speedTest.ping(self._config_tts['network']['test_ping_destination'])
        if float_latency > self.FLOAT_LATENCY_MAX:
            raise NetworkNotAccessibleException()

        # returns download speed in bits/sec
        float_download_speed = self._speedTest.download()
        if float_download_speed < self.FLOAT_SPEED_DOWNLOAD_MIN:
            raise NetworkSpeedNotApplicableException()

        return True
