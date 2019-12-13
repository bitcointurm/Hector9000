# hardware configuration
config = {
    "hx711": {
        "CLK": 29,
        "DAT": 31,
        "ref": -2145  # calibration yields 100 g <-> readout 214500
    },
    "pca9685": {
        "freq": 60,
        "valvechannels": range(24),  # 0..23
        "valvepositions": [  # (open, closed)
            (280, 520),  # ch 0
            (290, 520),  # ch 1
            (280, 520),  # ch 2
            (590, 360),  # ch 3
            (480, 250),  # ch 4
            (480, 240),  # ch 5
            (280, 510),  # ch 6
            (280, 530),  # ch 7
            (490, 250),  # ch 8
            (290, 530),  # ch 9
            (500, 260),  # ch 10
            (330, 550),  # ch 11
            (360, 590),  # ch 12
            (360, 590),  # ch 13
            (330, 570),  # ch 14
            (360, 590),  # ch 15
            (360, 580),  # ch 16
            (360, 580),  # ch 17
            (360, 590),  # ch 18
            (360, 590),  # ch 19
            (360, 580),  # ch 20
            (360, 590),  # ch 21
            (360, 600),  # ch 22
            (360, 590)  # ch 23
        ],
        "fingerchannel": 12,
        "fingerpositions": (280, 440, 465),  # retracted, above bell, bell
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
        "DIN": 18,
        "NUM": 48
    }
}
