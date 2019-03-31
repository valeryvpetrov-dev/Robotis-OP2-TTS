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
              -t TEXT, --text TEXT  text to synthesize speech.
              -f FILE, --file FILE  path to text file with content to synthesize speech.
              -c CONFIG, --config CONFIG
                                    path to TTS configuration file.

    3. Create RobotisOP2TTS object;
    4. Set TTS configuration to object;
    4. Call synthesize_* method. Passed source of text will be caught automatically.
    """
    # add path to current module to PYTHONPATH environment variable
    import sys

    sys.path.insert(0, '.')

    from tts_client import RobotisOP2TTSClient
    from cli.parser import parse_arguments

    dict_args = parse_arguments()
    str_path_file_config = dict_args["config"]

    tts = RobotisOP2TTSClient(str_path_file_config)

    if dict_args.get("text"):
        str_text = dict_args["text"]
        str_path_file_audio = tts.synthesize_audio(str_text)
        print("Client got audio: {}".format(str_path_file_audio))
    elif dict_args.get("file"):
        file_text = open(dict_args["file"], 'r')
        tts.synthesize_speech(file_text)
        file_text.close()
