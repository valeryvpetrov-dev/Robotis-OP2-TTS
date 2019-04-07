class InterfaceTTSClient(object):
    """
    Abstract TTS client class.
        - Declares interface of interaction with TTS client.
        - Should be used as parent of all TTS clients.
    """
    def synthesize_audio(self, source_text):
        """
        Creates audio file with passed source_text spoken.

        * TTS synthesis method will be chosen by priority.
        * Audio file format - .mp3.
        * File will be stored in ./data/audio directory.

        :param source_text: string or file with text for synthesize.
        :return: string - path to synthesized file.
        """
        pass

    def synthesize_speech(self, source_text):
        """
        Speaks passed source_text in real time.

        * TTS synthesis method will be chosen by priority.

        :param source_text: string or file with text for synthesize.
        :return: bool - indicator of succeeded synthesis.
        """
        pass

    def validate_configuration(self, dict_config):
        """
        Validates configuration of TTS client.

        * Call of what method is performed before instance initialization.

        :return: bool - indicator of succeeded validation.
        """
        pass


class LoggableInterface(object):
    """
    Abstract class that is responsible for logging.
        - Declares abstract structure of loggable class.
        - Should be used as parent of all classes that needs in logging facilities.
    """
    from logging import DEBUG, INFO

    logger = None                   # logger instance that provides logging interface
    _console_handler = None         # console logs handler
    _console_formatter = None       # console logs formatter

    def __init__(self, name, level=INFO):
        super(LoggableInterface, self).__init__()

        import logging
        from sys import stdout

        # changing default logging level of root logger from WARNING to DEBUG
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)

        # create specific logger for heir
        self.logger = logging.getLogger(name)
        # adjust handler to redirect logs to stdout
        self.console_handler = logging.StreamHandler(stdout)
        self.console_handler.setLevel(level)
        # adjust LogRecord format
        self.console_formatter = logging.Formatter("[%(asctime)s] [%(process)d:%(name)25s] [%(levelname)8s] "
                                                   "--- %(message)s (%(filename)s:%(lineno)s)")
        self.console_handler.setFormatter(self.console_formatter)
        # bind handler with logger
        self.logger.addHandler(self.console_handler)
