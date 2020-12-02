#!/bin/bash 

#cd /home/pi/projects/rpi-controller
#piserver='10.5.5.26'
#python /home/pi/projects/sbda-controller/py/modules/i2cbridge.py > i2cbridge_log.txt 2>&1 

# output redirect is necessary to avoid connection unexpected drops
#python /home/pi/projects/sbda-controller/py/modules/i2cbridge.py > /dev/null 2>&1 &
python /home/pi/projects/sbda-controller/py/modules/i2cbridge.py > /home/pi/projects/sbda-controller/i2cserver.log 2>&1 &

