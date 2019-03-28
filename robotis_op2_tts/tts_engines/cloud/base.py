from base import InterfaceTTSClient


class InterfaceTTSCloudClient(InterfaceTTSClient):
    """
    Abstract TTS cloud_clients client class.
        - Declares interface of interaction with TTS cloud_clients client.
        - Extends interface of InterfaceTTSClient.
        - Should be used as parent of all TTS cloud_clients clients.
    """
    def validate_network(self):
        """
        Validates network with regard to specific TTS cloud_clients client requirements based on configuration.

        :return: bool - indicator of succeeded validation.
        """
        pass
