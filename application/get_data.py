from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5 import QtWidgets, QtCore
import serial
import assets.config as cf
import time
import os
import logging
from scipy import integrate
import numpy as np
import logging
import math

# For the machine learning section
from tensorflow.keras.models import load_model

# Load in the model
Model_DAQ = load_model("/home/pi/Serial/model/Model_DAQ.h5")

class Worker(QObject):
    """
    Class Thread for data acquisition
    
    Parameters
    ----------
    None
    
    Returns
    -------
    Nothing
    """
    sig_msg = pyqtSignal(str)
    RMs_display = pyqtSignal(list)
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
        self.trigger = False # trigger to start loop collect data
        self.patient_number = patient_number
        self.patient_folder_dir = cf.save_path + patient_number + '/' + time.strftime("%Y-%m-%d")
        if not os.path.exists(self.patient_folder_dir):
            os.makedirs(self.patient_folder_dir)
        print('Patient folder path: ' + self.patient_folder_dir)
        self.logger.info('Patient folder path: ' + self.patient_folder_dir)
        try:
            self.ser = serial.Serial(port_number,cf.BAUDrate,timeout=10)
            print("Listening on port:" + port_number)
            self.logger.info("Listening on port:" + port_number)
            self._isRunning = True
        except Exception as e:
            print('error on port', e)
            self.logger.warning('error on port')
            self.signal_error.emit()
            self._isRunning = False

        filename = "patient_" + patient_number + '_' + time.strftime("%Y-%m-%d_%H-00-00") + '.txt' # concat into filename
        self.f = open(self.patient_folder_dir + '/' + filename, "a+")


    def task(self):
        print('WKR thread:', QtCore.QThread.currentThread())
        self.logger.info('WKR thread:' +  str(QtCore.QThread.currentThread()))
         
        while self._isRunning:
            try:
                line = self.ser.readline()
                decoded_line = line.decode()
                # decoded_line = line.encode("UTF-8")
                # decoded_line = line.decode("ISO-8859-1")
                if len(decoded_line) == 0:
                    self.timeout_error.emit()
                    self.stop()
                starttracker = "BS" in decoded_line # finds the breath signal
                if starttracker == True: # breath detected
                    self.trigger = True # set trigger to start collect data
            except Exception as e:
                print('Line88:' + str(e))
                print(line)
                self.stop()
                self.signal_error.emit()
            
            if self.trigger == True: # start collecting data
                BSline = "BS" in decoded_line # finds BS in string
                BEline = "BE" in decoded_line # finds BE in string
                
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
                    # self.sig_msg.emit('BE') # emit signal to output   
                    sck_pressure = self.temp_pressure[:]
                    sck_flow = self.temp_flow[:]
                    self.plot_pressure.emit(sck_pressure) # signal for plotting purpose
                    self.plot_flow.emit(sck_flow) # signal for plotting purpose
                    current_time_milli = str(round(time.time() * 1000))
                    self.stream_msg.emit(current_time_milli,sck_flow,sck_pressure)
                    
                    # Respiratory mechanics calculation
                    try:
                        Ers, Rrs, PEEP, PIP, TidalVolume, IE, VE = self.calc_RM(sck_pressure,sck_flow)
                        mv_mode = self.calc_MV_mode(sck_pressure,sck_flow)      # produce the MV mode
                        self.RMs_display.emit([str(Ers),str(Rrs),mv_mode])
                        # self.RMs_display.emit([str(Ers),str(Rrs),breath_number])
                        timenow = str(time.strftime("%d-%m-%y %H:%M:%S"))
                        # Try save in a text file
                        try:
                            with open("Mechanics.txt", "a+") as f:
                                f.write(f"{timenow} - {breath_number} - {mv_mode} - {Ers},{Rrs},MV mode (PC=0,VC=1)\n")
                        except:
                            pass
                    except:
                        pass

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

    def calc_RM(self, P, Q):
        """ Calculate respiratory mechanics """
        temp_flow = np.array(Q)/60
        temp_pressure = P

        # get maximum pressure pip
        PIP = max(temp_pressure)

        flow_inspi,flow_expi,pressure_inspi,pressure_expi = self._seperate_breath(temp_pressure,temp_flow)
        
        b_points = np.size(pressure_inspi)
        Time = list(np.linspace(0, (b_points-1)*0.02, b_points))

        expi_b_points = np.size(flow_expi)
        expi_Time = list(np.linspace(0, (expi_b_points-1)*0.02, expi_b_points))

        b_points_total = np.size(temp_pressure)
        total_time = list(np.linspace(0, (b_points_total-1)*0.02, b_points_total))
        
        # get PEEP, use expi min as peep
        PEEP = math.floor(min(pressure_expi))
        np_PEEP = np.array(PEEP)  
        
        V = integrate.cumtrapz(flow_inspi, x=Time, initial=0)
        V_expi = integrate.cumtrapz(flow_expi, x=expi_Time, initial=0)
        V_total = integrate.cumtrapz(temp_flow, x=total_time, initial=0)+0.000001

        
        # Using Integral method, reintegrate to reduce noise
        int_V = integrate.cumtrapz(V, x=Time, initial=0)
        int_Q = integrate.cumtrapz(flow_inspi, x=Time, initial=0)
        int_B = integrate.cumtrapz(pressure_inspi-np_PEEP, x=Time, initial=0)
        
        # Constructing Ax=B to obtain Ers and R
        A = np.vstack((int_V, int_Q)).T  # Transpose
        B = int_B

        # linear algebra method to return least square solution
        Ers, Rrs, = np.linalg.lstsq(A, B, rcond=-1)[0]

        # round Ers, Rrs to one decimal point
        Ers = np.around(Ers,1)
        Rrs = np.around(Rrs,1)

        # get other parameters
        TidalVolume = max(V)
        IE = len(flow_expi)/len(flow_inspi)
        VE = abs(min(V_expi))

        # Limit Rrs to zero, remove negative value
        if Rrs < 0:
            Rrs = 0

       

        return Ers, Rrs, PEEP, PIP, TidalVolume, IE, VE

    def resample_array(self, data, new_length):
        """ Reshape the array to be 180 """
        old_indices = np.linspace(0, len(data) - 1, len(data))
        new_indices = np.linspace(0, len(data) - 1, new_length)
        new_data = np.interp(new_indices, old_indices, data)
        return new_data
    
    def calc_MV_mode(self, P, Q):
        """ Obtain the MV mode from the CNN """
        mv_mode = None
        
        print(len(P))
        print(len(Q))
        
        # Have to cut the waveform and resize it to 1x180
        for i in range(len(Q)):
            if Q[i] < 0:
                cutoff_index = i
                break
        
        temp_P = self.resample_array(P[:cutoff_index], 180)
        temp_Q = self.resample_array(Q[:cutoff_index], 180)
        result = Model_DAQ.predict([temp_P, temp_Q])
        
        if result[0] > result[1]:
            mv_mode = 0
        else:
            mv_mode = 1
        
        return mv_mode

    def _seperate_breath(self, temp_pressure, temp_flow):
        """Seperate breath to inspiration and expiration"""
        # add 5 data points in future so that will avoid the 1st digit as negative
        Fth = 5
        flow_inspi_loc_ends = np.argmax(temp_flow[1+Fth:-1] <= 0)
        flow_inspi = temp_flow[0:flow_inspi_loc_ends+Fth]

        while (len(flow_inspi) <= 10):
            # print(len(flow_head))
            # add 5 data points in future so that will avoid the 1st digit as negative
            flow_inspi_loc_ends = np.argmax(temp_flow[1+Fth:-1] <= 0)
            flow_inspi = temp_flow[0:flow_inspi_loc_ends+Fth]
            Fth = Fth + 1

        # add 5 data points in future so that will avoid the 1st digit as negative
        flow_inspi_loc_ends = np.argmax(temp_flow[1+Fth:-1] <= 0)
        flow_inspi = temp_flow[0:flow_inspi_loc_ends+Fth]

        flow_expi = temp_flow[flow_inspi_loc_ends+1+Fth::]
        flow_expi_loc_starts = np.argmin(flow_expi)
        flow_expi = flow_expi[flow_expi_loc_starts::]

        # % Pressure Inspiration and expiration
        pressure_inspi = temp_pressure[0:flow_inspi_loc_ends+Fth]
        pressure_expi = temp_pressure[flow_inspi_loc_ends+1+Fth::]
        # pressure_expi_T = pressure_expi[flow_expi_loc_starts::]

        return flow_inspi,flow_expi,pressure_inspi,pressure_expi

    def stop(self):
        self.finished.emit()
        self._isRunning = False # stop task loop
        self.f.close() # close text file
        self.trigger = False # stop trigger
    
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

