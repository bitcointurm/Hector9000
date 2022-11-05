#!/usr/bin/env python3

import sys
from HectorConfig import config
from HectorHardware import HectorHardware

h = HectorHardware(config)

while True:
    vnum = int(input("Bitte Ventilnr. eingeben (0..23); Ende mit -1:  "))
    if vnum == -1:
        sys.exit()
    cpos = h.fingerPositions[1]
    if vnum < 24:
        cpos = h.valvePositions[vnum][1]
    print("Ventil %d wird geschlossen, Servoposition = %d" % (vnum, cpos))
    while cpos != -1:
        if vnum < 12:
            h.pca.set_pwm(vnum, 0, cpos)
        elif vnum >= 24:
            h.pca.set_pwm(h.fingerChannel, 0, cpos)
        else:
            h.pcaplus.set_pwm(vnum-12, 0, cpos)
        cpos = int(input("Bitte neue Servoposition eingeben:"))


