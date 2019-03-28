from exceptions.tts_engines.cloud import TTSCloudClientException


class GoogleApplicationCredentialsNotProvided(TTSCloudClientException):
    """
    Google Cloud application credentials are not provided exception.

    * Details: https://cloud_clients.google.com/docs/authentication/getting-started
    """
    def __init__(self) -> None:
        super().__init__("Environment variable GOOGLE_APPLICATION_CREDENTIALS is not provided.")
