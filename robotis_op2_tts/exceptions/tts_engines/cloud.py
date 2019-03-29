from ..base import RobotisOP2TTSException


class TTSCloudClientException(RobotisOP2TTSException):
    """
    Parent class for all available exceptions that may occur in work of TTS cloud client.
    """
    def __init__(self, message) -> None:
        super().__init__(message)


class CallParamNotFoundException(TTSCloudClientException):
    """
    Call param not found exception class.
    """
    def __init__(self) -> None:
        super().__init__("Cloud TTS call param not found exception.")


class NetworkParamNotFoundException(TTSCloudClientException):
    """
    Network param not found exception class.
    """
    def __init__(self) -> None:
        super().__init__("Cloud TTS network param not found exception.")


class NetworkNotAccessibleException(TTSCloudClientException):
    """
    Network is not accessible exception class.
    """
    def __init__(self) -> None:
        super().__init__("Network is not accessible, so cloud TTS can't work.")


class NetworkSpeedNotApplicableException(TTSCloudClientException):
    """
    Network speed is not applicable exception class.
    """
    def __init__(self) -> None:
        super().__init__("Network speed is not applicable, so cloud TTS can't work properly.")
