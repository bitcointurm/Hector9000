import board

import neopixel

pixels = neopixel.NeoPixel(board.D18, 20)

#12V: rot blau grün

pixels.fill((0, 0, 0))
pixels[6] = (0, 33, 0)
pixels[2] = (180, 0, 0)
#pixels[8] = (0, 0, 255)
