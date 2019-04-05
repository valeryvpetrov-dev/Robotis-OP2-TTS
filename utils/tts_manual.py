"""
Script for manual generation of speech audio files based on text files.

1. Create ./input folder and place .txt file with text there.
2. Adjust configuration of TTS.
3. Run script as main or use synthesize function in other programs.
"""

import os
from google.cloud import texttospeech


def synthesize(str_text, file_audio,
               bool_is_ssml: bool,
               language_code: str, name: str,                                   # Logical params
               speaking_rate: float, pitch: float, effects_profile_id: list = []     # Technical params
               ):
    """
    Google Cloud TTS. Synthesizes speech audio file based on text using passed configuration.

    Note:
    * Google Cloud TTS is used for speech synthesis.
    * Internet access is required.
    * GOOGLE_APPLICATION_CREDENTIALS environment variable must be set.
        Details: https://cloud.google.com/docs/authentication/getting-started
    * Audio file will be automatically closed.

    :param str_text: text to convert to speech.
    :param file_audio: output audio file with synthesized speech.
    :param bool_is_ssml: Synthesize Speech Markup Language (SSML) - source text is marked up flag.

    Logical params:
    * Description: https://cloud.google.com/text-to-speech/docs/reference/rpc/google.cloud.texttospeech.v1beta1#voiceselectionparams
    * List of available values: https://cloud.google.com/text-to-speech/docs/voices
    :param language_code: language tag from BCP-47.
    :param name: Google Cloud TTS voice name.

    Technical params:
    * Description: https://cloud.google.com/text-to-speech/docs/reference/rpc/google.cloud.texttospeech.v1beta1#audioconfig
    :param speaking_rate: speed of pronunciation.
    :param pitch: voice pitch value.
    :param effects_profile_id: audio effect profile.
    :return: None (Audio file will be generated.)
    """
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    if bool_is_ssml:
        synthesis_input = texttospeech.types.SynthesisInput(ssml=str_text)
    else:
        synthesis_input = texttospeech.types.SynthesisInput(text=str_text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.types.VoiceSelectionParams(
        language_code=language_code,
        name=name)

    # Select the type of audio file you want returned
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3,
        speaking_rate=speaking_rate,
        pitch=pitch,
        effects_profile_id=effects_profile_id
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    # The response's audio_content is binary.
    # Write the response to the output file.
    file_audio.write(response.audio_content)

    file_audio.close()
    print('Audio file - {} was written.'.format(os.path.abspath(file_audio.name)))


if __name__ == '__main__':
    """
    Basic scenario of TTS.
    
    Usage:
    0. Get authentication credentials .json file and create environment variable. 
        Details: https://cloud.google.com/docs/authentication/getting-started
    1. Create ./input dir.
    2. Place .txt files there.
    3. Adjust TTS configuration - dict_config_tts. If you have several configurations place them in list_dict_config_tts.
        For each configuration ./output/<name> directory will be created.
    3. Run script.
    4. Check out result in ./output directory. Audio files have the same name as corresponding .txt.
    """
    from os import listdir

    str_path_input_dir = os.path.abspath("./input")
    str_path_output_dir = os.path.abspath("./output")
    try:
        os.mkdir(str_path_output_dir)
    except FileExistsError:
        pass

    list_dict_config_tts = [                                        # list of all configurations to be applied
        {
            "language_code": "en-GB",
            "name": "en-GB-Wavenet-A",
            "speaking_rate": 0.85,
            "pitch": 2.0,
            "effects_profile_id": ["large-home-entertainment-class-device"]
        }
    ]

    for str_name_input_file in listdir(str_path_input_dir):
        for dict_config_tts in list_dict_config_tts:
            str_name_config = dict_config_tts["name"]
            str_path_output_dir_config = "{dir}/{config}".format(dir=str_path_output_dir, config=str_name_config)
            try:
                os.mkdir(str_path_output_dir_config)
            except FileExistsError:
                pass

            bool_is_ssml = str_name_input_file.split(".")[-1] == "ssml"
            file_text = open("{dir}/{file}".format(dir=str_path_input_dir, file=str_name_input_file), 'r')

            str_name_file_audio = "{name}.{extension}"\
                .format(name=str_name_input_file.split(".")[0], extension="mp3")
            file_audio = open("{dir}/{file}".format(dir=str_path_output_dir_config, file=str_name_file_audio), 'wb')

            synthesize(file_text.read(), file_audio, bool_is_ssml, **dict_config_tts)

            print("Synthesis for configuration: {config} was done.".format(config=dict_config_tts))
        print("Synthesis for file {file_name} was done.\n".format(file_name=str_name_input_file))
