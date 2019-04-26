#!/usr/bin/env bash

# source virtualenvwrapper commands to current script
source $(which virtualenvwrapper.sh)
# switch to TTS virtual environment
workon "Robotis-OP2-TTS-venv"

# action
# start motion
rosrun robotis_dance robotis_dance "$1.txt" > /dev/null &   # run on background
# start speaking
python tts.py play -f "./kids_lessons/$1.ssml" > /dev/null &    # run on background, silent

# post configuration
deactivate