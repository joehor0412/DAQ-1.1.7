"""
Module to process all work related to logging
"""

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5 import QtCore
import assets.config as cf
import psutil
import time
import logging

class LogMixin(object):
    @property
    def logger(self):
        name = '.'.join([__name__, self.__class__.__name__])
        return logging.getLogger(name)
        
class Log_Worker(QObject): # Class Thread for logging
    """
    Class Thread for logging
    
    """
    finished = QtCore.pyqtSignal()

    def __init__(self):
        super(Log_Worker, self).__init__()
        self._isRunning = False

    def task(self):
        while True:
            time_tuple = time.struct_time(time.gmtime())
            if time_tuple.tm_min == 0 and time_tuple.tm_sec == 0:
                self.write_log()
            time.sleep(1) #1 hour interval
        self.finished.emit()
    
    def write_log(self):
        log_f = open(cf.log_save_path + str(time.strftime("%Y-%m-%d")) + '_log.txt',"a+")
        data_line = str(time.strftime("%d-%m-%Y %H:%M:%S")) + ',' +  Status.get_memory()  + ',' +  Status.get_total_memory()+ ',' + Status.get_temperature() + ',' + Status.get_cpu() + '\n'
        log_f.write(data_line)
        log_f.close()

    @property
    def logger(self):
        name = '.'.join([__name__, self.__class__.__name__])
        return logging.getLogger(name)
    
class Status():
    def get_time():
        gettime = str(time.strftime("%d-%m-%y %H:%M:%S"))
        return gettime
    
    def get_memory():
        mem = psutil.Process().memory_info().rss
        getmemory = str(round(int(mem)/1000000,0))
        return getmemory
    
    def get_total_memory():
        gettotalmemory = str(psutil.virtual_memory().percent)
        return gettotalmemory

    def get_temperature():
        # !!!! psutil stopped working, keep giving rtc module ds3231 reading !!!!

        # for name, entries in psutil.sensors_temperatures().items():
        #     for entry in entries:
        #         current_temp = entry.current
        #         log_temp = str((round(current_temp,0)))
        
        f = open("/sys/class/thermal/thermal_zone0/temp", "r")
        t = f.readline ()
        cputemp = round(int(t)/1000,0)
        gettemperature = str(cputemp)
        return gettemperature

    def get_cpu():
        getcpu = str(psutil.cpu_percent())
        return getcpu