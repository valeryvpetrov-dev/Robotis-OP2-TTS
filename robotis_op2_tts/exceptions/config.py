from .base import RobotisOP2TTSException


class AudioFileFormatException(RobotisOP2TTSException):
    """
    Audio file format is not supporter exception class.
    """
    def __init__(self, str_format_file_audio) -> None:
        super().__init__("'{}' audio file format is not supported.".format(str_format_file_audio))


class AudioFilePlayerException(RobotisOP2TTSException):
    """
    Audio player system program is not available exception class.
    """
    def __init__(self, str_name_audio_file_player) -> None:
        super().__init__("'{}' audio player is not available.".format(str_name_audio_file_player))


class TTSEnginesNotProvidedException(RobotisOP2TTSException):
    """
    TTS engines configurations are not provided exception class.
    """
    def __init__(self) -> None:
        super().__init__("No one TTS engine configuration is not provided.")


class TTSEngineNotProvidedException(RobotisOP2TTSException):
    """
    One of TTS engine configurations is not provided exception class.
    """
    def __init__(self) -> None:
        super().__init__("One of TTS engines configuration is not provided.")


class TTSEnginePriorityNotNumberException(RobotisOP2TTSException):
    """
    TTS engine priority is not a number exception class.
    """
    def __init__(self) -> None:
        super().__init__("TTS engine priority is not a number.")


class TTSEnginePriorityNotProvidedException(RobotisOP2TTSException):
    """
    Priority of TTS engine is not provided exception class.
    """
    def __init__(self) -> None:
        super().__init__("TTS priority is not provided.")
