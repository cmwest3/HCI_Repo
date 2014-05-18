import sys
import clr
import math
clr.AddReference (' System ')
clr.AddReference (' System.Core ')
clr.AddReference('Microsoft.Xna.Framework')
clr.AddReference('Microsoft.Xna.Framework.Game')

import System

from System.Timers import Timer
from System import Action

from Microsoft.Xna.Framework import *
from Microsoft.Xna.Framework.Input import *

import time

flightMode=1

class MyWindow():
    

    def __init__(self):


        #initialize rc values
        
        for chan in range(1,9):
            Script.SendRC(chan,1500,False)
            Script.SendRC(3,Script.GetParam('RC3_MIN'),True)
            Script.Sleep(10)
            print "Initializaing channel %d" % chan
	  
        print("Flight mode is: %d" % flightMode)
        self.changeMode()
        
        while(True):
            self.controller()
            time.sleep(0.013*10)
    
    def changeMode(self):
        global flightMode
        if(flightMode ==1):
            Script.ChangeMode("Stabilize")
        elif(flightMode ==2):
            Script.ChangeMode("AltHold")
        elif(flightMode ==3):
                Script.ChangeMode("Loiter")
        elif(flightMode ==4):
            Script.ChangeMode("RTL")
        elif(flightMode ==5):
            Script.ChangeMode("Land")
        elif(flightMode ==6):
            Script.ChangeMode("Auto")
        elif(flightMode ==7):
            Script.ChangeMode("Acro")
        elif(flightMode ==8):
            Script.ChangeMode("Sport")
        elif(flightMode ==9):
            Script.ChangeMode("Drift")
        elif(flightMode ==10):
            Script.ChangeMode("Guided")
        elif(flightMode ==11):
            Script.ChangeMode("Circle")
        elif(flightMode ==12):
            Script.ChangeMode("OF_Loiter")
        else:
            Script.ChangeMode("Stabilize")
	

    #event handler
    def controller(self):
        print "tick"
	sensitivity = 0.1
	global flightMode

	#get the state of the controller
	self.gamePad = GamePad.GetState(PlayerIndex.One, GamePadDeadZone.Circular)
        fMode = cs.mode
	
	if (self.gamePad.IsConnected):
            #Joysicks
            print "Joysticks:"

	    #to get a single sick axis
	    hpos1 = self.gamePad.ThumbSticks.Left.X
	    vpos1 = self.gamePad.ThumbSticks.Left.Y
	    hpos2 = self.gamePad.ThumbSticks.Right.X
	    vpos2 = self.gamePad.ThumbSticks.Right.Y

	    #ignore small joystick movements
	    if (math.fabs(hpos1) < sensitivity):
	    	hpos1 = 0
	    if (math.fabs(vpos1) < sensitivity):
	    	vpos1 = 0
	    if (math.fabs(vpos2) < sensitivity):
	    	vpos2 = 0
	    if (math.fabs(hpos2) < sensitivity):
    		hpos2 = 0

	    print "Left Stick: (%f,%f) Right Stick: (%f,%f)" % (hpos1,vpos1,hpos2,vpos2)
		

	    #if you want the vector indicated by the joystick:
	    vectorMagnitude1 = math.sqrt(math.pow(hpos1,2) + math.pow(vpos1, 2))
	    theta1 = math.atan2(vpos1, hpos1)

	    vectorMagnitude2 = math.sqrt(math.pow(hpos2,2) + math.pow(vpos2, 2))
	    theta1 = math.atan2(vpos2, hpos2)  

	    #to get a single tigger:
	    LTrigger = self.gamePad.Triggers.Left
	    RTrigger = self.gamePad.Triggers.Right

	    print "Left trigger: %f" % LTrigger
	    print "Right trigger: %f" % RTrigger

	    print self.gamePad.Buttons.A

	    if (self.gamePad.Buttons.B == ButtonState.Pressed):
	    	B = 1
	    	print 'B'
	    else:
	    	B = 0

	    if (self.gamePad.Buttons.X == ButtonState.Pressed):
                print 'X'
	    else:
	    	X = 0

	    if (self.gamePad.Buttons.Y == ButtonState.Pressed):
	    	print('Y')
	    	#perform takeoff procedure, there should be failsafes to be able to not perform if disarmed
                if(cs.mode == "AltHold"): #first checks if in alt mode
                    abort = False
                    print("Take-off procedure inititated! Hold Y to cancel.")
                    time.sleep(1)
                    Script.SendRC(3,1000,True) #sets throttle to 0
                    print("Throttle set to 0")
                    x = 3
                    while(x>0):#Then waits 3 seconds for abort command
                        #get state of controller
                        self.gamePad = GamePad.GetState(PlayerIndex.One, GamePadDeadZone.Circular)

                        print x
                        if (self.gamePad.Buttons.Y == ButtonState.Pressed):
                            print("Y has been pressed. Aborting!")
                            time.sleep(1)
                            abort = True
                            break
                        x -= 1
                        time.sleep(1)
                    
                    if(abort == False): #checks for abort command
                        print("Abort is false, stand by...")
                        time.sleep(1)
                        while(cs.alt < 2):
                            #get state of controller
                            self.gamePad = GamePad.GetState(PlayerIndex.One, GamePadDeadZone.Circular)
                            
                            print("Taking off!")
                            if(self.gamePad.Buttons.Y == ButtonState.Pressed): #checks for abort command during takeoff
                                print("Y has been pressed in take off!")
                                abort = True
                                break
                            Script.SendRC(3, 1700, True)
                        Script.SendRC(3,1500,True)
                        print("Throttle set to 50%")
                        time.sleep(1)
                    if(abort == True): #if aborted
                        print("Take off aborted!!!")
                        time.sleep(1)
                else:
                    print("Drone most be in 'AltHold' mode! Use bumpers to select")
                    time.sleep(2)
                    
	    if (self.gamePad.Buttons.Back == ButtonState.Pressed):
	    	print("Disarming...")
    		MAV.doARM(False)
	    	if(cs.armed == False):
                    print("Drone has been disarmed!")
		else:
                    print("ERROR: Drone cannot be disarmed!")

	    if (self.gamePad.Buttons.Start == ButtonState.Pressed):
		print("Arming...")
		MAV.doARM(True)
		if(cs.armed == True):
		    print("Drone has been armed! Stay clear!")
		else:
		    print("ERROR: Drone cannot be armed! See HUD for details")

	    if (self.gamePad.Buttons.LeftShoulder == ButtonState.Pressed):
		print("Left Shoulder")
		if(flightMode <= 1):
                   flightMode = 12
		else:
		    flightMode -= 1
		self.changeMode()

	    if (self.gamePad.Buttons.RightShoulder == ButtonState.Pressed):
		print("Right Shoulder")
		if(flightMode >= 12):
		    flightMode = 1
		else:
		    flightMode += 1
		self.changeMode()
	    print("Flight mode selection is: %d" % flightMode)
	    print("Flight mode is: %s" % fMode)
	    

	    #Send Pitch PWM
	    pitchPWM = -vpos1 * 500 + 1500
            Script.SendRC(2,pitchPWM,False)
            print("Pitch PWM: %f" % pitchPWM)

	    #send Roll PWM
	    rollPWM = hpos1 * 500 + 1500
            Script.SendRC(1,rollPWM,False)
	    print ("Roll PWM: %f" % rollPWM)

	    #send yaw

	    yawPWM = hpos2 * 500 + 1500
	    Script.SendRC(4, yawPWM, False)
	    print ("Yaw PWM: %f" % yawPWM)
            
            if(fMode == "AltHold"):
                if(LTrigger > 0):
                    trigger = -(LTrigger)
                else:
                    trigger = RTrigger
                throttlePWM = trigger * 500 + 1500
            else:
                throttlePWM = RTrigger * 1000 + 1000 #Ensures PWM is in range of 1000 - 2000

	    #send Throttle
	    Script.SendRC(3,throttlePWM,True)
	    print("Throttle PWM: %f" % throttlePWM)
		
	    #other buttons listed at
	    #http://msdn.microsoft.com/en-us/library/microsoft.xna.framework.input.buttons.aspx
	    #eg. self.gamePad.Buttons.B, self.gamePad.Buttons.Y,
	    #self.gamePad.Buttons.X, self.gamePad.Buttons.Back, self.gamePad.Buttons.Start
	 
MyWindow()

if __name__ == '__main__':
  
  MyWindow()
