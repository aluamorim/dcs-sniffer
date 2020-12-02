
from __future__ import print_function
import sys, traceback
import time

if (sys.version_info.major>=3):
    import _thread as thread
else:
    import thread

import threading
from PyQt5 import QtCore, QtGui
from collections import deque
from modules.entity import *
from modules.entity.controller import *
from modules.connection.i2cnetcomm import *
from modules.connection.serialcomm import *
from modules.definitions import *
from modules.service.service import *

class ADCSamplerService(Service):

    deviceController=None
    running=False
    pause=False

    def __init__(self):
        Service.__init__(self)    

    def run(self):
        self.running = True
        try:
            try:
                self.adcSamplerThread()
            except Exception as e:
                print("Error: " + str(e))
                traceback.print_exc(file=sys.stdout)
        except Exception as e:
            print("Error: " + str(e))
            traceback.print_exc(file=sys.stdout)
        self.running = False

    def adcSamplerThread(self):
        pass