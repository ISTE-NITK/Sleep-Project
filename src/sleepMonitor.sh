#!/bin/sh
#sleepMonitor.sh
#navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd home/pi/istesleep/src
python sleepMonitor.py
cd /
