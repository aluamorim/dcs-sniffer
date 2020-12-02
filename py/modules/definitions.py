

import sys
import time
import datetime
import random

REMOTE_SERVER_SCRIPT_PATH = "/home/pi/projects/sbda-controller/runI2Cserver.sh"

# ADC SAMPLE PARAMETERS
ADC_FREQ_RESOLUTION_HZ = 62 # each fft k is 16KHz
ADC_SAMPLE_FREQ = 128000.0
ADC_WINDOW_SIZE = 1280.0 # corresponds to 10ms of signal (128ks/s)
ADC_PACKAGE_SAMPLES = 2048 # 16ms
ADC_PACKAGE_SIZE = (ADC_PACKAGE_SAMPLES*4 + 4) # bytes

ADC_IDLE = 0
ADC_BUSY = 1,
ADC_READY = 2

HK_PACKAGE_SIZE = 18
HK_TIME_TAG_START = 10  # starts at byte 10
HK_TIME_TAG_LENGTH = 8

HK_CFG_WORD_SIZE				= 0x02 # in bytes
HK_CFG_RTC						= 0x0001
HK_CFG_CURRENT_SENSORS			= 0x0002
HK_CFG_ADC_RMS_SAMPLE			= 0x0004
HK_CFG_PLL_SYNC_BIT				= 0x0008
HK_CFG_OVER_CURRENT				= 0x0010

DEFAULT_CMD_SIZE = 12
PTT_PACKAGE_SIZE = 54
PTT_TIME_TAG_START = 13  # starts at byte 9
PTT_TIME_TAG_LENGTH = 8
PTT_SENSOR_DATA_START = 21
PTT_SENSOR_DATA_LENGTH = 31

PTT_DATA_BUFFER_SIZE = 16 #Max number of PCD records the

# PACKAGE TYPES
ACK_PCKG_ID = 0x10
PTT_PCKG_ID = 0x1A
ADC_PCKG_ID	= 0x1B
HK_PCKG_ID  = 0x1C
NO_PCKG_ID = 0xFE

## COMMAND ID CODES
NONE = 0
RTC_SET=1
RTC_PAUSE=2
RTC_RESUME=3
RTC_RESET=4
HK_CONFIG=5
PTT_POP=6
PTT_AVAILABLE=7
PTT_PAUSE=8
PTT_RESUME=9
PTT_ISPAUSED=10
PTT_RESET = 18

ADC_LOAD = 11
ADC_STATE = 12
ADC_RESET = 13

CMD_SET_CONFIG_MODE = 14
CMD_SET_PTT_MODE = 15
CMD_SET_HK_MODE = 16
CMD_SET_ADC_MODE = 17
ECHO=0xFA
EXIT = -1

def calcCRC(message):

	CRC7_POLY = 0x91;
	crc = 0x00
	for i in range(0, len(message)):
		crc ^= message[i]
		for j in range(0,8):
			if (crc & 1):
				crc ^= CRC7_POLY
			crc>>=1
	return crc
