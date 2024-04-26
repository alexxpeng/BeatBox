#Import the necessary Packages and scripts for this software to run
import cv2
from collections import Counter
from module import findnameoflandmark,findpostion
import math
import alsaaudio
import pigpio
import sys
#import pygame
#initialize
up = 0
down = 5

#gpio for led control
thisPi = pigpio.pi()

open('iostream.txt', 'w').close()

#testing wav file manual audio input
#pygame.mixer.init()
#pygame.mixer.set_num_channels(1)
#testSound = pygame.mixer.Sound("bthings.wav")

for mixername in alsaaudio.mixers():
    if str(mixername) == "Master" or str(mixername) == "PCM":
        systemAudio = alsaaudio.Mixer(mixername)

#cv2 setup to capture vidoe stream and map fingers
cap = cv2.VideoCapture(0)
tip=[8,12,16,20]
tipname=[8,12,16,20]
fingers=[]
finger=[]


#search for hands in live feed
while True:
     ret, frame = cap.read() 
     
     #set frame 640 x 480
     frame1 = cv2.resize(frame, (640, 480))
    
     #find joints
     a=findpostion(frame1)
     b=findnameoflandmark(frame1)
     
     if len(b and a)!=0:
        finger=[]
        if a[0][1:] < a[4][1:]: 
           finger.append(1)
        else:
           finger.append(0)   
        fingers=[] 
        for id in range(0,4):
            if a[tip[id]][2:] < a[tip[id]-2][2:]:
               fingers.append(1)
            else:
               fingers.append(0)
               
     #print to the terminal the number of fingers that are up or down          
     x=fingers + finger
     c=Counter(x)
     pastUp = up
     pastDown = down
     up=c[1]
     down=c[0]
     
     if (pastUp != up):
         print('Fingers up  : ', up)
         print('Fingers down: ', down)
         print('==========================')
         if (up == 5):
             print("Playing")
             print('play', file=open('iostream.txt','a'))
         elif (up == 4):
             print("Full Volume")
             systemAudio.setvolume(100)
         elif (up == 3):
             print("Low Volume")
             systemAudio.setvolume(60)
         elif (up == 2):
             print("Skip song")
             print('next', file=open('iostream.txt','a'))
         elif (up == 1):
             print("Paused")
             print('pause', file=open('iostream.txt','a'))
         elif (up == 0):
             print("Stopping Sound")
             
         print('==========================')
     
     cv2.imshow("Frame", frame1);
     key = cv2.waitKey(1) & 0xFF
     

    