class RobotisOP2TTSException(Exception):
    """
    Parent class for all available exceptions that may occur in work of Robotis OP2 Text-to-Speech (TTS).
    """
    def __init__(self, message) -> None:
        super().__init__(message)
