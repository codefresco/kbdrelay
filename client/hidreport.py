
from client.layout import *


def hidReport(keys):
    report = [0]*8

    for key in keys:
        if key in modifierMap:
            report[0] |= modifierMap[key]
        elif key in keymap:
            for i in range(2, 8):
                if report[i] == 0:
                    report[i] = keymap[key]
                    break

    return bytes(report)
