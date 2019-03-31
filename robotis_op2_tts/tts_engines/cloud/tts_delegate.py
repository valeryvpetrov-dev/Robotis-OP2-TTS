from tts_engines.base import AbstractTTSClientDelegate
from .base import InterfaceTTSCloudClient
from .google_cloud.tts_client import TTSGoogleCloudClient
from exceptions.base import RobotisOP2TTSException
import subprocess


class TTSCloudClientDelegate(AbstractTTSClientDelegate, InterfaceTTSCloudClient):
    """
    TTS cloud client delegate class.
        - Initializes specific TTS cloud client based on passed configuration.
        - Redirects calls of interface methods to specific TTS cloud client.
        - Has structure like AbstractTTSClientDelegate.
        - Behaves like InterfaceTTSCloudClient.
    """
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
            return self._client_tts.synthesise_audio(source_text)

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
        Implements corresponding method of interface parent class.

        * If TTS cloud client configurations have something in common than method should be implemented.
        * For free format configuration there is no necessity to do general validation.
        """
        return True

    def validate_network(self):
        """
        Implements corresponding method of interface parent class.
        """
        return self._client_tts.validate_network()
