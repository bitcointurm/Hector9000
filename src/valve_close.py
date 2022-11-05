#!/usr/bin/env python3

import sys, time
from hardware.HectorConfig import config
from hardware.HectorHardware import HectorHardware

hardware = True

if hardware:
    h = HectorHardware(config)

print("VENTILE SCHLIESSEN")
print("")

if hardware:
    h.light_on()
    time.sleep(0.2)
    h.arm_in()

    h.pump_stop()
    for vnum in range(0,24):
            print("Ventil %d wird geschlossen" % (vnum,))
            time.sleep(0.2)
            h.valve_close(vnum)

h.light_off()

print("fertig.")


