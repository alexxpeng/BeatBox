#Import the necessary Packages and scripts for this software to run
import cv2
#import pygame
from collections import Counter
from module import findnameoflandmark,findpostion
import math
import alsaaudio
import dbus, dbus.mainloop.glib, sys
from gi.repository import GLib

def on_property_changed(interface, changed, invalidated):
    if interface != 'org.bluez.MediaPlayer1':
        return
    for prop, value in changed.items():
        if prop == 'Status':
            print('Playback Status: {}'.format(value))
        elif prop == 'Track':
            print('Music Info:')
            for key in ('Title', 'Artist', 'Album'):
                print('   {}: {}'.format(key, value.get(key, '')))
def on_playback_control(fd, condition):
    str = fd.readline()
    if str.startswith('play'):
        player_iface.Play()
    elif str.startswith('pause'):
        player_iface.Pause()
    elif str.startswith('next'):
        player_iface.Next()
    elif str.startswith('prev'):
        player_iface.Previous()
    elif str.startswith('vol'):
        vol = int(str.split()[1])
        if vol not in range(0, 128):
            print('Possible Values: 0-127')
            return True
        systemAudio.setvolume(vol)
        transport_prop_iface.Set(
                'org.bluez.MediaTransport1',
                'Volume',
                dbus.UInt16(vol))
    return True

#testing wav file manual audio input
#pygame.mixer.init()
#pygame.mixer.set_num_channels(1)
#testSound = pygame.mixer.Sound("bthings.wav")

#systemAudio = alsaaudio.Mixer('PCM')
for mixername in alsaaudio.mixers():
    if str(mixername) == "Master" or str(mixername) == "PCM":
        systemAudio = alsaaudio.Mixer(mixername)

#Use CV2 Functionality to create a Video stream and add some values + variables
cap = cv2.VideoCapture(0)
tip=[8,12,16,20]
tipname=[8,12,16,20]
fingers=[]
finger=[]

#Create an infinite loop which will produce the live feed to our desktop and that will search for hands
while True:
     ret, frame = cap.read() 
     #Unedit the below line if your live feed is produced upsidedown
     #flipped = cv2.flip(frame, flipCode = -1)
     
     #Determines the frame size, 640 x 480 offers a nice balance between speed and accurate identification
     frame1 = cv2.resize(frame, (640, 480))
    
    #Below is used to determine location of the joints of the fingers 
     a=findpostion(frame1)
     b=findnameoflandmark(frame1)
     440
     #Below is a series of If statement that will determine if a finger is up or down and
     #then will print the details to the console
     if len(b and a)!=0:
        finger=[]
        if a[0][1:] < a[4][1:]: 
           finger.append(1)
           print (b[4])
          
        else:
           finger.append(0)   
        
        fingers=[] 
        for id in range(0,4):
            if a[tip[id]][2:] < a[tip[id]-2][2:]:
               print(b[tipname[id]])

               fingers.append(1)
    
            else:
               fingers.append(0)
     #Below will printu to the terminal the number of fingers that are up or down          
     x=fingers + finger
     c=Counter(x)
     up=c[1]
     down=c[0]
     print('Fingers up  : ', up)
     print('Fingers down: ', down)
     
     pastUp = up
     pauseFlag = 0
     if (up == 5):
         print("Playing sound")
         if (pauseFlag == 1):
             #player_iface.Play()
             pauseFlag = 0
         if (pauseFlag == 0):
             #player_iface.Pause()
             pauseFlag = 1
         #testSound.play(-1)   
     elif (up == 4):
         print("Volume 100")
         #testSound.set_volume(1)
         systemAudio.setvolume(100)
     elif (up == 3):
         print("Volume 70")
         #testSound.set_volume(0.7)
         systemAudio.setvolume(70)
     elif (up == 2):
         print("Volume 20")
         #testSound.set_volume(0.2)
         systemAudio.setvolume(20)
     elif (up == 1):
         print("Skipping")
         player_iface.Next()
     elif (up == 0):
         print("Stopping Sound")
         #testSound.stop()
     

     #Below shows the current frame to the desktop 
     cv2.imshow("Frame", frame1);
     key = cv2.waitKey(1) & 0xFF
     
     #Below states that if the |s| is press on the keyboard it will stop the system
     #if key == ord("s"):
     #  break
     '''
     dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
     bus = dbus.SystemBus()
     obj = bus.get_object('org.bluez', "/")
     mgr = dbus.Interface(obj, 'org.freedesktop.DBus.ObjectManager')
     player_iface = None
     transport_prop_iface = None
     for path, ifaces in mgr.GetManagedObjects().items():
         if 'org.bluez.MediaPlayer1' in ifaces:
             player_iface = dbus.Interface(
                    bus.get_object('org.bluez', path),
                    'org.bluez.MediaPlayer1')
         elif 'org.bluez.MediaTransport1' in ifaces:
             transport_prop_iface = dbus.Interface(
                    bus.get_object('org.bluez', path),
                    'org.freedesktop.DBus.Properties')
     if not player_iface:
         sys.exit('Error: Media Player not found.')
     if not transport_prop_iface:
         sys.exit('Error: DBus.Properties iface not found.')

     bus.add_signal_receiver(
            on_property_changed,
            bus_name='org.bluez',
            signal_name='PropertiesChanged',
            dbus_interface='org.freedesktop.DBus.Properties')
     GLib.io_add_watch(sys.stdin, GLib.IO_IN, on_playback_control)

    '''