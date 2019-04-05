from tts_engines._base import AbstractTTSClientDelegate
from ._base import InterfaceTTSOnboardClient
from .festival.tts_client import TTSFestivalClient


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
        super(TTSOnboardClientDelegate, self).set_configuration(dict_config)

        for str_name_tts, dict_config_tts in self._config_tts.items():
            if str_name_tts == 'festival':
                dict_config_tts_copy = dict_config_tts.copy()
                dict_config_tts_copy['audio_file_format'] = self._config_tts['audio_file_format']
                self._client_tts = TTSFestivalClient(dict_config_tts_copy)
            elif False:
                pass  # fill for another onboard TTS clients
            else:
                continue  # skip information not about TTS clients

    def synthesize_audio(self, source_text):
        """
        Implements corresponding method of interface parent class.
        """
        self.logger.info("Speech synthesis starts. Please, wait.")
        self.logger.debug("It redirects call to %s.", self._client_tts)
        return self._client_tts.synthesize_audio(source_text)

    def synthesize_speech(self, source_text):
        """
        Implements corresponding method of interface parent class.
        """
        self.logger.info("Speech synthesis starts. Please, wait.")
        self.logger.debug("It redirects call to %s.", self._client_tts)
        return self._client_tts.synthesize_speech(source_text)

    def validate_configuration(self, dict_config):
        """
        Implements corresponding method of interface parent class.

        * If TTS onboard client configurations have something in common than method should be implemented.
        * For free format configuration there is no necessity to do general validation.
        """
        bool_result = True
        if bool_result:
            self.logger.debug("Configuration validation succeeds.")
        else:
            self.logger.debug("Configuration validation fails.")
        return bool_result
