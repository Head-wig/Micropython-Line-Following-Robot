# Micropython Line Following Robot 
The goal of this project was to create a robot on the romi platform controlled by a Nucleo l476rg running micropython that can be activated using the user button on the Nucleo, follow a 1/4'' line, detect obstacles, and return to start potion after completing any given course. This was accomplished by mounting four TCRT5000 IR Sensors to the front of the romi and one limit switch in order to detect any obstacle that may be in the path of the robot.  The data from each sensor was read at a 25ms interval and was used to determine which movements to make based off of predetermined states. 

# Contents
 - [Romi Setup](#romi-setup) 
 - [Code Structure](#code-structure)
 - [Results](#results) 
 - [Potential Issues](#potential-issues)
 - [Future Work](#future-work)
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
As stated in the introduction, this code uses a myriad of different sensor states to determine how the robot will move. Below you can see a state transition diagram depicting the finite state machines used to model the behavior of romi. When first powered on the robot will move to the Off Mode state, as the Start_Button variable initializes as zero. Once the user button is pressed Start_Button is set to one and the code moves to Line Sensors Hub state. In this state it reads all of the sensors and compares them to each of the sensor states.  Once the corresponding sensor state is found the code will transition to either Pivot state or directly to the Set Duty Cycle state if the robot is going to continue moving forward. Once the Set Duty Cycle has completed it will return to the Button Check state and restart the process. While in the pivot state the code checks the front sensor value, if this value is equal to one, the code effectively returns to the Line Sensor hub state in order to start moving forward again. If at any point the limit switch at the front of the robot is depressed our code will stop what its doing and move to the Obstacle Maneuver state. In this state the robot will back up, turn so its parallel to the obstacle and move in an arch until its on the other side of the obstacle at which point our code will return to Button check state and subsequently the Line Sensor Hub State in order to find the line and continue on its path. 

![Appa FSM](https://i.ibb.co/DC4KRqK/Appa-s-FSM-drawio-1.png)
One last function of this code is the ability to stop the romi at any point by clicking the user button which will transition the code into the Off Mode state. The only time this function will not work is during the Obstacle Maneuver state. 
# Results

# Potential Issues

# Future Work

# BOM
