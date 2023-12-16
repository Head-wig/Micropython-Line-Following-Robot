

# Micropython Line Following Robot 
The goal of this project was to create a robot on the romi platform controlled by a Nucleo l476rg running micropython. This was accomplished by mounting four TCRT5000 IR Sensors to the front of the romi and one limit switch in order to detect any obstacle that may be in the path of the robot.  The data from each sensor was read at a 2ms interval and was used to determine which movements to make based off of predetermined states. 

# Contents
 - [Romi Setup](#romi-setup) 
 - [Dependencies Title](#dependencies-title) 
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

Once the pins are correctly connected, install the sensor mount provided in the Models folder. This model can be connected to the romi using two M2.5 bolts and nuts. The sensors can then be install with the same M2.5 bolts. Each IR sensor will need one bolt. while installing the IR sensors use the built in channel to route the connecting wires to the breadboard and Nucleo respectively. 
![SensorMount](https://i.ibb.co/YbMf36C/Sensor-Mount.png)









