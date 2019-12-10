#!/bin/sh

#tmux new-session -d -s hector 'python3 src/HardwareRunner.py'
#tmux new-window -t  hector:1 'python3 src/NeoPixel.py'
#python3 src/main.py

cd /home/pi/Satoshi24/src
KIVY_GL_BACKEND=gl /usr/bin/python3 main.py &> last-run.log 2>&1
