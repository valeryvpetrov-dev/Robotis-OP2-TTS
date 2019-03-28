from tts_engines.base import AbstractTTSClientDelegate
from .base import InterfaceTTSCloudClient


class TTSCloudClientDelegate(AbstractTTSClientDelegate, InterfaceTTSCloudClient):
    """
    TTS cloud_clients client delegate class.
        - Initializes specific TTS cloud_clients client based on passed configuration.
        - Redirects calls of interface methods to specific TTS cloud_clients client.
        - Has structure like AbstractTTSClientDelegate.
        - Behaves like InterfaceTTSCloudClient.
    """
    _speedTest = None   # instance of speed test validator

    def set_configuration(self, dict_config):
        """
        Overrides corresponding method of abstract parent class.

        Extends:
            - Creates instance of specific TTS cloud_clients client based on configuration and sets it as _client_tts.
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
        pass

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
        pass
