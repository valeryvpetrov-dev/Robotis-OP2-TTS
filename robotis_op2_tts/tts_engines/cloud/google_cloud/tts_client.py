from tts_engines.base import AbstractTTSClient
from ..base import InterfaceTTSCloudClient


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

    def set_configuration(self, dict_config):
        """
        Overrides corresponding method of abstract parent class.

        Extends:
            - Creates instance of TextToSpeechClient and sets it as _client_tts.
        """
        pass

    def synthesise_audio(self, source_text):
        """
        Implements corresponding method of interface parent class.

        Google Cloud TTS input params:
            Logical params:
                - language_code: language tag from BCP-47.
                - name: google_cloud voice name.
                * Description: https://cloud_clients.google.com/text-to-speech/docs/reference/rpc/google.cloud_clients.texttospeech.v1beta1#voiceselectionparams
                * List of available values: https://cloud_clients.google.com/text-to-speech/docs/voices
            Technical params:
                - speaking_rate: speed of pronunciation.
                - pitch: voice pitch value.
                - effects_profile_id: audio effect profile.
                * Description: https://cloud_clients.google.com/text-to-speech/docs/reference/rpc/google.cloud_clients.texttospeech.v1beta1#audioconfig
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
            - Raises Google Cloud TTS exceptions.
        Checks:
            - Environment variable GOOGLE_APPLICATION_CREDENTIALS is set.
                    Details: https://cloud_clients.google.com/docs/authentication/getting-started
        :raises:
            * GoogleApplicationCredentialsNotProvided - if required credentials are not provided.
        """
        pass

    def validate_network(self):
        """
        Overrides corresponding method of interface parent class.

        Extends:
            -
        Checks:
            -
        :raises:
            *
        """
        pass
