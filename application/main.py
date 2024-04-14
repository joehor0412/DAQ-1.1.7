from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QObject, pyqtSignal, QThread
from PyQt5 import QtWidgets, QtCore
import serial.tools.list_ports
from datetime import date
import pyqtgraph as pg
import numpy as np
import socketio
import logging
import serial
import socket
import time
import os
import sys
import warnings
import websocket

"""
Import self created package
"""
from assets.gui.mainwindow import *
import assets.config as cf
from logclass import *
from retry_util import RetryException, retry_func
from functools import partial

"""
Get arguments when launching application

Usage:
 -r: Retrospective mode
 -d: Demo mode
"""
retro_mode = False
demo_mode = False

opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

if "-r" in opts:
    print("Operating mode: Retrospective")
    retro_mode = True
    from get_retro_data import Worker # get data from retrosepctive text file

elif "-d" in opts:
    print("Operating mode: Demo")
    demo_mode = True
    from get_data import Worker # get data from serial port

else:
    print("Operating mode: Normal")
    from get_data import Worker # get data from serial port


"""
SocketIO related settings
"""
sio = socketio.Client()
sio_local = socketio.Client()
hostname = socket.gethostname()
rpi_namespace = '/' + hostname

device_status = 'disconnected'
sio_connected = False
sio_local_connected = False


@sio.event
def connect(namespace=rpi_namespace):
    global device_status
    print("Sio connected!")
    window.stream_label_remote.setText(" Connected!")
    device_status = 'connected'
    sio_connected = True


@sio.event
def connect_error(message):
    print(f"The connection failed!:{message}")
    window.stream_label_remote.setText(" Connection failed!")

@sio.event
def disconnect():
    global device_status
    print("Live disconnected!")
    device_status = 'disconnected'
    window.stream_label_remote.setText(" Disconnected!")

@sio.event
def check_daq_status():
    global device_status
    # print('Server req DAQ status ')
    sio.emit('my_status_return', {'name':hostname,'status': device_status})

@sio_local.event
def check_daq_status():
    global device_status
    # print('Server req DAQ status ')
    sio_local.emit('my_status_return', {'name':hostname,'status': device_status})

@sio_local.event
def connect_error(message):
    print(f"The connection failed!:{message}")
    window.stream_label_local.setText(" Connection failed!")

@sio_local.event
def connect(namespace=rpi_namespace):
    print("Sio local connected!")
    window.stream_label_local.setText(" Connected!")
    sio_local_connected = True

@sio_local.event
def disconnect():
    print("Local disconnected!")
    global device_status
    device_status = "disconnected"
    window.stream_label_local.setText(" Disconnected!")


