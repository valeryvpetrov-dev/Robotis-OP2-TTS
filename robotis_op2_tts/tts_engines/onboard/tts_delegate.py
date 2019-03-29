from tts_engines.base import AbstractTTSClientDelegate
from .base import InterfaceTTSOnboardClient


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
        pass

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

        * If TTS onboard client configurations have something in common than method should be implemented.
        * For free format configuration there is no necessity to do general validation.
        """
        pass
