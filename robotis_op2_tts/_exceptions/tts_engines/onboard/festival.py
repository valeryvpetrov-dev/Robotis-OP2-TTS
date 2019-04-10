from _exceptions.base import RobotisOP2TTSException


class TTSFestivalException(RobotisOP2TTSException):
    """
    Parent class for all available exceptions that may occur in work of Festival TTS client.
    """
    def __init__(self, message):
        super(TTSFestivalException, self).__init__(message)


class FestivalNotAvailableException(TTSFestivalException):
    """
    Festival TTS is not available to call.
    """
    def __init__(self):
        super(FestivalNotAvailableException, self).__init__("Festival TTS is not available to call.")


class LanguageNotSupportedException(TTSFestivalException):
    """
    Festival TTS does not support language.
    """
    def __init__(self, str_language):
        super(LanguageNotSupportedException, self)\
            .__init__("Festival TTS does not support %s language."
                      % str_language)
