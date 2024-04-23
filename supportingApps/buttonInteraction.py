# Importing Libraries
import serial
import time
from pyKey import pressKey, releaseKey, press, sendSequence, showKeys

arduino = serial.Serial(port='COM7', baudrate=9600, timeout=.1)

playPauseFlag = 1
newPauseFlag = 0

def readFromButton():
    playPauseFlag = 1
    newPauseFlag = 0
    value = arduino.readline()
    print(str(value)) 
    time.sleep(1)
    #blue
    if ( str(value) == "b'play\\r\\n'"):
        newPauseFlag = 0
        if (newPauseFlag != playPauseFlag):
            press(key='P', sec=1) #play/pause
            playPauseFlag = newPauseFlag
    #red
    elif ( str(value) == "b'up\\r\\n'"):
        newPauseFlag = 0
        if (newPauseFlag != playPauseFlag):
            press(key='U', sec=1) #vol upP
            playPauseFlag = newPauseFlag
    #green
    elif ( str(value) == "b'down\\r\\n'"):
        newPauseFlag = 0
        if (newPauseFlag != playPauseFlag):
            press(key='D', sec=1) #vol down
            playPauseFlag = newPauseFlag


while True:
    readFromButton()