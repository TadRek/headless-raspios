# headless-raspios
Autodownload and install script for headless RaspiOS on SD card with WiFi and SSH enabled for Linux.

# Usage
Due to mount and dd usage, script requires root privileges. 

Connect SD card and run script to download latest .IMG of RaspiOS and install it on SD card, enable ssh and configure Wireless Network.

To run simply type 
```bash
sudo ./raspios-sd.py 
```
or 
```bash
sudo python3 raspios-sd.py
```

Linux only, tested on Arch.