class MyApp(QMainWindow,Ui_Main,LogMixin):
    pressure_buffer = []
    flow_buffer = []
    y = np.empty(400) * np.NaN
    y2 = np.empty(400) * np.NaN
    x = np.linspace(0,8,400)
    plot_exist = False
    update_speed = 25
    


    def __init__(self):
        QMainWindow.__init__(self)
        Ui_Main.__init__(self) # load Ui file 
        if retro_mode:
            Ui_Main.display_retro(self)
        if demo_mode:
            Ui_Main.display_demo(self)
        self.logger.info('App started')
    
    def connect_stream_server(self):
        if not sio_local_connected:
            if cf.connect_sio_local:
                try:
                    sio_local.connect(cf.sio_local_addr, namespaces=[rpi_namespace])
                except Exception as e:
                    
                    print(e)
        if not sio_connected:
            if cf.connect_sio_remote:
                try:
                    sio.connect(cf.sio_live_addr, namespaces=[rpi_namespace])
                    
                except socketio.exceptions.ConnectionError as err:
                    self.logger.warning("ConnectionError: "+ str(err))
                    print("ConnectionError: ", err)
                else:
                    self.connected = True
        

    def savedata(self):
        print("saving data...")
        self.logger.info("Saving data into file")
        self.worker.stop()
        self.thread.quit()
        self.thread.wait()
        self.worker.save()
        self.logger.info("Done saving. Restarting recording.")
        self.start_recording()


    def update_device_info(self):
        self.time_label.setText(Status.get_time())
        self.memory_label.setText(Status.get_memory()+ ' MB / ' + Status.get_total_memory() + ' %')
        self.temperature_label.setText(Status.get_temperature() + ' °C')
        self.cpu_label.setText(Status.get_cpu() + ' %')
    

    def control_start_stop(self):
        button = self.sender().text()
        if button == "Start":
            self.patient_number = self.patient_button.text()
            if self.patient_number == "":
                dialog_resp = confirm(styleoptions['patient_num_reminder_window'],self.centralwidget)
            else:
                self.startthread()
        else:
            self.stop_recording()


    def startthread(self):
        if retro_mode:
            self.port_number = "retro"
        else:
            self.port_number = self.check_serial_port() # get connected port number

        if self.port_number == False: 
            # check port failed, return error window
            self.portErrorHandler()
        else: 
            # check port passed, proceed to start recording
            self.startbtn.setText("Stop")
            self.startbtn.setStyleSheet("QPushButton:pressed#startbtn{background-color:#662429} QPushButton:disabled#startbtn{background-color:#D5B4B6} QPushButton#startbtn{background-color: #d9534f;color: white;font-weight:bold;border: 1px solid #8f8f91;border-radius: 6px;}")
            self.start_recording()
            self.log_thread.start()
            self.patient_button.setEnabled(False)
            self.plotgraph()

        print('GUI thread:', QtCore.QThread.currentThread())
        print('Patient number: ' + self.patient_number)
        print("Port connected: " + str(self.port_number))
        self.logger.info('Recording thread started')
        self.logger.info('GUI thread:'+  str(QtCore.QThread.currentThread()))
        self.logger.info('Patient number: ' + self.patient_number)
        self.logger.info("Port connected: " + str(self.port_number))
        

    def start_recording(self):
        self.thread = QtCore.QThread()
        self.worker = Worker(self.patient_number,self.port_number,sio)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.task)
        self.worker.finished.connect(self.thread.quit)
        self.worker.sig_msg.connect(self.label.setText)
        self.worker.stream_msg.connect(self.stream_data)
        self.worker.signal_error.connect(self.signalErrorHandler)
        self.worker.timeout_error.connect(self.timeoutErrorHandler)
        self.worker.plot_pressure.connect(self.update_pressure)
        self.worker.plot_flow.connect(self.update_flow)
        self.worker.RMs_display.connect(self.display_RMs)
        self.thread.start()
        self.save_timer.start()
        self.label.setStyleSheet("background-color: #00ff00")


    def display_RMs(self,data):
        """ Display RMs info on GUI. """
        self.stream_label_remote.setText(data[0])
        self.stream_label_local.setText(data[1])
        
        
    

    def stop_recording(self):
        self.startbtn.setEnabled(False)
        dialog_resp = two_option_dialog(styleoptions['stop_recording_window'],self.centralwidget)
        self.startbtn.setEnabled(True)
        if dialog_resp:
            self.stopthread()
            

    def check_serial_port(self):
        try:
            port_list = []
            for port in serial.tools.list_ports.comports():
                if 'ACM' in str(port.device):
                    port_list.append(port.device)
                elif 'USB' in str(port.device):
                    port_list.append(port.device)
            return port_list[0]
        except Exception as e:
            print("Serial port error: ", e)
            self.logger.warning("no signal from serial port" + str(e))
            return False

    

    def stopthread(self):
        global device_status
        self.logger.info("Recording thread stopped")
        self.worker.stop()
        self.update_timer.stop()
        self.pressure_buffer = []
        self.flow_buffer = []
        self.thread.wait()
        self.patient_button.setEnabled(True)
        self.label.setStyleSheet("background-color: #dddde4")
        self.save_timer.stop()
        self.startbtn.setText("Start")
        self.startbtn.setStyleSheet("QPushButton:pressed#startbtn{background-color:#2F6643} QPushButton:disabled#startbtn{background-color:#ACD3BA} QPushButton#startbtn{background-color: #499F68;color: white;font-weight:bold;border: 1px solid #8f8f91;border-radius: 6px;}")
        self.stream_label_remote.setText("__._")
        self.stream_label_local.setText("__._")
        device_status = "connected"


    def update_pressure(self,data):
        self.pressure_buffer.extend(data)


    def update_flow(self,data):
        self.flow_buffer.extend(data)


    def plotgraph(self):
        if self.plot_exist is False:
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore', 'All-NaN axis encountered')
                warnings.filterwarnings('ignore', 'All-NaN slice encountered')
                self.pressure_curve = self.pressure_plot.plot(self.x,self.y,connect="finite", pen=pg.mkPen('g', width=2))
                self.flow_curve = self.flow_plot.plot(self.x,self.y,connect="finite", pen=pg.mkPen('g', width=2))
            self.plot_exist = True
            self.plot_timer = QtCore.QTimer() # timer to delay plot
            self.plot_timer.setInterval(50) 
            self.plot_timer.timeout.connect(self.startloop)
            self.plot_timer.setSingleShot(True)
            self.plot_timer.start()
            self.c = 1
        else:
            self.y=np.empty(400) * np.NaN
            self.y2=np.empty(400) * np.NaN
            self.update_timer.start()
            self.c = 1


    def startloop(self):
        self.update_timer = QtCore.QTimer() # timer to save data
        self.update_timer.setInterval(self.update_speed) #10 minutes interval
        self.update_timer.timeout.connect(self.updategraphdata)
        self.update_timer.start()


    def updategraphdata(self):

        # Append new pressure values to buffer
        if len(self.pressure_buffer)>1:
            new_point = self.pressure_buffer[1]
            self.y[self.c] = new_point
            self.y[self.c+1:self.c+10] = np.NaN
            self.pressure_buffer.pop(1)
            self.pressure_curve.setData(self.x,self.y)
            self.c += 1
            if self.c > 390:
                self.c = 1
        
        # Append new flow values to buffer
        if len(self.flow_buffer)>1:
            new_point_y = self.flow_buffer[1]
            self.y2[self.c] = new_point_y
            self.y2[self.c+1:self.c+10] = np.NaN
            self.flow_buffer.pop(1)
            self.flow_curve.setData(self.x,self.y2)

        buffer_size = sys.getsizeof(self.pressure_buffer)

        if buffer_size > 2000:
            self.update_speed = 10
        elif buffer_size < 80:
            self.update_speed = 25
        else:
            self.update_speed = -0.0078125*buffer_size + 25.625
        #self.speed_label.setText(str(self.update_speed))

        self.update_timer.setInterval(self.update_speed)
        

    def stream_data(self,current_time,sck_flow,sck_pressure):
        send_dict = {
                'patient_num':self.patient_number,
                'rpi_time':current_time,
                'rpi_date': date.today().strftime("%Y-%m-%d"),
                'flow':sck_flow,
                'pressure':sck_pressure
                }
        if cf.connect_sio_local:
            try:
                sio_local.emit('my_plot_event',send_dict, namespace=rpi_namespace)
            except Exception as e:
                self.logger.warning('Sio warning: ',str(e))
                print(e)
        if cf.connect_sio_remote:
            try:
                global device_status
                sio.emit('my_plot_event',send_dict, namespace=rpi_namespace)
                device_status = "streaming"
            except Exception as e:
                self.logger.warning('Sio warning: ',str(e))
                device_status = "disconnected"
                print(e)


    def open_numpad(self):
        from assets.gui.dialog.numpaddialog import Numpad_New
        self.centralwidget.setEnabled(False)
        dialog = Numpad_New(self)
        if dialog.exec_() == QtGui.QDialog.Accepted:
            dlg_resp = dialog.text
            input_patient_folder_dir = cf.save_path + dlg_resp 
            if not os.path.exists(input_patient_folder_dir):
                self.patient_button.setText(dlg_resp)
            else:
                # disp dialog, warn already exists patient number, if yes accept set pat_no, if no return to numpad
                dialog_resp = two_option_dialog_custom(styleoptions['patient_num_repeated_err_window'],dlg_resp,self)
                if dialog_resp == True:
                    self.patient_button.setText(dlg_resp)
                else:
                    self.open_numpad()
            self.centralwidget.setEnabled(True)
        else:
            self.centralwidget.setEnabled(True)




    '''
    Error handler function
    '''

    def portErrorHandler(self):
        print('no serial connected. not starting recording thread')
        self.startbtn.setEnabled(False)
        self.logger.warning("no signal from serial port")
        dialog_resp = timed_dialog( styleoptions['dialog_window'],self.centralwidget)
        if dialog_resp:
            try:
                retry_func(partial(self.startthread), max_retry=3)
            except RetryException as e:
                print(e)
        else:
            self.startbtn.setEnabled(True)
            self.patient_button.setEnabled(True)
            self.startbtn.setText("Start")
            self.startbtn.setStyleSheet("QPushButton:pressed#startbtn{background-color:#2F6643} QPushButton:disabled#startbtn{background-color:#ACD3BA} QPushButton#startbtn{background-color: #499F68;color: white;font-weight:bold;border: 1px solid #8f8f91;border-radius: 6px;}")


    def signalErrorHandler(self):
        print('signal error handler')
        self.logger.warning("no signal from serial port")
        dialog_resp = timed_dialog( styleoptions['serial_err_window'],self.centralwidget)
        if dialog_resp:
            try:
                self.stopthread()
                self.update_timer.stop()
                try:
                    retry_func(partial(self.startthread), max_retry=3)
                except RetryException as e:
                    print(e)
            except:
                pass
        else:
            self.stopthread()
            self.update_timer.stop()


    def timeoutErrorHandler(self):
        print('timeout error handler')
        self.logger.warning("Timeout error: Serial port connected but no signal")
        dialog_resp = timed_dialog( styleoptions['timeout_err_window'],self.centralwidget)
        if dialog_resp:
            try:
                self.stopthread()
                self.update_timer.stop()
                try:
                    retry_func(partial(self.startthread), max_retry=3)
                except RetryException as e:
                    self.logger.warning(f'Timeout error warning: {e}')
            except:
                pass
        else:
            self.stopthread()
            self.update_timer.stop()


    def exit_app(self):
        self.centralwidget.setEnabled(False)
        dialog_resp = two_option_dialog(styleoptions['exit_window'],self)
        if dialog_resp:
            import os
            os._exit(0)
        else:
            self.centralwidget.setEnabled(True)




if __name__ == '__main__':
    log_name = cf.event_log_save_path + str(time.strftime("%Y-%m-%d")) + '_events.log'
    logging.basicConfig(level=logging.INFO, filename=log_name, filemode='a+',
                        format='%(asctime)s - %(name)s %(levelname)s %(message)s')
    logging.getLogger('engineio.client').setLevel(logging.ERROR)
    logging.getLogger('socketio.client').setLevel(logging.ERROR)
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MyApp()
    window.show()
    MyApp().connect_stream_server()
    sys.exit(app.exec_())