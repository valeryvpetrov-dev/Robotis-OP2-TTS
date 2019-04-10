from .base import RobotisOP2TTSException


class AudioFileFormatException(RobotisOP2TTSException):
    """
    Audio file format is not supporter exception class.
    """
    def __init__(self, str_format_file_audio):
        super(AudioFileFormatException, self)\
            .__init__("'%s' audio file format is not supported."
                      % str_format_file_audio)


class AudioFilePlayerException(RobotisOP2TTSException):
    """
    Audio player system program is not available exception class.
    """
    def __init__(self, str_name_audio_file_player):
        super(AudioFilePlayerException, self)\
            .__init__("'%s' audio player is not available."
                      % str_name_audio_file_player)


class TTSEnginesNotProvidedException(RobotisOP2TTSException):
    """
    TTS engines configurations are not provided exception class.
    """
    def __init__(self):
        super(TTSEnginesNotProvidedException, self).__init__("No one TTS engine configuration is not provided.")


class TTSEngineNotProvidedException(RobotisOP2TTSException):
    """
    One of TTS engine configurations is not provided exception class.
    """
    def __init__(self):
        super(TTSEngineNotProvidedException, self).__init__("One of TTS engines configuration is not provided.")


class TTSEnginePriorityNotNumberException(RobotisOP2TTSException):
    """
    TTS engine priority is not a number exception class.
    """
    def __init__(self):
        super(TTSEnginePriorityNotNumberException, self).__init__("TTS engine priority is not a number.")


class TTSEnginePriorityNotProvidedException(RobotisOP2TTSException):
    """
    Priority of TTS engine is not provided exception class.
    """
    def __init__(self):
        super(TTSEnginePriorityNotProvidedException, self).__init__("TTS priority is not provided.")
