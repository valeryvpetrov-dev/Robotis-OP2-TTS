if __name__ == '__main__':
    """
    Robotis OP2 Text-to-Speech (TTS) client general usage script.

    1. Create TTS configuration and place it inside ./config;
    2. Pass path to configuration file as params to program;
        You can get support:

            $ python tts.py -h
            usage: tts.py [-h] [-c CONFIG]

            Robotis OP2 Text-to-Speech (TTS) client. To learn more visit:
            https://github.com/valera0798/Robotis-OP2-TTS

            optional arguments:
              -h, --help            show this help message and exit
              -t TEXT, --text TEXT  text to synthesize speech.
    
    3. In the start of session 
        3.1. Create RobotisOP2TTS object;
    4. Input commands in CLI to call specific methods of RobotisOP2TTS instance.
        You can get support:
            
            tts> help
            Robotis OP2 Text-to-Speech (TTS) client. To learn more visit:
            https://github.com/valera0798/Robotis-OP2-TTSusage: <command> [arguments] 
            Available commands:
                help                     - show this help message.
                say [string/file path]   - speaks passed text from source.
                save [string/file path]  - saves synthesized text to file.
                exit                     - ends current session.
    """
    from tts_client import RobotisOP2TTSClient
    from cli import CLI
    import re
    from os.path import abspath

    cli = CLI()
    dict_args = cli.parse_arguments()
    str_path_file_config = dict_args["config"]

    tts = RobotisOP2TTSClient(str_path_file_config)

    regex_file = re.compile(r'\.?(\/[\w]+)*\/[\w]+\.[\w]+')
    source_text = None
    bool_is_session_opened = True
    cli.logger.info("Session has been begun.")
    while bool_is_session_opened:
        tuple_str_command_list_args = cli.read_command()
        if tuple_str_command_list_args:
            str_command = tuple_str_command_list_args[0]
            list_args = tuple_str_command_list_args[1]
            if str_command == 'exit':
                bool_is_session_opened = False
            elif str_command == 'help':
                cli.print_prompt()
            else:
                try:
                    if regex_file.match(list_args[0]):
                        if list_args[0][0] == '.':  # if source file is located in local input directory
                            list_args[0] = list_args[0].replace('.', abspath('./input/'), 1)
                        source_text = open(list_args[0])
                    else:
                        source_text = list_args[0]
                        
                    if str_command == 'say':
                        tts.synthesize_speech(source_text)
                    elif str_command == 'save':
                        tts.synthesize_audio(source_text)
                except IOError as e:
                    cli.logger.error(msg=str(e))

    cli.logger.info("Session has been ended.")
    if source_text:
        if hasattr(source_text, 'read'):
            source_text.close()
