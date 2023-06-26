gadget = {
    'idVendor': '0x1209',    # Generic
    'idProduct': '0x0010',   # Test device
    'bcdDevice': '0x0100',   # v1.0.0
    'bcdUSB': '0x0200',      # USB2
    # find raspberry pi serial here: cat /sys/firmware/devicetree/base/serial-number
    'strings/0x409/serialnumber': '000000001ab1cd12',
    'strings/0x409/manufacturer': 'codefresco',
    'strings/0x409/product': 'HID Compliant USB Device',
    'configs/c.1/strings/0x409/configuration': 'Config 1: USB HID Keyboard',
    'configs/c.1/MaxPower': '250',
    'functions/hid.usb0/protocol': '1',
    'functions/hid.usb0/subclass': '1',
    'functions/hid.usb0/report_length': '8',
    'functions/hid.usb0/report_desc': b'\x05\x01\x09\x06\xa1\x01\x05\x07\x19\xe0\x29\xe7\x15\x00\x25\x01\x75\x01\x95\x08\x81\x02\x95\x01\x75\x08\x81\x03\x95\x05\x75\x01\x05\x08\x19\x01\x29\x05\x91\x02\x95\x01\x75\x03\x91\x03\x95\x06\x75\x08\x15\x00\x25\x65\x05\x07\x19\x00\x29\x65\x81\x00\xc0',
}
