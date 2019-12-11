import time 
import board
import neopixel
import sys

PORT = board.D18
NUM = 48
NUM_VALVES = 24


pixels = neopixel.NeoPixel(PORT, NUM)
ch = int(sys.argv[1])
r = int(sys.argv[2])
g = int(sys.argv[3])
b = int(sys.argv[4])

print(ch) # Channel
print(r) # Color R
print(g) # Color G
print(b) # Color B

if ch < NUM_VALVES:
    pixels[ch] = (r,g,b)
    pixels[ch+NUM_VALVES] = (r,g,b)
else: ### 
    pixels.fill((r,g,b))
    
pixels.show()

time.sleep(.1)




