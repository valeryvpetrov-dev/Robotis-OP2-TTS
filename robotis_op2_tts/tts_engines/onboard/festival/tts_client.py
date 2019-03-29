from tts_engines.base import AbstractTTSClient
from ..base import InterfaceTTSOnboardClient


class TTSFestivalClient(AbstractTTSClient, InterfaceTTSOnboardClient):
    """
    Festival TTS client class.
        - Festival TTS specification of InterfaceTTSOnboardClient.
        - Has structure like AbstractTTSClient.
        - Behaves like InterfaceTTSOnboardClient.
    """
    # required params to play speech
    LIST_PLAY_SPEECH_CALL_PARAMS_REQUIRED = ['--language']
    # required params to save speech
    LIST_SAVE_SPEECH_CALL_PARAMS_REQUIRED = ['expression']

    _str_command_play_speech = None     # command to play speech in real time
    _str_command_save_speech = None     # command to save speech as file

    def set_configuration(self, dict_config):
        """
        Overrides corresponding method of abstract parent class.

        Extends:
            - Initializes commands.
        """
        pass

    def synthesise_audio(self, source_text):
        """
        Implements corresponding method of interface parent class.

        Festival TTS save command input params:
            - expression - file or lisp s-expression to be evaluated before synthesis.
                * It is enough to set '(language_related_voice)'.
                * Details: http://www.linuxcertif.com/man/1/text2wave/
        """
        pass

    def synthesise_speech(self, source_text):
        """
        Implements corresponding method of interface parent class.

        Festival TTS play command input params:
            - language - input text / output speech language.
                * Festival TTS must support this language.
                * Details: https://linux.die.net/man/1/festival
        """
        pass

    def validate_configuration(self, dict_config):
        """
        Overrides corresponding method of interface parent class.

        Extends:
            - Validates specification of Festival TTS.
            - Raises Festival TTS exceptions.
        Checks:
            - Festival TTS is installed.
            - Passed language has support in festival.
        :raises:
            * FestivalNotInstalledException - if Festival TTS is not installed in system.
            * LanguageNotSupportedException - if language is not supported by Festival.
        """
        pass
