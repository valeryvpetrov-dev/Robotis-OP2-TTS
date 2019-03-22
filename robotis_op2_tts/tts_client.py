class RobotisOP2TTSClient:
    """
    Robotis OP 2 Text-to-Speech (TTS) client class.
    """
    def __init__(self, str_path_config_file):
        """
        Constructor of TTS client object.

        1. Initializes object;
        2. Sets passed configuration.
        """
        super().__init__()
        self.set_configuration(str_path_config_file)

    def set_configuration(self, str_path_config_file):
        """
        Setter for config_tts field.

        * Configuration file will be parsed to dictionary.
        * Configuration dictionary will be validated before set.

        :param str_path_config_file: path to tts configuration file.
        :return: None (object field __config_tts will be set).
        """
        from config.parser import parse_configuration

        dict_config_tts = parse_configuration(str_path_config_file)
        self.__config_tts = dict_config_tts

    def synthesise_audio(self, source_text):
        """
        Creates audio file with passed source_text spoken.

        * Audio file format - .mp3.
        * File will be stored in ./audio directory.

        :param source_text: string or file with text for synthesise.
        :return: audio file with synthesised speech.
        """
        pass    # TODO

    def synthesise_speech(self, source_text):
        """
        Speaks passed source_text.

        * Actually calls synthesise_audio and passes result to audio player.

        :param source_text: string or file with text for synthesise.
        :return: None.
        """
        pass    # TODO


if __name__ == '__main__':
    """
    Example of using Robotis OP2 Text-to-Speech (TTS) client.
    
    1. Create TTS configuration and place it inside ./config;
    2. Pass path to configuration file and text (string or file) as params to program;
        You can get support:
        
            $ python tts_client.py -h
            usage: tts_client.py [-h] [-t TEXT] [-f FILE] [-c CONFIG]
            
            Robotis OP2 Text-to-Speech (TTS) client. To learn more visit:
            https://github.com/valera0798/Robotis-OP2-TTS
            
            optional arguments:
              -h, --help            show this help message and exit
              -t TEXT, --text TEXT  text to synthesise speech.
              -f FILE, --file FILE  path to text file with content to synthesise speech.
              -c CONFIG, --config CONFIG
                                    path to TTS configuration file.
    
    3. Create RobotisOP2TTS object;
    4. Set TTS configuration to object;
    4. Call synthesise_* method. Passed source of text will be caught automatically.
    """
    # add path to current module to PYTHONPATH environment variable
    import sys
    sys.path.insert(0, '.')

    from cli.parser import parse_arguments

    dict_args = parse_arguments()
    str_path_config_file = dict_args["config"]

    tts = RobotisOP2TTSClient(str_path_config_file)

    if dict_args.get("text"):
        str_text = dict_args["text"]
        tts.synthesise_speech(str_text)
    elif dict_args.get("file"):
        file_text = open(dict_args["file"], 'r')
        tts.synthesise_speech(file_text)
        file_text.close()
