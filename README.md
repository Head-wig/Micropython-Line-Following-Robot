# Micropython Line Following Robot 
The goal of this project was to create a robot on the romi platform controlled by a Nucleo l476rg running micropython. This was accomplished by mounting four TCRT5000 IR Sensors to the front of the romi and one limit switch in order to detect any obstacle that may be in the path of the robot.  The data from each sensor was read at a 2ms interval and was used to determine which movements to make based off of predetermined states. 

# Contents
 - [Romi Setup](#romi-setup) 
 - [Code Structure](#code-structure) 
 - [BOM](#billofmaterials)

# Romi Setup
To prepare the romi, connect wires from the four IR sensors, the motor drivers, the limit switch and the breadboard as described in the table below. This table will also contain information that is pertinent to the function of each pin in the classes provided.

|Function|Pin |Mode|Pull|
|--|--|--|--
| Right Motor  PWM|B8|PWM|-|
| Right Motor  DIR|A4|OUT_PP|-|
| Right Motor  SLP|B0|OUT_PP|-| 
| Left Motor  PWM|C8|PWM|-|
| Left Motor  DIR|A10|OUT_PP|-| 
| Left Motor  SLP|B3|OUT_PP|-|  
| IR  Left Digital Out  |C9|IN|-|
| IR  Front Digital Out |C11|IN|-|
| IR  Back Digital Out |C12|IN|-
| IR  Right Digital Out |C10|IN|-|
| Limit Switch Out |B9|IN|PULL_DOWN|
| Bread Board 3.5V Lane | 3.5V |-|-|
| Bread Board Ground Lane |GND|-|-|

Once the pins are correctly connected, install the sensor mount provided in the Models folder. As shown below this model can be connected to the romi using two M2.5 bolts and nuts. The IR sensors can then be install with one M2.5 bolts. while installing the IR sensors use the built in channel to route the connecting wires to the breadboard and Nucleo respectively. The VCC and GND pins from each sensor should connect to breadboard's 3.5V and ground lanes which can be mounted any place on the romi and secured using double sided tape. Finally,  attach the limit switch to the front of the romi with two additional M2.5 bolts. These two bolts will tap into the material of the print and therefore not need nuts. 
![SensorMount](https://i.ibb.co/YbMf36C/Sensor-Mount.png)

# Code Structure

# BOM
