#!/usr/bin/env bash
# action
# start motion
rosrun robotis_dance robotis_dance "$1.txt" > /dev/null &   # run on background
# start speaking
python tts.py play -f "./kids_lessons/$1.ssml" > /dev/null &    # run on background, silent