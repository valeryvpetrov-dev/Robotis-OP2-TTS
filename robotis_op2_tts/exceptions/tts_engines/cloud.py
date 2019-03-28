from ..base import RobotisOP2TTSException


class TTSCloudClientException(RobotisOP2TTSException):
    """
    Parent class for all available exceptions that may occur in work of TTS cloud_clients client.
    """
    def __init__(self, message) -> None:
        super().__init__(message)
