import time
import json
#from database import Database
from drinks import drink_list, ingredients
from functools import partial
from kivy.clock import Clock
from kivy.core.text import Label
from kivy.logger import Logger
from kivy.properties import StringProperty, ListProperty
from kivy.uix.progressbar import ProgressBar
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.image import Image
from hardware.HectorConfig import config
from hardware.HectorHardware import HectorHardware
from payment import payments
from pygame import mixer


## Für LND-Script (if file exists)
from pathlib import Path
import subprocess
#import payments
	
## logging
#import logging
#log_format = "%(asctime)s::%(levelname)s::%(name)s::"\
#                     "%(filename)s::%(lineno)d::%(message)s"
#log_format = "%(asctime)s:%(levelname)s:%(message)s"
#logging.basicConfig(filename="/home/pi/log/cocktail.log", filemode='w', level=logging.DEBUG, format=log_format)  ###TODO: put log location into config

class MainPanel(Screen):
    buttonText = ListProperty([StringProperty(),
                               StringProperty(),
                               StringProperty(),
                               StringProperty(),
                               StringProperty(),
                               StringProperty(),
                               StringProperty(),
                               StringProperty()])

    image = ListProperty([StringProperty(),
                               StringProperty(),
                               StringProperty(),
                               StringProperty(),
                               StringProperty(),
                               StringProperty(),
                               StringProperty(),
                               StringProperty()])

    buttonColor = ListProperty([ListProperty(),
                                ListProperty(),
                                ListProperty(),
                                ListProperty(),
                                ListProperty(),
                                ListProperty(),
                                ListProperty(),
                                ListProperty()])

    #db = None
    drinkOnScreen = None
    screenPage = None
    maxScreenPage = None
    lightning = True
