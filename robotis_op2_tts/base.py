class InterfaceTTSClient:
    """
    Abstract TTS client class.
        - Declares interface of interaction with TTS client.
        - Should be used as parent of all TTS clients.
    """
    def synthesise_audio(self, source_text):
        """
        Creates audio file with passed source_text spoken.

        * TTS synthesis method will be chosen by priority.
        * Audio file format - .mp3.
        * File will be stored in ./data/audio directory.

        :param source_text: string or file with text for synthesise.
        :return: string - path to synthesised file.
        """
        pass

    def synthesise_speech(self, source_text):
        """
        Speaks passed source_text in real time.

        * TTS synthesis method will be chosen by priority.

        :param source_text: string or file with text for synthesise.
        :return: None (speech will be pronounced).
        """
        pass

    def validate_configuration(self, dict_config):
        """
        Validates configuration of TTS client.

        :return: bool - indicator of succeeded validation.
        """
        pass
