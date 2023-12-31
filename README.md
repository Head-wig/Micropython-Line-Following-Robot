# Micropython Line Following Robot 
The goal of this project was to create a robot on the romi platform controlled by a Nucleo l476rg running micropython that can be activated using the user button on the Nucleo, follow a 1/4'' line, detect obstacles, and return to start potion after completing any given course. This was accomplished by mounting four TCRT5000 IR Sensors to the front of the romi and one limit switch in order to detect any obstacle that may be in the path of the robot.  The data from each sensor was read at a 25ms interval and was used to determine which movements to make based off of predetermined states. 

# Contents
 - [Romi Setup](#romi-setup) 
 - [Code Structure](#code-structure)
 - [Results](#results) 
 - [Known Bugs](#known-bugs)
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

Once the pins are correctly connected, install the sensor mount provided in the Models folder. As shown below this model can be connected to the romi using two M2.5 bolts and nuts. The IR sensors can then be install with one M2.5 bolt each. while installing the IR sensors use the built in channel to route the connecting wires to the breadboard and Nucleo respectively. The VCC and GND pins from each sensor should connect to breadboard's 3.5V and ground lanes which can be mounted any place on the romi and secured using double sided tape. Finally,  attach the limit switch to the front of the romi with two additional M2.5 bolts. These two bolts will tap into the material of the print and therefore not need nuts. 
![SensorMount](https://i.ibb.co/YbMf36C/Sensor-Mount.png)

# Code Structure
As stated in the introduction, this code uses a myriad of different sensor states to determine how the robot will move. Below is the state transition diagram depicting the finite state machines used to model the behavior of romi. When first powered on the robot will move to the Off Mode state, as the Start_Button variable initializes as zero. Once the user button is pressed Start_Button is set to one and the code moves to Line Sensors Hub state. In this state it reads all of the sensors and compares them to each of the sensor states.  

Once the corresponding sensor state is found the code will transition to either Pivot state or directly to the Set Duty Cycle state if the robot is going to continue moving forward. Once the Set Duty Cycle has completed it will return to the Button Check state and restart the process. While in the pivot state the code checks the front sensor value, if this value is equal to one, the code effectively returns to the Line Sensor hub state in order to start moving forward again.

 If at any point the limit switch at the front of the robot is depressed the code will stop what its doing and move to the Obstacle Maneuver state. In this state the robot will back up, turn so its parallel to the obstacle and move in an arch until its on the other side of the obstacle at which point the code will return to Button check state and subsequently the Line Sensor Hub State in order to find the line and continue on its path. 

![Appa FSM](https://i.ibb.co/DC4KRqK/Appa-s-FSM-drawio-1.png)
One last function of this code is the ability to stop the romi at any point by clicking the user button which will transition the code into the Off Mode state. The only time this function will not work is during the Obstacle Maneuver state. 
# Results
When tested, romi completed the course that had been laid out for it in only one minute and four seconds. Below is the video of this test.  Due to time constraints the ability to return to the robots starting position, and a more complex obstacle maneuver algorithm were not added. 

[![](https://markdown-videos-api.jorgenkh.no/youtube/NFez8l3HVpM)](https://youtu.be/NFez8l3HVpM )



![Romi1](https://i.ibb.co/MDNfNfk/IMG-5951.jpg)





# Known Bugs
This build does have a few bugs that this section hopes to address. The first issue is that the TCRT5000 IR Sensors only work on specific surfaces. If the surface is too reflective the sensors will get false readings which will lead the robot off course. Another issues with these sensors is that they can have some sort of malfunction that causes a  much longer response time. This issue comes on without warning and has no current solution. During the building and testing of this romi at least two sensors were replaced due to this issue. 

Another issues faced unrelated to the sensors was the way the Nucleo board interacted with Mac laptops. When loading scripts onto the Nucleo the micropython installation could get corrupted, loosing all files stored on the Nucleo, and necessitating the firmware to be re-flashed 

# Future Work

 - Add a function that will allow romi to return to its starting position using an IMU 
 - Increase compatibility with reflective materials
 - Add more sensors to increase consistency on dashed and curved lines
 - Smooth our turning by either introducing a turning state, changing the way romi pivots, or introducing A PID controller to our motors 

# BOM

| Items |Quantity  |
|--|--|
|Nucleo l476rg | 1 |
|Shoe Of Brian |1
|Romi kit|1
|Limit Switch |1
|Breadboard |1
|TCRT5000 IR Sensors |4
|Pack of assorted wires|1 
|Pack of heat shrink | 1
|Roll of filament |1
|M2.5 Screws | 8
|M2.5 Nuts | 6
|Shoe Of Brian mounting kit | 1
