# kbdrelay
Relay keyboard events to an HID device over network. This tool connects to an HID capable device connected to another machine via USB (a raspberry pi zero w) and can send keystrokes remotely to the machine. The HID device replicates keys on the receiving machine as if it was a regular keyboard attached to it via the usb port.

## ⚠️ Disclaimer

This software is provided for educational purposes and legitimate use cases only. It is the responsibility of the end user to comply with all applicable laws, regulations, and ethical guidelines when using this software. 

The authors, contributors, or any associated parties of this project are not responsible for any illegal actions taken by those who choose to use this software. Use of this software for malicious activities, such as hacking, unauthorized access, damage, or theft of data, is strictly prohibited and not the intent of this project. 

By choosing to use this software, you acknowledge that you understand and agree to these terms, and that any unlawful use of this software will be solely at your own risk. Any actions and or activities related to the material contained within this software is solely your responsibility. Misuse of the information in this software can result in criminal charges brought against the persons in question. 

## How it works

There is a client and a firmware.
  - The firmware is meant to be installed on the HID device connected to the receiving machine. Current version works on a raspberry pi zero, but can be modified for other OTG capable devices.
  - The client runs on the sending machine (ie. a laptop) and can connect and send keystrokes to the HID device which would then enter them into the receiving machine as if it was a normal keyboard.

### Firmware
Create a raspberry pi zero headless image with Wifi connection and run `firmware.py` on it. The easiest way is to set is as a systemd service so it runs automatically on boot up, this way you would not need to ssh into the rpi each time to run the receiver code.

Connect the pi zero to the receiving machine via USB port, it will be recognised as a `Generic HID keyboard`. Keep in mind this would not show anything on the machine and it just silently happens, so if nothing happened after connecting, it does not necessarily mean it did not work.

### Client
Install dependencies from `requirements.txt` and run `sender.py` on the client machine (python 3.9+), enter an `address:port` for the HID device and connect. Any keystroke on the client window happens on the receiving machine.

![alt text](https://raw.githubusercontent.com/codefresco/kbdrelay/main/assets/shot.png)


