# Chart-Light-Sim
Simulate Maritime chart navigation lights using Neopixels and CircuitPython

Written for Adafruit Circuit Playground Express using CircuitPython

Lets you simulate maritime lights (buoys, lighthouses etc) using Neopixels and a simple sequence format

##Example:
```python
#Cardingmill Bay Special Purpose Marker
#[Y FL Y 5S]
# Flashes Yellow, period 5 seconds.
# Create our buoy object, give it a name, a Neopixel address/pixel number, and a colour.
buoy1 = Buoy("Cardingmill SP",pixel=0,colour=YELLOW)
# set the flashing sequence. An array of alternating ON-OFF durations in seconds. Arbitrary length
# in this example, we turn on for 0.5 seconds, then off for 4.5 seconds. The sequence then repeats
buoy1.setSequence ([0.5,4.5])

# Example 2: 
# Sgeir Rathaid "Scrat Rocks" South Cardinal
# [YB Q(6)+ LFL 15S]
# Quick flash x6, followed by single long flash, period 15 seconds.
scratS = Buoy("Scrat Rocks South Cardinal",pixel=8,colour=WHITE)
scratS.setSequence([0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,1.5,7.5])
```
