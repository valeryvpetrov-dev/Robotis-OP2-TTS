from tts_engines.base import AbstractTTSClient
from ..base import InterfaceTTSCloudClient
from exceptions.tts_engines.cloud_clients.google_cloud import GoogleApplicationCredentialsNotProvided

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

    def set_configuration(self, dict_config):
        """
        Overrides corresponding method of abstract parent class.

        Extends:
            - Creates instance of TextToSpeechClient and sets it as _client_tts.
        """
        self._str_path_output_dir = "./data/cloud_clients/google_cloud/audio"
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
                * Description: https://cloud_clients.google.com/text-to-speech/docs/reference/rpc/google.cloud_clients.texttospeech.v1beta1#voiceselectionparams
                * List of available values: https://cloud_clients.google.com/text-to-speech/docs/voices
            Technical params:
                - speaking_rate: speed of pronunciation.
                - pitch: voice pitch value.
                - effects_profile_id: audio effect profile.
                * Description: https://cloud_clients.google.com/text-to-speech/docs/reference/rpc/google.cloud_clients.texttospeech.v1beta1#audioconfig
        """
        # creates audio file corresponding to source text
        if isinstance(source_text, TextIOBase):     # if source_text is represented as file
            str_name_file_audio = os.path.basename(source_text.name).split(".")[0]
            source_text = source_text.read()
        else:                                       # if source_text is represented as string
            str_name_file_audio = source_text[:10]  # first 10 character from file
        str_name_file_audio = "{name}.{extension}".format(name=str_name_file_audio,
                                                          extension=self._str_format_file_audio)
        str_path_file_audio = os.path.join(self._str_path_output_dir, str_name_file_audio)
        file_audio = open(str_path_file_audio, 'wb')

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
        return str_path_file_audio

    def synthesise_speech(self, source_text):
        """
        Implements corresponding method of interface parent class.
        """
        pass    # Google Cloud TTS does not support real time synthesis

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
        if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") is not None:
            return True
        else:
            raise GoogleApplicationCredentialsNotProvided()

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
        pass    # Google Cloud TTS does not require specific validation
