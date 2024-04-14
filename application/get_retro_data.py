from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5 import QtWidgets, QtCore
import serial
import assets.config as cf
import time
import os
import logging

file_path = "/home/pi/Serial/application/patient_P0001_2017-08-30_00-00-00.txt"
folder_path = "/home/pi/Serial/retro/"

class Worker(QObject):
    """

    Class Thread for data acquisition

    """
    sig_msg = pyqtSignal(str)
    stream_msg = pyqtSignal(str,list,list)
    signal_error = pyqtSignal()
    timeout_error = pyqtSignal()
    plot_pressure = pyqtSignal(list)
    plot_flow = pyqtSignal(list)
    finished = pyqtSignal()
    xtime = []
    temp_pressure = []
    temp_flow = []

    def __init__(self,patient_number,port_number,sio):
        super(Worker, self).__init__()
        self._isRunning = True
        self.trigger = True # trigger to start loop collect data
        self.patient_number = patient_number
        self.patient_folder_dir = cf.save_path + patient_number + '/' + time.strftime("%Y-%m-%d")
        if not os.path.exists(self.patient_folder_dir):
            os.makedirs(self.patient_folder_dir)
        print('Patient folder path: ' + self.patient_folder_dir)
        self.logger.info('Patient folder path: ' + self.patient_folder_dir)
        try:
            print("Listening on port:" + port_number)
            self.logger.info("Listening on port:" + port_number)
            self._isRunning = True
        except Exception as e:
            print('error on port', e)
            self.logger.warning('error on port, {}'.format(e))
            self.signal_error.emit()
            self._isRunning = False

        filename = "patient_" + patient_number + '_' + time.strftime("%Y-%m-%d_%H-00-00") + '.txt' # concat into filename
        self.f = open(self.patient_folder_dir + '/' + filename, "a+")


    def task(self):
        print('WKR thread:', QtCore.QThread.currentThread())
        self.logger.info('WKR thread:' +  str(QtCore.QThread.currentThread()))
         
        # while self._isRunning:
        for root,dirs,files in os.walk(folder_path,topdown=True):
            for filename in sorted(files):
                print(filename)
                if filename.endswith(".txt"):
                    with open(os.path.join(root,filename)) as f:
                        while self.trigger:
                            for decoded_line in f:
                                # time.sleep(0.02)
                                BSline = "BS" in decoded_line # finds BS in string
                                BEline = "BE" in decoded_line # finds BE in string
                                if self.trigger == False:
                                    break
                                if BSline == True: # breath start line
                                    breath_time = 0.00 # restart and initiate breath_time of each breath
                                    complete_breath = decoded_line 
                                    decoded_line.strip('\n')
                                    decoded_line = decoded_line.strip('\r\n')
                                    line_num = decoded_line.split(",")
                                    breath_number = line_num[1]
                                    current_time = QtCore.QTime.currentTime().toString()
                                    self.sig_msg.emit('BS,'+ breath_number +', '+ current_time) # emit signal to output
                                    self.temp_pressure = []
                                    self.temp_flow = []

                                elif BEline == True: #breath end line
                                    breath_time = 0.00 # restart and initiate breath_time of each breath
                                    complete_breath += decoded_line
                                    self.f.write(complete_breath) # write into file into new line each data
                                    complete_breath = ""   
                                    sck_pressure = self.temp_pressure[:]
                                    sck_flow = self.temp_flow[:]
                                    # self.plot_pressure.emit(sck_pressure) # signal for plotting purpose
                                    # self.plot_flow.emit(sck_flow) # signal for plotting purpose
                                    current_time_milli = str(round(time.time() * 1000))
                                    # self.stream_msg.emit(current_time_milli,sck_flow,sck_pressure)
                                    
                                else:
                                    breath_time = round(breath_time,2) # round up breath_time
                                    decoded_line = decoded_line.strip('\n')
                                    decoded_line = decoded_line.strip('\r\n')
                                    num = decoded_line.split(",")
                                    try:
                                        if len(num)>1:
                                            numflow = num[0]
                                            numpressure = num[1]
                                        self.temp_pressure.append( float(numpressure) )
                                        self.temp_flow.append(float(numflow))
                                    except:
                                        pass

                                    decoded_line = decoded_line + ', ' + str(breath_time) +"\n"  # strip blank space and new time
                                    complete_breath += decoded_line
                                    breath_time = breath_time + 0.02 # add time after each line
                    #except Exception as e:
                        #print('Line88:' + str(e))
                        #print(line)
                        #self.stop()
                        #self.signal_error.emit()
                    


    def stop(self):
        self.trigger = False # stop trigger
        self.finished.emit()
        self._isRunning = False # stop task loop
        self.f.close() # close text file
    
    def run(self):
        self.trigger = True
        self._isRunning = True

    def save(self):
        self.f.close()
        filename = "patient_" + self.patient_number + '_' + time.strftime("%Y-%m-%d_%H-00-00") + '.txt'
        patient_folder_dir = cf.save_path + self.patient_number + '/' + time.strftime("%Y-%m-%d")
        if not os.path.exists(patient_folder_dir):
            os.makedirs(patient_folder_dir)
        self.f = open(patient_folder_dir + '/' + filename, "a+")

    @property
    def logger(self):
        name = '.'.join([__name__, self.__class__.__name__])
        return logging.getLogger(name)

