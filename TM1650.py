import os
import random
import time
import sys
import random
import keyboard
import threading

I2C_BUS = 3

TM1650_DISPLAY_BASE = 0x34
TM1650_DCTRL_BASE = 0x24
TM1650_NUM_DIGITS = 16
TM1650_MAX_STRING = 128
TM1650_BIT_ONOFF = 0b00000001
TM1650_MSK_ONOFF = 0b11111110
TM1650_BIT_DOT = 0b00000001
TM1650_MSK_DOT = 0b11110111
TM1650_BRIGHT_SHIFT = 4
TM1650_MSK_BRIGHT = 0b10001111
TM1650_MIN_BRIGHT = 0
TM1650_MAX_BRIGHT = 7


TM1650_CDigits = [
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 0x00
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 0x10
    0x00, 0x82, 0x21, 0x00, 0x00, 0x00, 0x00, 0x02, 0x39, 0x0F, 0x00, 0x00, 0x00, 0x40, 0x80, 0x00,  # 0x20
    0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F, 0x00, 0x00, 0x00, 0x48, 0x00, 0x53,  # 0x30
    0x00, 0x77, 0x7C, 0x39, 0x5E, 0x79, 0x71, 0x6F, 0x76, 0x06, 0x1E, 0x00, 0x38, 0x00, 0x54, 0x3F,  # 0x40
    0x73, 0x67, 0x50, 0x6D, 0x78, 0x3E, 0x00, 0x00, 0x00, 0x6E, 0x00, 0x39, 0x00, 0x0F, 0x00, 0x08,  # 0x50 
    0x63, 0x5F, 0x7C, 0x58, 0x5E, 0x7B, 0x71, 0x6F, 0x74, 0x02, 0x1E, 0x00, 0x06, 0x00, 0x54, 0x5C,  # 0x60
    0x73, 0x67, 0x50, 0x6D, 0x78, 0x1C, 0x00, 0x00, 0x00, 0x6E, 0x00, 0x39, 0x30, 0x0F, 0x00, 0x00   # 0x70
]


TM1650_CDigits_flip = [
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 0x00
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 0x10
    0x00, 0x82, 0x21, 0x00, 0x00, 0x00, 0x00, 0x02, 0x0F, 0x0F, 0x00, 0x00, 0x00, 0x40, 0x80, 0x00,  # 0x20
    0x3F, 0x30, 0x5B, 0x79, 0x74, 0x6D, 0x6F, 0x38, 0x7F, 0x7D, 0x00, 0x00, 0x00, 0x48, 0x00, 0x53,  # 0x30
    0x00, 0x7E, 0x67, 0x39, 0xF3, 0x4F, 0x4E, 0x7D, 0x76, 0x06, 0x1E, 0x00, 0x87, 0x00, 0x62, 0xBF,  # 0x40
    0x94, 0x67, 0x50, 0x6D, 0xC7, 0x37, 0x00, 0x00, 0x00, 0x6E, 0x00, 0x39, 0x00, 0x0F, 0x00, 0x08,  # 0x50
    0x63, 0x5F, 0x7C, 0x58, 0x5E, 0x7B, 0x4E, 0x6F, 0x66, 0x02, 0x1E, 0x00, 0x06, 0x00, 0x62, 0x63,  # 0x60
    0x5E, 0x67, 0x42, 0x6D, 0x78, 0x1C, 0x00, 0x00, 0x00, 0x6E, 0x00, 0x39, 0x30, 0x0F, 0x00, 0x00   # 0x70
]


#TM1650_CDigits_flip = [
#    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 0x00
#    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 0x10
#    0x00, 0x82, 0x21, 0x00, 0x00, 0x00, 0x00, 0x02, 15, 0x0F, 0x00, 0x00, 0x00, 64, 128, 0x00,  # 0x20
#    63, 48, 91, 121, 116, 109, 111, 56, 127, 125, 0x00, 0x00, 0x00, 0x48, 0x00, 0x53,  # 0x30
#    0x00, 126, 103, 0x39, 243, 79, 78, 125, 118, 0x06, 0x1E, 0x00, 135, 0x00, 98, 191,  # 0x40
#    0x94, 0x67, 0x50, 0x6D, 199, 55, 0x00, 0x00, 0x00, 0x6E, 0x00, 0x39, 0x00, 0x0F, 0x00, 0x08,  # 0x50 
#    0x63, 0x5F, 0x7C, 0x58, 0x5E, 0x7B, 78, 0x6F, 102, 0x02, 0x1E, 0x00, 0x06, 0x00, 98, 99,  # 0x60
#    94, 103, 66, 0x6D, 0x78, 0x1C, 0x00, 0x00, 0x00, 0x6E, 0x00, 0x39, 0x30, 0x0F, 0x00, 0x00   # 0x70
#]

class TM1650:
    def __init__(self, aNumDigits=4):
        self.iNumDigits = min(aNumDigits, TM1650_NUM_DIGITS)
        self.iPosition = None
        self.iActive = False
        self.iBrightness = 0
        self.iString = ['\0'] * (TM1650_MAX_STRING + 1)
        self.iBuffer = bytearray(self.iNumDigits)
        self.iCtrl = bytearray(self.iNumDigits)

    def init(self):
        self.iPosition = None
        self.iBuffer = bytearray(self.iNumDigits)
        self.iCtrl = bytearray(self.iNumDigits)
        self.iActive = os.system(f"i2cget -f -y -a {I2C_BUS} {TM1650_DISPLAY_BASE} 0") == 0
        self.clear()
        self.displayOn()

    def setBrightness(self, aValue=TM1650_MAX_BRIGHT):
        if not self.iActive:
            return

        self.iBrightness = min(aValue, TM1650_MAX_BRIGHT)
        for i in range(self.iNumDigits):
            self.iCtrl[i] = (self.iCtrl[i] & TM1650_MSK_BRIGHT) | (self.iBrightness << TM1650_BRIGHT_SHIFT)
            os.system(f"i2cset -f -y -a {I2C_BUS} {TM1650_DCTRL_BASE + i} {self.iCtrl[i]}")

    def setBrightnessGradually(self, aValue=TM1650_MAX_BRIGHT):
        if not self.iActive or aValue == self.iBrightness:
            return

        aValue = min(aValue, TM1650_MAX_BRIGHT)
        step = -1 if aValue < self.iBrightness else 1
        i = self.iBrightness

        while i != aValue:
            self.setBrightness(i)
