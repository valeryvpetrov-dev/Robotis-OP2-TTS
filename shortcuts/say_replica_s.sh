#!/usr/bin/env bash
# source local ~/.bashrc
source ~/.bashrc

VIRTUALENV_NAME="Robotis-OP2-TTS-venv"
ROSMASTER_NAME="rosmaster"

call_replica () {   # calls replica
# pre configuration
#    roslaunch robotis_op_onboard_launch robotis_op_whole_robot.launch  ! It must be run before in another terminal
    # source virtualenvwrapper commands to current script
    source $(which virtualenvwrapper.sh)
    # switch to TTS virtual environment
    workon ${VIRTUALENV_NAME}

# action
    # start motion
    rosrun robotis_dance robotis_dance "$1.txt" > /dev/null &
    # start speaking
    python tts.py play -f "./kids_lessons/$1.ssml" > /dev/null &

# post configuration
    deactivate
}

# check if replica name is valid
regexp_replica_name="L[0-9]+\.replica[0-9]+(_[0-9]+)?"
if [[ $1 =~ $regexp_replica_name ]]
then
    echo "Replica name '$1' matches pattern."
else
    echo "Replica name '$1' does not match pattern."
    exit 128
fi

# check if roscore is running
if pgrep -x ${ROSMASTER_NAME} > /dev/null
then
    echo "'$ROSMASTER_NAME' is already running."
else
    echo "'$ROSMASTER_NAME' is not running. Now it is starting."
    roscore
fi

call_replica $1