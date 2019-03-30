from ...base import RobotisOP2TTSException


class TTSFestivalException(RobotisOP2TTSException):
    """
    Parent class for all available exceptions that may occur in work of Festival TTS client.
    """
    def __init__(self, message) -> None:
        super().__init__(message)


class FestivalNotAvailableException(TTSFestivalException):
    """
    Festival TTS is not available to call.
    """
    def __init__(self) -> None:
        super().__init__("Festival TTS is not available to call.")


class LanguageNotSupportedException(TTSFestivalException):
    """
    Festival TTS does not support language.
    """
    def __init__(self, str_language) -> None:
        super().__init__("Festival TTS does not support {language} language.".format(language=str_language))
