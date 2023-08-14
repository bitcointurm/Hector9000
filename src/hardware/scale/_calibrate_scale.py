from hx711 import HX711 

hx = HX711(29,31)
hx.set_reading_format("LSB", "MSB")
hx.set_reference_unit_low(-2777)
hx.set_reference_unit_high(-2941)
hx.reset()
hx.tare()

input('Scale set to zero. Place object and press enter.')
#value = hx.get_value(100)
#print(f"Raw Value: {value} --- Weight: {value/hx.REFERENCE_UNIT}")
weight = hx.get_weight(100)
print(f"Weight: {weight}")