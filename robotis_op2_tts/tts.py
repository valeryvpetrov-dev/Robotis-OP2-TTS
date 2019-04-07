if __name__ == '__main__':
    """
    Robotis OP2 Text-to-Speech (TTS) client general usage script.

    1. Create TTS configuration and place it inside ./config;
    2. Pass path to configuration file and text (string or file) as params to program;
        You can get support:

            $ python tts.py -h
            usage: tts.py [-h] [-t TEXT] [-f FILE] [-c CONFIG]

            Robotis OP2 Text-to-Speech (TTS) client. To learn more visit:
            https://github.com/valera0798/Robotis-OP2-TTS

            optional arguments:
              -h, --help            show this help message and exit
              -t TEXT, --text TEXT  text to synthesize speech.
              -f FILE, --file FILE  path to text file with content to synthesize speech.
              -c CONFIG, --config CONFIG
                                    path to TTS configuration file.

    3. Create RobotisOP2TTS object;
    4. Set TTS configuration to object;
    4. Call synthesize_* method. Passed source of text will be handled automatically.
    """
    from tts_client import RobotisOP2TTSClient
    from cli.parser import CLIParser

    cli_parser = CLIParser()
    dict_args = cli_parser.parse_arguments()
    str_path_file_config = dict_args["config"]

    tts = RobotisOP2TTSClient(str_path_file_config)

    if dict_args.get("text"):
        str_text = dict_args["text"]
        if dict_args.get("operation") == "play":
            tts.synthesize_speech(str_text)
        elif dict_args.get("operation") == "save":
            str_path_file_audio = tts.synthesize_audio(str_text)
    elif dict_args.get("file"):
        file_text = open(dict_args["file"], 'r')
        if dict_args.get("operation") == "play":
            tts.synthesize_speech(file_text)
        elif dict_args.get("operation") == "save":
            str_path_file_audio = tts.synthesize_audio(file_text)
        file_text.close()
