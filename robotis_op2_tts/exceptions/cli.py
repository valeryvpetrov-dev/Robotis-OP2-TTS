from .base import RobotisOP2TTSException


class ConfigurationFileNotFoundException(RobotisOP2TTSException):
    """
    Configuration file not found exception class.
    """
    def __init__(self) -> None:
        super().__init__("Configuration file was not found.")


class SourceTextFileNotFoundException(RobotisOP2TTSException):
    """
    Source text file not found exception class.
    """
    def __init__(self) -> None:
        super().__init__("Text file was not found.")


class SeveralSourceTextsException(RobotisOP2TTSException):
    """
    Several source texts available exception class.
    """
    def __init__(self) -> None:
        super().__init__("There are several sources of text. I can't figure out what to use.")


class NoSourceTextException(RobotisOP2TTSException):
    """
    No source texts available exception class.
    """
    def __init__(self) -> None:
        super().__init__("There is no text to speech.")
