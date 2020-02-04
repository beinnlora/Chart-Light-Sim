# Chart buoy light simulator for Neopixel/CircuitPlayground Express/CircuitPython
# (C) Stephen Wilson February 2020 steve@burnside.it
# GPL v3
#=====
# INITIALISE LIBRARIES AND CONSTANTS
#=====
import time,random,board,digitalio,neopixel
from adafruit_circuitplayground import cp
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
OFF = (0, 0, 0)
cp.pixels.brightness = 1

#=====
# Create a Buoy class.
#=====
class Buoy:
    # Create a register of all buoys, so we can iterate through all buoys.
    _registry = []
    # Initialisation/creation of new light: set defaults
    def __init__(self,name,pixel,colour=RED,sequence=[1,1],initialDelay=0,jitter=0,startTime=0):
        #add our buoy to the list of all buoys
        #self.led = digitalio.DigitalInOut(pixel)
        #self.led.direction = digitalio.Direction.OUTPUT
        self._registry.append(self)                     # add our buoy to the register of lights
        self.name = name                                # buoy name (for serial debug)
        print ("initialising new buoy: ",self.name)         
        self.pixel = pixel                              # Neopixel PIXEL NUMBER (0-9 on CircuitPlayground)
        self.setSequence(sequence)                      # ON-OFF sequence array
        self.colour = colour                            # pixel colour (see definitions above)
        self.initialDelay=initialDelay                  # Delay the start of a buoy's sequence (seconds) 
        self.jitter = jitter                            # Add a random jitter to a buoy's timing by plus or minus this amount(seconds)
        self.nextEventTime = 0                          # timestamp of when next event (on or off) is due
        self.currentState = False                       # Is the light currently on (True) or off (False)
        
        if (startTime ==0):                             # Initialise Start Time
            self.startTime = time.monotonic()
        else:
            self.startTime = startTime
        self.setStartTime(startTime)
        
    #=====
    # HOW TO TURN LIGHT ON OR OFF
    #=====
    def lightOn(self):
        print ("turning on ",self.name,"on pixel ",self.pixel)
        cp.pixels[self.pixel]=self.colour
    def lightOff(self):
        print ("turning off ",self.name,"on pixel ",self.pixel)
        cp.pixels[self.pixel]=OFF
    
    #=====
    # Set the start timestamp of a sequence (ensures synchronised lights start at the same time)
    # Sets nextEventTime for the first event.
    # Also accounts for any initial delay and any jitter.
    #=====
    def setStartTime(self,timeIn=time.monotonic()):
        #Pass a timestamp in, add on random jitter and startup delay. Calculate the nextEventTime.
        rand = random.uniform (-1,1)
        print ("Setting Start Time of : ",self.name)
        jit = self.jitter*rand
        self.startTime = timeIn + self.initialDelay + jit
        self.nextEventTime = self.startTime
        print ("timeIn     initialDelay     jitter      =startTime")
        print (timeIn," ",self.initialDelay," ",jit," ",self.startTime)
    #=====
    # CHECK AND PERFORM ANY NECESSARY EVENTS 
    #=====
    def check(self):
        # Has the next Event time passed?
        if (time.monotonic() > self.nextEventTime):
            print ("Event Needed: time now: ",time.monotonic())
            # TURN LIGHT ON OR OFF AS NEEDED (TOGGLE)
            if (self.currentState==True):
                self.currentState=False
                self.lightOff()
            else: 
                self.currentState=True
                self.lightOn()
                
            #=====
            #Set the time of the next event, calculated from the sequence array
            #=====
    
            self.nextEventTime = time.monotonic() + self.jitter*(random.uniform(-1,1)) + self.sequence[self.sequencePointer]
            self.sequencePointer = self.sequencePointer + 1
            if (self.sequencePointer>(self.sequenceLength-1)):
                self.sequencePointer=0
    #=====
    # Store a supplied sequence in the Object.
    # Calculates sequence length and resets sequence pointer
    #=====    
    def setSequence(self,seq):
        self.sequenceLength = len(seq)
        self.sequencePointer=0
        self.sequence = seq
        print ("New Sequence for buoy: ",self.name,"/\t ", self.sequence, " len: ",self.sequenceLength)


#==============================================
# define our buoys
#==============================================
# 1) Make a new Buoy object:

# name: Give your buoy a name for easy reference
# pixel:  the Neopixel pixel number (0-9)
# colour: (optional). See above list of colours
# initialDelay (optional). delay the first flash by this amount of time (seconds)
# jitter (optional). Introduces a random amount of delay into the sequence (seconds). 

