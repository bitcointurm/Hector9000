import time 
import board
import neopixel
import sys

PORT = board.D18
NUM = 48

pixels = neopixel.NeoPixel(PORT, NUM)


print sys.argv[0] # prints NeoPixelAPI.py
print sys.argv[1] # Channel
print sys.argv[2] # Color R
print sys.argv[3] # Color G
print sys.argv[4] # Color B

if (sys.argv[1] < NUM):
    pixels[sys.argv[1]] = (sys.argv[2],sys.argv[3],sys.argv[4])
else:
    pixels.fill(0,0,0)
    
pixels.show()

time.sleep(.1)




