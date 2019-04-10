from _exceptions.base import RobotisOP2TTSException


class TTSGoogleCloudException(RobotisOP2TTSException):
    """
    Parent class for all available exceptions that may occur in work of TTS cloud client.
    """
    def __init__(self, message):
        super(TTSGoogleCloudException, self).__init__(message)


class GoogleApplicationCredentialsNotProvided(TTSGoogleCloudException):
    """
    Google Cloud application credentials are not provided exception.

    * Details: https://cloud.google.com/docs/authentication/getting-started
    """
    def __init__(self):
        super(GoogleApplicationCredentialsNotProvided, self).__init__("Environment variable GOOGLE_APPLICATION_CREDENTIALS is not provided.")


class RequiredCallParamNotProvidedException(TTSGoogleCloudException):
    """
    Required call param is not provided exception class.
    """
    def __init__(self, str_name_param_call_required):
        super(RequiredCallParamNotProvidedException, self)\
            .__init__("Google Cloud TTS required call param '%s' is not provided."
                         % str_name_param_call_required)


class RequiredNetworkParamNotProvidedException(TTSGoogleCloudException):
    """
    Required network param is not provided exception class.
    """
    def __init__(self, str_name_param_call_required):
        super(RequiredNetworkParamNotProvidedException, self)\
            .__init__("Google Cloud TTS required network param '%s' is not provided."
                      % str_name_param_call_required)


class CallParamValueNotProvidedException(TTSGoogleCloudException):
    """
    Required call param value is not provided exception class.
    """
    def __init__(self, str_name_param_call_required):
        super(CallParamValueNotProvidedException, self)\
            .__init__("Value related to call param '%s' is not provided. "
                      % str_name_param_call_required)


class NetworkParamValueNotProvidedException(TTSGoogleCloudException):
    """
    Required network param value is not provided exception class.
    """
    def __init__(self, str_name_param_call_required):
        super(NetworkParamValueNotProvidedException, self)\
            .__init__("Value related to network param '%s' is not provided. "
                      % str_name_param_call_required)


class NetworkNotAccessibleException(TTSGoogleCloudException):
    """
    Network is not accessible exception class.
    """
    def __init__(self):
        super(NetworkNotAccessibleException, self).__init__("Network is not accessible, so cloud TTS can't work.")


class NetworkSpeedNotApplicableException(TTSGoogleCloudException):
    """
    Network speed is not applicable exception class.
    """
    def __init__(self):
        super(NetworkSpeedNotApplicableException, self).__init__("Network speed is not applicable, so cloud TTS can't work properly.")