# example Ferry Rocks East Cardinal buoy, by Kerrera Ferry

# bouy1 = Buoy("Ferry Rocks East Cardinal",pixel=0,colour=WHITE)

# 2) Set the sequence
# you set the flashing sequence by making a list:
# a) the computer reads the first number in the list, and turns the light ON for this amount of time
# b) the computer reads the next number in the list, and turns the light OFF for this amount of time.
# c) this continues, alternating between turning the light ON and OFF for the given amount of time
# d) when the end of the list is reached, it loops back to the beginning!
#

# A simple example of flashing a light once every 10 seconds would be:
#      buoy1.setSequence([1,9])
# Why 9? Well, we turn it ON for one second, then OFF for 9 seconds, so the total sequence length
# is 10 seconds!
#
# In our example of Ferry Rocks East Cardinal, the chart says
# The chart says
# "FERRY ROCKS EAST CARDINAL:  QF(3) 10s
# What does this mean? 
# https://en.wikipedia.org/wiki/Light_characteristic
# QF(3) means three quick flashes. A Quick flash is between 60 and 80 flashes per minute
# 10s means the flashes repeat every 10 seconds.
# Do the maths on how long a flash is then: 
# 60 flashes per minute = 1 second per flash. 
# 80 flashes per second = 0.75 seconds per flash.
# The light "on" and "off durations should match, so, for QF(3) we need
# ON for 0.75s
# OFF for 0.75s
# ON for 0.75s
# OFF for 0.75s
# ON for 0.75s

# 
# How do we get this to repeat every 10 seconds?
# We know our TOTAL sequence duration should be 10 seconds, and the above flashing takes up
# 0.75 * 5 = 3.75 seconds
# So, at the end of our sequence, we need turn OFF for 10s - 3.75s = 6.25 s
# Our final sequence is therefore
# ON for 0.75s
# OFF for 0.75s
# ON for 0.75s
# OFF for 0.75s
# ON for 0.75s
# OFF for 6.25s
#REPEAT

# So, QF(3) 10s translates to
#     buoy1.setSequence([0.75,0.75,0.75,0.75,0.75,6.25])

# Example 2 Dunollie Point 
# FL(2) WRG 6S 8-6M
# Flashing twice every 6 seconds.
# Sector light with WHITE, RED and GREEN sectors (so we need three Buoy objects all with the same sequence)

# Have a play with sequences
#=======================================

# Heather Island Port Channel Marker
# [FL R 2.5S 11m 2M]
hp = Buoy ("Heather Port ",pixel=0,colour=RED)
hp.setSequence([0.5,2])

#Cardingmill Bay Special Purpuse
# [Y FL Y 5S]
cbsp = Buoy("Cardingmill SP",pixel=1,colour=YELLOW)
cbsp.setSequence ([0.5,4.5])

#Dunollie Light - three sector light
# [FL(2) WRG 6S 8-6M]
dunollieR = Buoy ("Dunollie Light Red",  pixel = 2, colour = RED)
dunollieW = Buoy ("Dunollie Light White",pixel = 3, colour = WHITE)
dunollieG = Buoy ("Dunollie Light Green",pixel = 4, colour = GREEN)

dunollieR.setSequence([0.5,0.5,0.5,4.5])
dunollieW.setSequence([0.5,0.5,0.5,4.5])
dunollieG.setSequence([0.5,0.5,0.5,4.5])

# North Channel Starboard Channel Markers. 
#n.b. we will artificially sequence them, to try out the delay feature
# [G FL G 2S]
north1 = Buoy("first", pixel=5,colour=GREEN,initialDelay=0)
north2 = Buoy("second",pixel=6,colour=GREEN,initialDelay=0.3)
north3 = Buoy("third", pixel=7,colour=GREEN,initialDelay=0.6)

north1.setSequence([0.5,1.5])
north2.setSequence([0.5,1.5])
north3.setSequence([0.5,1.5])

# Sgeir Rathaid "Scrat Rocks" South Cardinal
# [YB Q(6)+ LFL 15S]
scratS = Buoy("Scrat Rocks South Cardinal",pixel=8,colour=WHITE)
scratS.setSequence([0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,1.5,7.5])

# END OF SETTING LIGHTS
#===================================================
# MAIN PROGRAM LOOP
#===================================================

# Synchronise start times - give the system 0.1 seconds to initialise each light,
start = time.monotonic()  + 0.1
for person in Buoy._registry:
    person.setStartTime(start)
    
# Create a loop over each light, and check if each light should turn on or off.
try:
     while True:
        for light in Buoy._registry:
            light.check()
except KeyboardInterrupt:
    pass