#    lightning = False
    payment_hash = None
    event = None
    timer = 0
    balance = 0
    #logging.debug("variables set")

    def __init__(self, **kwargs):
        super(MainPanel, self).__init__(**kwargs)

        #self.db = Database("h9k")
        #self.db.createIfNotExists()

        self.screenPage = 1

        items = len(drink_list) % 8
        self.maxScreenPage = (len(drink_list) // 8)

        if items > 0:
            self.maxScreenPage += 1

        self.drinkOnScreen = list()
        self.drinkOnScreen = drink_list[:8]
        
        self.fillButtons(self.drinkOnScreen)
        self.initVent()
        #self.balance = payments.get_balance()
        
    def lightningSwitch(self):
        root = BoxLayout(orientation='vertical')
        
        root2 = BoxLayout()
        root2.add_widget(
        Label(text='Do you want to get connected to a lightning node?\n\n Choose wisely,\n because this panel\n can be used once only!', font_size='30sp'))
        root.add_widget(root2)
        
        lightningBIT = Button(text='Bitcoin im Turm-Node (inactive)', font_size=30, size_hint_y=0.15)
        root.add_widget(lightningBIT)
        lightningLAN = Button(text='esotronic.net-LAN-Node', font_size=30, size_hint_y=0.15)
        root.add_widget(lightningLAN)
        lightningOFF = Button(text='OFF', font_size=30, size_hint_y=0.15)
        root.add_widget(lightningOFF)
        
        popup = Popup(title="Lightning configuration", content=root,
                      auto_dismiss=False)

        def lnd_off(button):
            self.lightning =  False
            popup.dismiss()

        def lnd_on(button):
            self.lightning =  True
            popup.dismiss()

        lightningOFF.bind(on_press=lnd_off)
        lightningLAN.bind(on_press=lnd_on)
        lightningBIT.bind(on_press=lnd_on)
        
        popup.open()

    def initVent(self):
        print("Prepare vets.")
        h = HectorHardware(config)
        h.light_on()
        time.sleep(1)
        h.arm_in()

        h.pump_stop()
        for vnum in range(24):
            print("Vent %d closing..." % (vnum,))
            time.sleep(0.1)
            h.pixel_on(vnum)
            h.valve_close(vnum)
        h.light_off()
        h.pixel_off()

    def isalcoholic(self, drink):
        for ing, _ in drink["recipe"]:
            if ingredients[ing][1]: return True
        return False

    def fillButtons(self, drinks):
        countDrinksOnScreen = len(drinks)
        count = 0
        while count < countDrinksOnScreen:
            self.buttonText[count] = drinks[count]['name']
            self.image[count] = drinks[count]['image']
            if self.buttonText[count].startswith("..."):
                self.buttonColor[count] = [.3, .3, .3, 1]
            elif self.isalcoholic(drinks[count]):
                self.buttonColor[count] = [1, 0, 0, 1]
            else: # non-alcoholic
                self.buttonColor[count] = [0, 1, 0, 1]
            count += 1

        while count < 8:
            self.buttonText[count] = ''
            self.buttonColor[count] = [1, 1, 1, 1]
            count += 1

    def choiceDrink(self, drink):
        self.readPumpConfiguration()
        if len(self.drinkOnScreen) -1 < drink:
            print("no drinks found.")
            return
        
        print("Lightning:" + str(self.lightning))

        if self.lightning:
            print("Start creating Invoice")
            self.balance = payments.get_balance()
            print(self.balance)
            # payment_hash identifies the invoice so we can check the paymentstatus later
            #self.payment_hash = payments.invoice_to_qr()
            print("Invoice created")

        root = BoxLayout(orientation='vertical')
        root2 = BoxLayout()
        
        if self.lightning:
            #root2.add_widget(Image(source='test_img.png'))
            root2.add_widget(Image(source='payment/lnurl.png'))
        else:
            root2.add_widget(Image(source='img/empty-glass.png'))
            
        list_ing = "Ingredients:\n"
        for ing in self.drinkOnScreen[drink]["recipe"]:
            list_ing = list_ing + ingredients[ing[0]][0] + ": " + str(ing[1]) + "\n"
            
        root2.add_widget(
            Label(text=list_ing + '\nPlease be sure\nthat a glass with min 200 ml \nis placed onto the black fixture.', font_size='20sp'))
        root.add_widget(root2)

        root3 = BoxLayout(size_hint_y=0.15)
        if not self.lightning:
            contentOK = Button(text='OK', font_size=60)
            root3.add_widget(contentOK)

        contentCancel = Button(text='Cancel', font_size=60)
        root3.add_widget(contentCancel)
        
        root.add_widget(root3)

        popup = Popup(title=self.drinkOnScreen[drink]["name"], content=root,
                      auto_dismiss=False)

        #logging.debug(self.drinkOnScreen[drink]["name"])
        #Logger.info(f"Cocktail: {self.drinkOnScreen[drink]['name']}")

        def close_popup_and_give_drink(button):
            popup.dismiss()
            Clock.schedule_once(partial(self.doGiveDrink, drink), .01)
            if self.lightning:
                self.event.cancel()

        def close_popup_without_drink(button):
            popup.dismiss()
            if self.lightning:
                self.event.cancel()

        contentCancel.bind(on_press=close_popup_without_drink)
        if not self.lightning:
            contentOK.bind(on_press=close_popup_and_give_drink)

        def start_payment_check(parent):
            self.event = Clock.schedule_interval(partial(checkPayment, parent), 1)

        def checkPayment(parent, interval_time):
            print("Check paymentstatus")
            #invoice_was_paid = payments.is_invoice_paid(self.payment_hash)["paid"]
            invoice_was_paid = payments.is_invoice_paid_2(self.balance)
            self.timer += 1
            if invoice_was_paid:
                print("paid - Yiihaaaa")
                popup.dismiss()
                Clock.schedule_once(partial(self.doGiveDrink, drink), .1)
                self.event.cancel()
            elif (self.timer > 60):
                popup.dismiss()
                Clock.schedule_once( partial( self.doGiveDrink, drink), .1 )
                self.event.cancel()
                self.timer = 0
            else:
                time.sleep(1)
                print("not paid")
            print("End checking paymentstatus")

        if self.lightning:
            popup.bind(on_open=start_payment_check)

        popup.open()

    def doGiveDrink(self, drink, intervaltime):
        root = BoxLayout(orientation='vertical')
        content = Label(text='Take a break -- \nYour \n\n' + self.drinkOnScreen[drink]["name"]+'\n\nwill be mixed.', font_size='40sp')
        root.add_widget(content)
        popup = Popup(title='Life, the Universe, and Everything. There is an answer.', content=root, auto_dismiss=False)

        if (self.drinkOnScreen[drink]["sound"]):
            mixer.init()
            mixer.music.load(self.drinkOnScreen[drink]["sound"])
            mixer.music.play()
            mixer.music.fadeout(60000)


        def makeDrink(parentwindow):
            drinks = self.drinkOnScreen[drink]

            hector = HectorHardware(config)
            hector.light_on()
            time.sleep(1)
            hector.arm_out()
            Logger.info(f"Cocktail: {drinks['name']}")

            for ingredient in drinks["recipe"]:
                hector.valve_dose(pumpList[ingredient[0]], ingredient[1])
                time.sleep(.1)
                print("IndexPumpe: ", pumpList[ingredient[0]])
                print("Ingredient: ", ingredient[0])
                print("Output in ml: ", ingredient[1])
                #self.db.countUpIngredient(ingredient[0],ingredient[1])
                Logger.info(f"Ingredients: {ingredient[0]} - {ingredient[1]}")

            time.sleep(1)
            #self.db.countUpDrink(drinks["name"])
            hector.arm_in()
            hector.light_off()
            hector.finger(1)
            hector.ping(3)
            hector.finger(0)
            print(drinks["name"])
            parentwindow.dismiss()

        popup.bind(on_open=makeDrink)

        popup.open()
        

    def back(self):
        if self.screenPage == 1:
            self.screenPage = self.maxScreenPage
        else:
            self.screenPage -= 1

        self.drinkOnScreen = drink_list[(self.screenPage * 8) - 8:8 * self.screenPage]
        self.fillButtons(self.drinkOnScreen)

    def forward(self):
        if self.screenPage == self.maxScreenPage:
            self.screenPage = 1
        else:
            self.screenPage += 1
        i = (self.screenPage * 8) - 8
        self.drinkOnScreen = drink_list[i:8 * self.screenPage]
        self.fillButtons(self.drinkOnScreen)

    def readPumpConfiguration(self):
        #servo_config = json.load(open('servo_config.json'))
        #global pumpList
        #pumpList = {}
        #for servo in servo_config:
        #    pumpList = servo[['value']] = servo['channel']
        #return pumpList

        x = json.load(open('hardware/servo_config.json'))
        global pumpList
        pumpList = {}
        for key in x:
            chan = x[key]
            pumpList[chan['value']] = chan['channel']

        return pumpList
