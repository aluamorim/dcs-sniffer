#!/bin/bash

# ::piserver='10.5.5.26'
# SET piserver=192.168.0.198
# ::START /B ssh -X pi@%piserver% "python /home/pi/projects/rpi-controller/modules/i2cbridge.py"
cd py
python app.py
cd ..

# ::ssh -X pi@%piserver% 'killall python'
# ::taskkill /IM cmd.exe


