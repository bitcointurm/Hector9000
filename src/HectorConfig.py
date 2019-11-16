# hardware configuration
config = {
    "hx711": {
        "CLK": 29,
        "DAT": 31,
        "ref": -2145  # calibration yields 100 g <-> readout 214500
    },
    "pca9685": {
        "freq": 60,
        "valvechannels": range(12),  # 0..11
        "valvepositions": [  # (open, closed)
            (280, 520),  # ch 0
            (290, 520),  # ch 1
            (280, 520),  # ch 2
            (590, 380),  # ch 3
            (480, 240),  # ch 4
            (480, 250),  # ch 5
            (280, 520),  # ch 6
            (280, 520),  # ch 7
            (490, 250),  # ch 8
            (290, 520),  # ch 9
            (500, 250),  # ch 10
            (330, 110),  # ch 11
            (375, 250),  # ch 12
            (375, 250),  # ch 13
            (375, 250),  # ch 14
            (375, 250),  # ch 15
            (375, 250),  # ch 16
            (375, 250),  # ch 17
            (375, 250),  # ch 18
            (375, 250),  # ch 19
            (375, 250),  # ch 20
            (375, 250),  # ch 21
            (375, 250),  # ch 22
            (375, 250),  # ch 23
        ],
        "fingerchannel": 24,
        "fingerpositions": (280, 430, 450),  # retracted, above bell, bell
        "lightpin": 22,
        "lightpwmchannel": 13,
        "lightpositions": (0, 500)
    },
    "a4988": {
        "ENABLE": 11,
        "MS1": 13,
        "MS2": 15,
        "MS3": 19,
        "RESET": 21,
        "SLEEP": 23,
        "STEP": 37,
        "DIR": 33,
        "numSteps": 260
    },
    "arm": {
        "SENSE": 16
    },
    "pump": {
        "MOTOR": 18
    },
    "ws2812": {
        "DIN": 12
    }
}
