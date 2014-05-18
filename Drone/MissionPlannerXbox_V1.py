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

class MyWindow():

    def __init__(self):


        #initialize channel PWM values
        
        for chan in range(1,9):
            Script.SendRC(chan,1500,False)
            Script.SendRC(3,Script.GetParam('RC3_MIN'),True)
            Script.Sleep(10)
            print "Initializaing channel %d" % chan    
	  

        while(True):
            self.controller()
            time.sleep(0.013*10)
	

    #event handler
    def controller(self):
        print "tick"
	sensitivity = 0.1

	#get the state of the controller
	self.gamePad = GamePad.GetState(PlayerIndex.One, GamePadDeadZone.Circular)

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

	    #to get a single trigger:
	    RTrigger = self.gamePad.Triggers.Right
	    print "Right trigger: %f" % RTrigger

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

	    #send Throttle
            throttlePWM = RTrigger * 1000 + 1000 #Ensures PWM is in range of 1000 - 2000
	    Script.SendRC(3,throttlePWM,True)
	    print("Throttle PWM: %f" % throttlePWM)
		
	    #other buttons listed at
	    #http://msdn.microsoft.com/en-us/library/microsoft.xna.framework.input.buttons.aspx
	    #eg. self.gamePad.Buttons.B, self.gamePad.Buttons.Y,
	    #self.gamePad.Buttons.X, self.gamePad.Buttons.Back, self.gamePad.Buttons.Start

	 
MyWindow()

if __name__ == '__main__':

  
  MyWindow()
