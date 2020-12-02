

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


class Service (threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        # self.threadID = threadID
        # self.name = name
        # self.counter = counter

    def pauseService(self):
        pass
    def resumeService(self):
        pass
    def stopService(self):
        pass
    def isRunning(self):
        pass
    def isPaused(self):
        pass


