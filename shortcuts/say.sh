#!/usr/bin/env bash
# adjust variables for virtualenvwrapper usage
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3.4
# source virtualenvwrapper functions to current script
source `which virtualenvwrapper.sh`

# switch to TTS virtual environment
# ! replace name with your own
workon robotis-op2-tts-venv

# call python tts.py play -t TEXT
python tts.py play -t "$1"
deactivate