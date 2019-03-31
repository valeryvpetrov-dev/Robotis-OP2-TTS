from tts_engines.base import AbstractTTSClient
from ..base import InterfaceTTSOnboardClient
from exceptions.base import RobotisOP2TTSException
from exceptions.tts_engines.onboard.festival import FestivalNotAvailableException, LanguageNotSupportedException


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
        self._str_path_output_dir = "./data/onboard/festival/audio"
        super().set_configuration(dict_config)

        # compile _str_command_play_speech
        self._str_command_play_speech = self._config_tts['play']['command']
        _list_param_call = []
        for _str_param_call, value in self._config_tts['play']['call_params'].items():
            _list_param_call.append("{key} {value}".format(key=_str_param_call, value=str(value)))
        self._str_command_play_speech = self._str_command_play_speech\
            .replace("{call_params}", " ".join(_list_param_call))

        # compile _str_command_save_speech
        self._str_command_save_speech = self._config_tts['save']['command']\
            .replace("{expression}", str(self._config_tts['save']['expression']))

    def synthesise_audio(self, source_text):
        """
        Implements corresponding method of interface parent class.

        Festival TTS save command input params:
            - expression - file or lisp s-expression to be evaluated before synthesis.
                * It is enough to set '(language_related_voice)'.
                * Details: http://www.linuxcertif.com/man/1/text2wave/
        """
        from io import TextIOBase
        import subprocess

        _str_path_file_audio = self._get_path_file_audio(source_text)

        if isinstance(source_text, TextIOBase):     # if source_text is represented as file
            source_text = source_text.read()

        _int_code_result = subprocess.check_call(
            self._str_command_save_speech.format(text=source_text, file=_str_path_file_audio),
            stderr=subprocess.STDOUT,
            shell=True      # security hazard
        )
        if _int_code_result == 0:   # success
            print('Audio file - {} was written.'.format(_str_path_file_audio))

            return _str_path_file_audio

    def synthesise_speech(self, source_text):
        """
        Implements corresponding method of interface parent class.

        Festival TTS play command input params:
            - language - input text / output speech language.
                * Festival TTS must support this language.
                * Details: https://linux.die.net/man/1/festival
        """
        from io import TextIOBase
        import subprocess

        _str_path_file_audio = self._get_path_file_audio(source_text)

        if isinstance(source_text, TextIOBase):  # if source_text is represented as file
            source_text = source_text.read()

        _str_output = subprocess.check_output(
            self._str_command_play_speech.format(text=source_text),
            stderr=subprocess.STDOUT,
            shell=True      # security hazard
        ).decode('utf-8')
        print(_str_output)
        return _str_path_file_audio

    def _validate_availability(self, dict_config):
        """
        Validates Festival installation.

        :raises:
            * FestivalNotInstalledException - if Festival is not installed.
        :param dict_config: Festival TTS configuration.
        :return: bool - true (valid), false (invalid).
        """
        import subprocess

        if len(subprocess.check_output(["which", "festival"])) == 0:
            raise FestivalNotAvailableException()
        return True

    def _validate_language_support(self, dict_config):
        """
        Validates if Festival supports passed language.

        Checks:
            - Festival language file is not empty.
                * Location of language settings may vary between versions of Festival.
        :raises:
            * LanguageNotSupportedException - if Festival dose not support language.
        :param dict_config: Festival TTS configuration.
        :return: bool - true (valid), false (invalid).
        """
        from os import stat, listdir

        # for current configuration of Festival
        _str_path_dir_share_festival_languages = '/usr/share/festival/languages/'
        _str_name_language = dict_config['play']['call_params']['--language']
        for _str_name_file in listdir(_str_path_dir_share_festival_languages):
            if _str_name_language in _str_name_file:        # check all files that corresponds to language
                if stat(_str_path_dir_share_festival_languages + _str_name_file).st_size == 0:  # file is emtpy
                    raise LanguageNotSupportedException(_str_name_language)
        return True

    def validate_configuration(self, dict_config):
        """
        Overrides corresponding method of interface parent class.

        Extends:
            - Validates specification of Festival TTS.
            - Raises Festival TTS exceptions.
        Checks:
            - Festival TTS is installed.
            - Passed language has support in festival.
        """
        try:
            return self._validate_availability(dict_config) and \
                   self._validate_language_support(dict_config)
        except RobotisOP2TTSException as e:
            exit(str(e))