#            time.sleep(0.05)
            time.sleep(0.5)
            i += step

    def displayState(self, aState):
        if aState:
            self.displayOn()
        else:
            self.displayOff()

    def displayOn(self):
        if not self.iActive:
            return

        for i in range(self.iNumDigits):
            self.iCtrl[i] = (self.iCtrl[i] & TM1650_MSK_ONOFF) | TM1650_BIT_DOT
            os.system(f"i2cset -f -y -a {I2C_BUS} {TM1650_DCTRL_BASE + i} {self.iCtrl[i]}")

    def displayOff(self):
        if not self.iActive:
            return

        for i in range(self.iNumDigits):
            self.iCtrl[i] = (self.iCtrl[i] & TM1650_MSK_ONOFF)
            os.system(f"i2cset -f -y -a {I2C_BUS} {TM1650_DCTRL_BASE + i} {self.iCtrl[i]}")

    def controlPosition(self, aPos, aValue):
        if not self.iActive:
            return

        if aPos < 0 or aPos >= self.iNumDigits:
            return

        self.iPosition = aPos

        if aValue:
            self.iCtrl[self.iPosition] |= TM1650_BIT_DOT
        else:
            self.iCtrl[self.iPosition] &= TM1650_MSK_DOT

        os.system(f"i2cset -f -y -a {I2C_BUS} {TM1650_DCTRL_BASE + self.iPosition} {self.iCtrl[self.iPosition]}")

    def clear(self):
        if not self.iActive:
            return

        for i in range(self.iNumDigits):
            self.iBuffer[i] = 0
            os.system(f"i2cset -f -y -a {I2C_BUS} {TM1650_DISPLAY_BASE + i} {self.iBuffer[i]}")

    def writeString(self, aString):
        if not self.iActive:
            return

        aString = aString[:TM1650_MAX_STRING]
        length = len(aString)
        self.clear()

        for i in range(length):
            self.iBuffer[i] = ord(aString[i])

        for i in range(self.iNumDigits):
            if i < length:
                os.system(f"i2cset -f -y -a {I2C_BUS} {TM1650_DISPLAY_BASE + i} {self.iBuffer[i]}")
            else:
                os.system(f"i2cset -f -y -a {I2C_BUS} {TM1650_DISPLAY_BASE + i} 0")

    def writeChar(self, aPos, aChar):
        if not self.iActive:
            return

        if aPos < 0 or aPos >= self.iNumDigits:
            return

        self.iBuffer[aPos] = ord(aChar)
        os.system(f"i2cset -f -y -a {I2C_BUS} {TM1650_DISPLAY_BASE + aPos} {self.iBuffer[aPos]}")

    def displayString(self, aString,inverti=False):
        if not self.iActive:
            return

        if inverti:
               aString=aString[::-1]

        for i in range(self.iNumDigits):
            a = ord(aString[i]) & 0b01111111
            dot = ord(aString[i]) & 0b10000000

            if inverti: 
                 self.iBuffer[i] = TM1650_CDigits_flip[a]
            else:
                 self.iBuffer[i] = TM1650_CDigits[a]

            if a:
                os.system(f"i2cset -f -y -a {I2C_BUS} {TM1650_DISPLAY_BASE + i} {self.iBuffer[i] | dot}")

    def setPosition(self,aPos, aValue):
        if not self.iActive:
          return

        if aPos < self.iNumDigits:
         self.iBuffer[aPos] = aValue
         os.system(f"i2cset -f -y -a {I2C_BUS} {TM1650_DISPLAY_BASE + aPos} {self.iBuffer[aPos]}")

    def setDot(self, aPos, aState):
         self.iBuffer[aPos] = self.iBuffer[aPos] & 0x7F | (0b10000000 if aState else 0)
         self.setPosition(aPos, self.iBuffer[aPos])



# Funzione per il thread del lampeggio del punto
def dot_thread():
    while True:
        DISPLAY.setDot(1, True)
        time.sleep(1)
        DISPLAY.setDot(1, False)
        time.sleep(1)


# Funzione per il thread dell'aggiustamento graduale della luminosità
def brightness_thread():
    while True:
        for brightness in range(8):
            DISPLAY.setBrightnessGradually(brightness)
            time.sleep(0.5)



DISPLAY = TM1650()
DISPLAY.init()
DISPLAY.setBrightnessGradually(TM1650_MAX_BRIGHT)

if len(sys.argv) > 1 and sys.argv[1] == "boot":
    DISPLAY.displayString('boot')
    exit(3)


previous_time = None

# Creazione dei thread
dot_thread = threading.Thread(target=dot_thread)
brightness_thread = threading.Thread(target=brightness_thread)

# Avvio dei thread
dot_thread.start()
brightness_thread.start()


while True:

      current_time = time.strftime("%H%M")

      if current_time != previous_time:
          DISPLAY.displayString(current_time, True)
          previous_time = current_time

