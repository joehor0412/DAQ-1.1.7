import time
import socket

## Device hostname and version info
dev_hostname = socket.gethostname()
version = 'v1.1.7'

## File save path
save_path = '/home/pi/Serial/data/'
log_save_path = '/home/pi/Serial/log/'
event_log_save_path = '/home/pi/Serial/events/'
filename = str(time.strftime("%Y-%m-%d %H:%M:%S")) + '.txt'

## Serial connection params
BAUDrate = 38400

## Socket.IO config
sio_live_addr = 'https://carenetdemo.com'

## Set true to enable live streaming, else false
connect_sio_remote = False
connect_sio_local = False
