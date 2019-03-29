from tts_engines.base import AbstractTTSClientDelegate
from .base import InterfaceTTSCloudClient
from exceptions.base import RobotisOP2TTSException
from exceptions.tts_engines.cloud import CallParamNotFoundException, NetworkParamNotFoundException, \
                                            NetworkNotAccessibleException, NetworkSpeedNotApplicableException
from .google_cloud.tts_client import TTSGoogleCloudClient
import subprocess


class TTSCloudClientDelegate(AbstractTTSClientDelegate, InterfaceTTSCloudClient):
    """
    TTS cloud client delegate class.
        - Initializes specific TTS cloud client based on passed configuration.
        - Redirects calls of interface methods to specific TTS cloud client.
        - Has structure like AbstractTTSClientDelegate.
        - Behaves like InterfaceTTSCloudClient.
    """
    _speedTest = None   # instance of speed test validator

    def set_configuration(self, dict_config):
        """
        Overrides corresponding method of abstract parent class.

        Extends:
            - Creates instance of specific TTS cloud client based on configuration and sets it as _client_tts.
        """
        super().set_configuration(dict_config)

        for str_name_tts, dict_config_tts in self._config_tts.items():
            if str_name_tts == 'google_cloud_tts':
                dict_config_tts_copy = dict_config_tts.copy()
                dict_config_tts_copy['audio_file_format'] = self._config_tts['audio_file_format']
                self._client_tts = TTSGoogleCloudClient(dict_config_tts_copy)
            elif False:
                pass        # fill for another cloud tts engines
            else:
                continue    # skip information not about TTS clients
        self._config_tts.pop('audio_file_format', None)  # to not to duplicate data

    def synthesise_audio(self, source_text):
        """
        Implements corresponding method of interface parent class.
        """
        if self.validate_network():
            self._client_tts.synthesise_audio(source_text)

    def synthesise_speech(self, source_text):
        """
        Implements corresponding method of interface parent class.
        """
        if self.validate_network():
            str_path_file_audio = self._client_tts.synthesise_audio(source_text)
            str_command_play_audio = self._str_command_play_audio.format(file=str_path_file_audio)
            str_output_command_play_audio = subprocess.check_output(str_command_play_audio.split(' '),
                                                                    stderr=subprocess.STDOUT).decode('utf-8')
            print(str_output_command_play_audio)

    def validate_configuration(self, dict_config):
        """
        Overrides corresponding method of interface parent class.

        Extends:
            - Raises exceptions if validation was failed.
        Checks for each TTS client general configuration:
            - Required call params are provided.
            - Required network params are provided.
        :raises:
            * CallParamNotFoundException - if required call param is not provided.
            * NetworkParamNotFoundException - if required network param is not provided.
            * TTS clients exceptions - if validation of specific TTS client fails.
        """
        try:
            for str_name_tts, dict_config_tts in dict_config.items():
                # general validation with specific params
                if str_name_tts == 'google_cloud_tts':
                    LIST_CALL_PARAMS_REQUIRED = TTSGoogleCloudClient.LIST_CALL_PARAMS_REQUIRED
                    LIST_NETWORK_PARAMS_REQUIRED = TTSGoogleCloudClient.LIST_NETWORK_PARAMS_REQUIRED
                elif False:
                    pass        # fill for another cloud tts engines
                else:
                    continue    # skip information not about TTS clients

                for _str_name_param, _value in dict_config_tts['call_params'].items():
                    if _str_name_param in LIST_CALL_PARAMS_REQUIRED and _value is not None:
                        pass
                    else:
                        raise CallParamNotFoundException()

                for _str_name_param, _value in dict_config_tts['network'].items():
                    if _str_name_param in LIST_NETWORK_PARAMS_REQUIRED and _value is not None:
                        pass
                    else:
                        raise NetworkParamNotFoundException()
            return True
        except RobotisOP2TTSException as e:
            exit(str(e))

    def validate_network(self):
        """
        Overrides corresponding method of interface parent class.

        Extends:
            - Raises exceptions if validation was failed.
        Checks for _client_tts:
            - Internet access.
            - Download speed.
            - Specific validation.
        :raises:
            * NetworkNotAccessibleException - if network connection is not set.
            * NetworkSpeedNotApplicableException - if network speed is too low.
            * TTS clients exceptions - if validation of specific TTS client fails.
        """
        try:
            for str_name_tts, dict_config_tts in self._config_tts.items():
                # general validation with specific params
                if str_name_tts == 'google_cloud_tts':
                    FLOAT_LATENCY_MAX = TTSGoogleCloudClient.FLOAT_LATENCY_MAX
                    FLOAT_SPEED_DOWNLOAD_MIN = TTSGoogleCloudClient.FLOAT_SPEED_DOWNLOAD_MIN
                elif False:
                    pass        # fill for another cloud tts engines
                else:
                    continue    # skip information not about TTS clients

                from pyspeedtest import SpeedTest

                if self._speedTest is None:
                    self._speedTest = SpeedTest(host=dict_config_tts['network']['test_download_destination'], runs=5)

                # returns latency in ms
                float_latency = self._speedTest.ping(dict_config_tts['network']['test_ping_destination'])
                if float_latency > FLOAT_LATENCY_MAX:
                    raise NetworkNotAccessibleException()

                # returns download speed in bits/sec
                float_download_speed = self._speedTest.download()
                if float_download_speed < FLOAT_SPEED_DOWNLOAD_MIN:
                    raise NetworkSpeedNotApplicableException()

                # specific validation
                self._client_tts.validate_network()
            return True
        except RobotisOP2TTSException as e:
            exit(str(e))
