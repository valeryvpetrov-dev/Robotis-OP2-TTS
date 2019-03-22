from .base import RobotisOP2TTSException


class AudioFileFormatException(RobotisOP2TTSException):
    """
    Audio file format is not supporter exception class.
    """
    def __init__(self) -> None:
        super().__init__("Audio file format is not supported.")


class AudioFilePlayerException(RobotisOP2TTSException):
    """
    Audio player system program is not available exception class.
    """
    def __init__(self) -> None:
        super().__init__("Audio player is not available.")


class TTSEnginesNoProvidedException(RobotisOP2TTSException):
    """
    TTS engines configurations were not provided exception class.
    """
    def __init__(self) -> None:
        super().__init__("No one TTS engine configuration was not provided.")
