from ...base import RobotisOP2TTSException


class TTSGoogleCloudException(RobotisOP2TTSException):
    """
    Parent class for all available exceptions that may occur in work of TTS cloud client.
    """
    def __init__(self, message) -> None:
        super().__init__(message)


class GoogleApplicationCredentialsNotProvided(TTSGoogleCloudException):
    """
    Google Cloud application credentials are not provided exception.

    * Details: https://cloud.google.com/docs/authentication/getting-started
    """
    def __init__(self) -> None:
        super().__init__("Environment variable GOOGLE_APPLICATION_CREDENTIALS is not provided.")


class CallParamNotFoundException(TTSGoogleCloudException):
    """
    Call param not found exception class.
    """
    def __init__(self) -> None:
        super().__init__("Cloud TTS call param not found exception.")


class NetworkParamNotFoundException(TTSGoogleCloudException):
    """
    Network param not found exception class.
    """
    def __init__(self) -> None:
        super().__init__("Cloud TTS network param not found exception.")


class NetworkNotAccessibleException(TTSGoogleCloudException):
    """
    Network is not accessible exception class.
    """
    def __init__(self) -> None:
        super().__init__("Network is not accessible, so cloud TTS can't work.")


class NetworkSpeedNotApplicableException(TTSGoogleCloudException):
    """
    Network speed is not applicable exception class.
    """
    def __init__(self) -> None:
        super().__init__("Network speed is not applicable, so cloud TTS can't work properly.")
