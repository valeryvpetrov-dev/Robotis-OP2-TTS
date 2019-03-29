from tts_engines.base import AbstractTTSClientDelegate
from .base import InterfaceTTSOnboardClient
from .festival.tts_client import TTSFestivalClient
from exceptions.base import RobotisOP2TTSException


class TTSOnboardClientDelegate(AbstractTTSClientDelegate, InterfaceTTSOnboardClient):
    """
    TTS onboard client delegate class.
        - Initializes specific TTS onboard client based on passed configuration.
        - Redirects calls of interface methods to specific TTS onboard client.
        - Has structure like AbstractTTSClientDelegate.
        - Behaves like InterfaceTTSOnboardClient.
    """
    def set_configuration(self, dict_config):
        """
        Overrides corresponding method of abstract parent class.

        Extends:
            - Creates instance of specific TTS onboard client based on configuration and sets it as _client_tts.
        """
        super().set_configuration(dict_config)

        try:
            for str_name_tts, dict_config_tts in self._config_tts.items():
                if str_name_tts == 'festival':
                    dict_config_tts_copy = dict_config_tts.copy()
                    dict_config_tts_copy['audio_file_format'] = self._config_tts['audio_file_format']
                    self._client_tts = TTSFestivalClient(dict_config_tts_copy)
                elif False:
                    pass  # fill for another onboard TTS clients
                else:
                    continue  # skip information not about TTS clients
        except RobotisOP2TTSException as e:
            exit(str(e))

    def synthesise_audio(self, source_text):
        """
        Implements corresponding method of interface parent class.
        """
        return self._client_tts.synthesise_audio(source_text)

    def synthesise_speech(self, source_text):
        """
        Implements corresponding method of interface parent class.
        """
        self._client_tts.synthesise_speech(source_text)

    def validate_configuration(self, dict_config):
        """
        Implements corresponding method of interface parent class.

        * If TTS onboard client configurations have something in common than method should be implemented.
        * For free format configuration there is no necessity to do general validation.
        """
        return True
