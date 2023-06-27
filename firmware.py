import os
import socket
from pathlib import Path
from hidconfig import gadget


def foundConfigElseAdd(setting, configFile):
    """
    Checks if a setting exists and is not commented out in a configuration file. 
    If not, it appends the setting to the end of the file and returns False. Otherwise, it returns True.

    Args:
        setting (str): The setting to search for in the configuration file.
        configFile (str): The path to the configuration file.

    Returns:
        bool: True if the setting is found and is not commented out, False otherwise.
    """
    with open(configFile, 'r') as f:
        found = any(setting in line.split('#', 1)[0].strip() for line in f)

    if not found:
        with open(configFile, 'a') as f:
            f.write(f'\n{setting}\n')

    return found


def overWriteConfigFile(setting, configFile):
    """
    Overwrites a configuration file with a specified setting. The setting could be a string or bytes. 

    Args:
        setting (str or bytes): The setting to be written to the configuration file. Type determines the mode in which the file is opened.
        configFile (str): The path to the configuration file.
    """
    with open(configFile, 'wb' if isinstance(setting, bytes) else 'w') as f:
        f.write(setting)


def checkKernelModules():
    """
    Checks if the required kernel modules 'dtoverlay=dwc2' and 'g_hid' are present and not commented out.
    If not, the missing settings are added, and the system is rebooted to apply the new configurations.
    """
    kernelReady = foundConfigElseAdd('dtoverlay=dwc2', '/boot/config.txt') and foundConfigElseAdd(
        'dwc2', '/etc/modules') and foundConfigElseAdd('g_hid', '/etc/modules')

    if not kernelReady:
        print('Configuration for rquired kernel modules added, rebooting...')
        os.system('reboot')


def setupHidGadget():
    """
    Sets up the HID gadget using the given configuration specified in the 'gadget' dictionary from 'hidconfig.py'.
    The function creates the necessary directories in the '/sys/kernel/config/usb_gadget/' path if they do not already exist.

    Feel free to change the serial number in 'hidconfig.py'. Raspberry pi serial number can be found here:
    cat /sys/firmware/devicetree/base/serial-number
    """
    gadgetPath = Path('/sys/kernel/config/usb_gadget/kbdrelay')
    gadgetPaths = [gadgetPath, gadgetPath.joinpath('strings/0x409'), gadgetPath.joinpath(
        'configs/c.1/strings/0x409'), gadgetPath.joinpath('functions/hid.usb0')]

    if gadgetPath.joinpath('UDC').exists() and gadgetPath.joinpath('UDC').stat().st_size > 0:
        return

    for path in gadgetPaths:
        path.mkdir(parents=True, exist_ok=True)

    for key, value in gadget.items():
        overWriteConfigFile(value, gadgetPath.joinpath(key))

    gadgetPath.joinpath(
        'configs/c.1/hid.usb0').symlink_to(gadgetPath.joinpath('functions/hid.usb0'))

    udc = os.listdir('/sys/class/udc')
    if not len(udc) > 0:
        print('No USB Device Controller found! Terminating...')
        os._exit(1)

    overWriteConfigFile(udc[0], gadgetPath.joinpath('UDC'))


def initialize():
    """
    Initilization of the device. Checks if the required kernel modules are installed, othewise installs and reboots.
    Sets up and activates the USB HID gadget.
    """
    checkKernelModules()
    setupHidGadget()


def start():
    """
    Starts the device.
    """
    initialize()

    HOST = '0.0.0.0'
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        data = []
        with conn:
            print(f"Connected by {addr}")
            with open(u'/dev/hidg0', 'wb+', buffering=0) as hid:
                while True:
                    if data and len(data) == 8:
                        hid.write(data)
                    data = conn.recv(8)
                    if not data:
                        break


start()
