from tts_engines._base import AbstractTTSClient
from .._base import InterfaceTTSOnboardClient
from _exceptions.tts_engines.onboard.festival import *


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
        super(TTSFestivalClient, self).set_configuration(dict_config)

        # compile _str_command_play_speech
        self._str_command_play_speech = self._config_tts['play']['command']
        _list_param_call = []
        for _str_param_call, value in self._config_tts['play']['call_params'].items():
            _list_param_call.append("%s %s" % (_str_param_call, str(value)))
        self._str_command_play_speech = self._str_command_play_speech\
            .replace("{call_params}", " ".join(_list_param_call))
        self._str_command_play_speech = self._str_command_play_speech.encode('ascii', 'ignore')

        # compile _str_command_save_speech
        _str_command_save_speech = self._config_tts['save']['command'].encode('ascii', 'ignore')
        self._str_command_save_speech = _str_command_save_speech\
            .replace("{expression}", str(self._config_tts['save']['expression']))

    def synthesize_audio(self, source_text):
        """
        Implements corresponding method of interface parent class.

        Festival TTS save command input params:
            - expression - file or lisp s-expression to be evaluated before synthesis.
                * It is enough to set '(language_related_voice)'.
                * Details: http://www.linuxcertif.com/man/1/text2wave/
        """
        import subprocess

        # generate output file path and name
        str_path_file_audio = self._get_path_file_audio(source_text)

        # check if audio file is already synthesized
        if self._is_audio_file_exist(str_path_file_audio):
            self.logger.info("Audio file with synthesized speech already exists. Get it %s.", str_path_file_audio)
            return str_path_file_audio
        else:
            self.logger.debug("Speech will be written to %s.", str_path_file_audio)

            if hasattr(source_text, 'read'):     # if source_text is represented as file
                try:
                    source_text = source_text.read()
                except UnicodeDecodeError as e:         # if source text file is not text file
                    self.logger.error(msg=str(e), exc_info=True)
                    exit()
                self.logger.debug("Source text is represented as file, read content.")

            try:
                _str_command_save_speech = self._str_command_save_speech.replace("{text}", source_text)
                _str_command_save_speech = _str_command_save_speech.replace("{file}", str_path_file_audio)
                _int_code_result = subprocess.check_call(
                    _str_command_save_speech,
                    stderr=subprocess.STDOUT,
                    shell=True      # security hazard
                )
            except subprocess.CalledProcessError as e:
                self.logger.error(msg=str(e), exc_info=True)
                exit()

            if _int_code_result == 0:   # success
                self.logger.debug("Synthesized speech is written to file.")
                return str_path_file_audio
            else:
                self.logger.debug("Speech is not synthesized to file.")
                return None

    def synthesize_speech(self, source_text):
        """
        Implements corresponding method of interface parent class.

        Festival TTS play command input params:
            - language - input text / output speech language.
                * Festival TTS must support this language.
                * Details: https://linux.die.net/man/1/festival
        """
        import subprocess

        if hasattr(source_text, 'read'):  # if source_text is represented as file
            try:
                source_text = source_text.read()
            except UnicodeDecodeError as e:      # if source text file is not text file
                self.logger.error(msg=str(e), exc_info=True)
                exit()
            self.logger.debug("Source text is represented as file, read content.")

        try:
            _int_code_result = subprocess.check_call(
                self._str_command_play_speech.replace("{text}", source_text),
                stderr=subprocess.STDOUT,
                shell=True      # security hazard
            )
        except subprocess.CalledProcessError as e:
            self.logger.error(msg=str(e), exc_info=True)
            exit()

        if _int_code_result == 0:   # success
            self.logger.debug("Speech is synthesized.")
            return True
        else:
            self.logger.debug("Speech is not synthesized.")
            return False

    def _validate_availability(self, dict_config):
        """
        Validates Festival installation.

        :raises:
            * FestivalNotInstalledException - if Festival is not installed.
        :param dict_config: Festival TTS configuration.
        :return: bool - true (valid), false (invalid).
        """
        import subprocess

        try:
            _str_output = subprocess.check_output(["which", "festival"])
            if len(_str_output) == 0:
                raise FestivalNotAvailableException()
            self.logger.debug("Festival is available at %s.", _str_output)
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(msg=str(e), exc_info=True)
            exit()

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

        try:
            _str_name_language = dict_config['play']['call_params']['--language']

            # for current configuration of Festival
            try:
                _str_path_dir_share_festival_languages = '/usr/share/festival/languages/'
                for _str_name_file in listdir(_str_path_dir_share_festival_languages):
                    if _str_name_language in _str_name_file:        # check all files that corresponds to language
                        _str_path_file_language = _str_path_dir_share_festival_languages + _str_name_file
                        if stat(_str_path_file_language).st_size != 0:  # file is not emtpy
                            self.logger.debug("%s language settings file = %s.",
                                              _str_name_language, _str_path_file_language)
                            self.logger.debug("%s language is supported.", _str_name_language)
                            return True     # does not check other configurations if one exists
                        else:   # it is possible that language directory contains several configurations
                            pass
            except OSError as e:    # no languages directory
                pass

            # for Robotis OP2 configuration of Festival
            try:
                _str_path_file_share_festival_languages = '/usr/share/festival/languages.scm'
                _str_keyword = "define (language_%s)" % _str_name_language
                _file_languages = open(_str_path_file_share_festival_languages, 'r')
                for _str_line in _file_languages:
                    if _str_keyword in _str_line:
                        return True
                _file_languages.close()
            except OSError as e:    # no languages file
                pass

            raise LanguageNotSupportedException(_str_name_language)
        except IOError as e:
            self.logger.error(msg=str(e), exc_info=True)
            exit()

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
            bool_result = self._validate_availability(dict_config) and \
                   self._validate_language_support(dict_config)
            if bool_result:
                self.logger.info("Specific validation of configuration succeeds.")
            else:
                self.logger.info("Specific validation of configuration fails.")
            return bool_result
        except RobotisOP2TTSException as e:
            self.logger.error(msg=str(e), exc_info=True)
            exit()
