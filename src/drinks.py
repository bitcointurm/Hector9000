# drinks.py

drink_list = [
    {
        "name": "Bitcoin im Turm",
        "sound": "/home/pi/Music/SatoshiCountry.mp3",
        "image": "img/bitcoinimturm.png",
        "recipe": [
            ("tonic", 150),
            ("gin", 50)
        ]
    }, {
        "name": "Matt Colado",
        "sound": "/home/pi/Music/Vitalik.mp3",
        "image": "img/bluematt.png",
        "recipe": [
            ("rum", 40),
            ("coco", 40),
            ("pineapple", 120)
        ]
    }, {
        "image": "img/honigdachs.png",
        "name": "Nasty Ass\nHoney Badger",
        "sound": "/home/pi/Music/honeybadger.mp3",
        "recipe": [
            ("lime", 10),
            ("coco", 20),
            ("rum", 40),
            ("gin", 80),
            ("cola", 120)
        ]
    },  {
        "name": "Hal Ginny",
        "image": "img/halfinney.png",
        "sound": "/home/pi/Music/CraigNoSplit.mp3",
        "recipe": [
            ("gin", 40),
            ("cola", 80),
            ("soda", 150)
        ]
    }, {
        "name": "Vodka Livera",
        "image": "img/livera.png",
        "sound": "/home/pi/Music/SatoshiCountry.mp3",
        "recipe": [
            ("vodka", 40),
            ("lime", 10),
            ("soda", 150)
        ]
    }, {
        "name": "What Bitcoin Did",
        "image": "img/whatbitcoindid.png",
        "sound": "/home/pi/Music/SatoshiCountry.mp3",
        "recipe": [
            ("rum", 40),
            ("cola", 160)
        ]
    }, {
        "name": "TFTC\nStacking Sats",
        "image": "img/TFTC.png",
        "sound": "/home/pi/Music/SatoshiCountry.mp3",
        "recipe": [
            ("vodka", 40),
            ("lime", 10),
            ("soda", 150)
        ]
    }, {
        "name": "7 tall black women",
        "image": "img/giacomo.png",
        "sound": "/home/pi/Music/Jail20yearsCW.mp3",
        "recipe": [
            ("vodka", 10),
            ("gin", 20),
            ("rum", 10),
            ("cola", 40),
            ("lime", 10),
            ("tonix", 20),
            ("coconut", 20)
        ]
    }, {
        "name": "Sats on the beach",
        "image": "img/empty-glass.png",
        "sound": "/home/pi/Music/SatoshiCountry.mp3",
        "recipe": [
            ("vodka", 40),
            ("grenadine", 40),
            ("pineapple", 80),
            ("tonic", 80)
        ]
    }, {
        "name": "Cuba Libra",
        "image": "img/empty-glass.png",
        "sound": "/home/pi/Music/SatoshiCountry.mp3",
        "recipe": [
            ("rum", 40),
            ("lime", 10),
            ("cola", 150)
        ]
    }, {
        "name": "Bavarian Badger",
        "sound": "/home/pi/Music/TestRaspi.mp3",
        "image": "img/badger.jpg",
        "recipe": [
            ("gin", 40),
            ("grenadine", 20),
            ("lime", 20),
            ("tonic", 100)
        ]
    },{
        "name": "Sh**tcoin's Punch",
        "image": "img/vob.png",
        "sound": "/home/pi/Music/vob.mp3",
        "recipe": [
            ("rum", 40),
            ("pineapple", 80),
            ("lime", 10),
            ("grenadine", 10)       
        ]
    }, {
        "name": "iota",
        "image": "img/empty-glass.png",
        "sound": "/home/pi/Music/SatoshiCountry.mp3",
        "recipe": [
            ("cola", 40),
            ("pineapple", 40),
            ("lime", 30),
            ("grenadine", 10)   
        ]
    }, {
        "name": "...under\nconstruction",
        "image": "img/empty-glass.png",
        "sound": "/home/pi/Music/SatoshiCountry.mp3",
        "recipe": [
        ]
    }, {
        "name": "...under\nconstruction",
        "image": "img/empty-glass.png",
        "sound": "/home/pi/Music/SatoshiCountry.mp3",
        "recipe": [
        ]
    }, {
        "name": "...under\nconstruction",
        "image": "img/empty-glass.png",
        "sound": "/home/pi/Music/SatoshiCountry.mp3",
        "recipe": [
        ]
    }, {
        "name": "...under\nconstruction",
        "image": "img/empty-glass.png",
        "sound": "/home/pi/Music/SatoshiCountry.mp3",
        "recipe": [
        ]
    }

]

# "NAME":("NICENAME", ISWITHALCOHOL)
ingredients = {
    "rum": ("Rum", True),
    "gin": ("Gin", True),
    "vodka": ("Vodka", True),
    "triple": ("Triple", True),
    "grenadine": ("Grenadine", False),
    "coco": ("Coco", False),
    "lemonjuice": ("Lemonjuice", False),
    "pineapple": ("Pineapple", False),
    "tonic": ("Tonic", False),
    "lime": ("Lime", False),
    "soda": ("Soda", True),
    "cola": ("Cola", False),
 #   "tequila": ("tequila", True),
 #   "beer": ("Beer", True),
 #   "water": ("Water", True),
 #   "bacardi": ("Bacardi", True),
}


