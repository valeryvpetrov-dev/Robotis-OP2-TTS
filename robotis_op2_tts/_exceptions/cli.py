from .base import RobotisOP2TTSException


class ConfigurationFileNotFoundException(RobotisOP2TTSException):
    """
    Configuration file not found exception class.
    """
    def __init__(self):
        super(ConfigurationFileNotFoundException, self).__init__("Configuration file was not found.")


class ConfigurationFileEmptyException(RobotisOP2TTSException):
    """
    Configuration file empty exception class.
    """
    def __init__(self):
        super(ConfigurationFileEmptyException, self).__init__("Configuration file is empty.")


class ConfigurationFileWrongFormatException(RobotisOP2TTSException):
    """
    Configuration file wrong format exception class.
        - Non-json.
    """
    def __init__(self, str_format_file_config):
        super(ConfigurationFileWrongFormatException, self)\
            .__init__("Configuration file has wrong format. Required - JSON, got - %s."
                      % str_format_file_config)


class SourceTextFileNotFoundException(RobotisOP2TTSException):
    """
    Source text file not found exception class.
    """
    def __init__(self):
        super(SourceTextFileNotFoundException, self).__init__("Text file was not found.")


class SourceTextEmptyException(RobotisOP2TTSException):
    """
    Text source is empty exception class.
    """
    def __init__(self):
        super(SourceTextEmptyException, self).__init__("Text source is empty.")


class SeveralSourceTextsException(RobotisOP2TTSException):
    """
    Several source texts available exception class.
    """
    def __init__(self):
        super(SeveralSourceTextsException, self).__init__("There are several sources of text. I can't figure out what to use.")


class NoSourceTextException(RobotisOP2TTSException):
    """
    No source texts available exception class.
    """
    def __init__(self):
        super(NoSourceTextException, self).__init__("There is no text to speech.")


class InvalidCommandException(RobotisOP2TTSException):
    """
    Input command is not valid exception class.
    """
    def __init__(self, str_format_file_config):
        super(InvalidCommandException, self).__init__("Command '%s' is not valid." % str_format_file_config)
