class RobotisOP2TTSException(BaseException):
    """
    Parent class for all available exceptions that may occur in work of Robotis OP2 Text-to-Speech (TTS).
    """
    def __init__(self, message):
        super(RobotisOP2TTSException, self).__init__(message)
