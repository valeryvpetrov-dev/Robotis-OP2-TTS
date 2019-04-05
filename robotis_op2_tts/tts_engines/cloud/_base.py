from base import InterfaceTTSClient


class InterfaceTTSCloudClient(InterfaceTTSClient):
    """
    Abstract TTS cloud client class.
        - Declares interface of interaction with TTS cloud client.
        - Extends interface of InterfaceTTSClient.
        - Should be used as parent of all TTS cloud clients.
    """
    def validate_network(self):
        """
        Validates network with regard to specific TTS cloud client requirements based on configuration.

        * Call of what method is performed via initialized instance.

        :return: bool - indicator of succeeded validation.
        """
        pass
