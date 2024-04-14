# Installion Guide

## 1.  How to setup SSH from CAREACQ to NAS
Detailed guide here: [Configure Synology NAS SSH Key-based authentication](https://blog.aaronlenoir.com/2018/05/06/ssh-into-synology-nas-with-ssh-key/)

### **!Important! Setting up NAS **

Make sure ssh is enabled

Make sure rsync is enabled

Make sure users home folder is enabled

### **Generate an SSH key**
At the DAQ terminal run this command to create SSH key pairs.The result, by default, is some files in the folder <code>~/.shh</code>. Among which your private <code>(id_rsa)</code> and public key <code>(id_rsa.pub)</code>.

    ssh-keygen -t rsa -b 4096 -C "pi@CAREACQ4"

### **Add public key to Authorized keys**
SSH into the NAS again.

On the NAS, you must create a file ~/.ssh/authorized_keys:

    mkdir ~/.ssh
    touch ~/.ssh/authorized_keys

If authorized keys already exists, you can preview it:

    vim ~/.ssh/authorized_keys

* NAS doesn't have nano. Vim (press Esc followed by :wq Enter to exit)

In that file, you must add the contents of your local <code>~/.ssh/id_rsa.pub</code>. SSH then uses this public key to verify that your client machine is in posession of the private key. Then it lets you in.

On client first copy over public key:

    scp ~/.ssh/id_rsa.pub admin@192.168.0.104:/var/services/homes/admin

And then on the NAS SSH session:

    cat ~/id_rsa.pub >> ~/.ssh/authorized_keys
    rm ~/id_rsa.pub

### **SSH into NAS**
Verify that you can ssh into NAS with SSH keys

    ssh -i ~/.ssh/id_rsa admin@192.168.0.104

Make sure <code>id_rsa created</code> just now is in directory <code>~/.ssh/id_rsa</code>.

Change folder permission

    chmod 755 /var/services/homes/admin

If still cant, try:

    chmod 700 ~/.ssh
    chmod 600 ~/.ssh/authorized_keys

## 2. Backup data from DAQ to NAS and Dropbox

### **Rsync com mand to sync data**
Make sure you are able to SSH into NAS using SSH keys first. Test backup using the following codes: *(Change device hostname accordingly.)*

    rsync -ave "ssh -i /home/pi/.ssh/id_rsa -p 22" /home/pi/Serial/data/ admin@carenas.local::datavault/data/$(hostname)

### **Setup cron job to sync hourly**

```
crontab -e
0 * * * * rsync -ave "ssh -i /home/pi/.ssh/id_rsa -p 22" /home/pi/Serial/data/ admin@carenas.local::datavault/data/$(hostname)
0 * * * * rsync -ave "ssh -i /home/pi/.ssh/id_rsa -p 22" /home/pi/Serial/events/ admin@carenas.local::datavault/events/$(hostname)
0 * * * * rsync -ave "ssh -i /home/pi/.ssh/id_rsa -p 22" /home/pi/Serial/log/ admin@carenas.local::datavault/log/$(hostname)
```

### **Setup cron job to sync to dropbox hourly**
```
0 * * * * python3 /home/pi/Serial/dropbox_sync.py -y >> /home/pi/Serial/logs/dropbox_output.log
```

## 3. Autolaunch program on start (DAQ)

***Autostart command for Raspi:***

```
sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
```

***In autostart file:***
add in last line: 
```
@python3 /home/pi/Serial/launchfile.py
```

lastly reboot daq:
```
sudo reboot
```

## 4. 🔆 Install rpi-backlight (Optional)

Install module to control RPi's official 7 inch touchscreen brightness

Link to page: https://github.com/linusg/rpi-backlight  

<br>

### Installation

---

Install from PyPI:

    $ pip3 install rpi-backlight    

Create this udev rule to update permissions, otherwise you'll have to run Python code, the GUI and CLI as root when changing the power or brightness:

    $ echo 'SUBSYSTEM=="backlight",RUN+="/bin/chmod 666 /sys/class/backlight/%k/brightness /sys/class/backlight/%k/bl_power"' | sudo tee -a /etc/udev/rules.d/backlight-permissions.rules

## Usage

### Python
```
>>> from rpi_backlight import Backlight
>>>
>>> backlight = Backlight()
>>> backlight.brightness
100
>>> backlight.brightness = 50
>>> backlight.brightness
50
```

### CLI
    $ rpi-backlight --set-brightness 20

## GUI
Open a terminal and run `rpi-backlight-gui`.

## 5. Install required modules

Install pypi modules
```
pip3 install -r requirements.txt
```

Install PyQt5
```
sudo apt-get install python3-pyqt5 -y
```

## 6. Setup real time clock (RTC) module
https://pimylifeup.com/raspberry-pi-rtc/
