from pyb import Pin, ExtInt, Timer
from time import ticks_ms, ticks_diff
import CLASSES
from CLASSES import ClosedLoop_Left, ClosedLoop_Right
import pyb
import math
# Appa Mode Key
# 10 = Going
# 20 = At end point
# 30 = 

class appa_brain: # Read the Sensors and assigning appropriate task
    '''! A class implementing data collection and serial (ie vcp)
        communication
    '''
    def __init__(self, Appa_Mode, Left_Wheel_RPM, Right_Wheel_RPM, X_Distance, Y_Distance, DEBUG_VAL):
        
        self.Appa_Mode = Appa_Mode
        self.Appa_Mode.put(10)
        self.Left_Wheel_RPM = Left_Wheel_RPM
        self.Right_Wheel_RPM = Right_Wheel_RPM
        self.Appa_Mode = DEBUG_VAL
        # User Button Set Up
        self.PA5 = Pin(Pin.cpu.A5, mode=Pin.OUT_PP)
        self.button_int = ExtInt(Pin.cpu.C13, ExtInt.IRQ_FALLING, Pin.PULL_NONE, lambda p: self.PA5.value(0 if self.PA5.value() else 1))
        
        # Bump sensor set up  
        self.Bump_Sensor = Pin(Pin.cpu.B9, mode= Pin.IN, pull= Pin.PULL_DOWN)
        
        # Desired Wheel Speed in term of duty cycle
        self.P_Gain = 0
        self.I_Gain = 0
        self.D_Gain = 0 # 0.2
        self.LEFT_Vel_Desired = 0
        self.RIGHT_Vel_Desired = 0 
        # Initialize Close Loop Control
        self.ClosedLoop_LEFT = ClosedLoop_Left(0,0,0,0,0)
        self.ClosedLoop_RIGHT = ClosedLoop_Right(0,0,0,0,0)
        
        # Line Sensor Set Up
        self.Sensor_L = Pin(Pin.cpu.C9, Pin.IN) # Left
        self.Sensor_T = Pin(Pin.cpu.C11, Pin.IN) # Top
        self.Sensor_R = Pin(Pin.cpu.C12, Pin.IN) # Right
        self.Sensor_B = Pin(Pin.cpu.C10, Pin.IN) # Bottom
        
        # Speed Set Up in terms of Duty Cycle
        self.speed_nor = 15 # 15
        # self.soft_turn = 17.5 # 30
        self.pivot = 12.5 # 15
        self.Previous_Values = []
        
        # Encoder Set Up
        
        # right encoder A6 - 3/1, A7 - 3/2
        self.Right_Enc = CLASSES.Encoder(1, Pin.cpu.A8, Pin.cpu.A9)
        # left encoder A8 - 1/1 A9 - 1/2
        self.Left_Enc = CLASSES.Encoder(2, Pin.cpu.A0, Pin.cpu.A1)
        
        # Right motor

        self.B8 = Pin.cpu.B8# PWM Pin
        self.B0 = Pin.cpu.B0# En Pin
        self.A4 = Pin.cpu.A4# Dir Pin
        self.RIGHT_tim = Timer(4, freq = 20000) # Channel 2
        # Left motor

        self.C8 = Pin.cpu.C8 # PWM Pin
        self.A10 = Pin.cpu.A10 # EN Pin
        self.B3 = Pin.cpu.B3 # Dir Pin
        self.LEFT_tim = Timer(8, freq = 20000) # Channel 2
        self.offset = 2
        
        # Make Motor Go

        # Make right motor object
        self.RIGHT = CLASSES.Motor(self.RIGHT_tim, self.B8, self.B0, self.A4)
        # self.RIGHT.set_duty(0)
        self.RIGHT.enable()
        
        # Make left motor object
        self.LEFT = CLASSES.Motor(self.LEFT_tim, self.C8, self.A10, self.B3)
        # self.LEFT.set_duty(0)
        self.LEFT.enable()
        self.count = 0
        self.state = -1 # Duty cycle is 0 until button is pressed
        #turning
        self.obstacle = False
        self.started = False
        
        self.Left_Back_Up = False
        self.Right_Back_Up = False
        
        self.Return_Sequence = 0
        self.End_Stage = False
        self.return_initiated = False
        
        self.turn_around = False
        self.forward = False
        self.pivot_done = False
        self.At_End = False
        self.At_Start = False
        
    def run(self):
        while True:
            # Check if button is pressed, if it is toggle go between off and on mode
            if self.state == -1:

                # if self.Appa_Mode.get() == 20:
                #     self.state = 5    
                if self.Bump_Sensor.value() == 0  or self.obstacle == True:
                    self.state = 4
                                        
                elif self.PA5.value() == 1:
                    # self.Appa_Go = True
                    # print("go")
                    self.state = 0
                elif self.PA5.value() == 0:
                    # self.Appa_Go = False
                    self.state = 3
                    # print("no go")

            if self.state == 0: # Main State // HUB
                # print("hubbing")
                self.Sensor_Values = [self.Sensor_L.value(), self.Sensor_T.value(), self.Sensor_B.value(), self.Sensor_R.value()]
                self.state = -1  
                self.Previous_Values = self.Sensor_Values
                self.hub_ticks = ticks_ms()
                
                # # # Had reached the end
                # if self.Sensor_Values == [0,1,0,0]:
                #     if self.At_End == True:
                #         self.state = 5
                #         self.At_End = False
                #     elif self.At_Start == True:
                #         self.state = 6
                                        
                # go straight
                if self.Sensor_T.value() == 1 or self.pivot_done == True:# or self.Sensor_B.value() == 1:#self.Sensor_Values == [0,0,1,0] or self.Sensor_Values == [0,1,0,0] or self.Sensor_Values == [0,1,1,0]:# or self.Sensor_Values == [1,1,1,1]: # Go Straight
                    # if ticks_diff(ticks_ms, self.hub_ticks) < 1000:
                    self.LEFT_Vel_Desired = self.speed_nor
                    self.RIGHT_Vel_Desired = self.speed_nor
                    self.state = 2 # Always go to set the Duty Cycle
                    self.pivot_done = False
                    print("going straight")
                    
                
                # Hashed Line Logic 
                elif (self.Sensor_L.value() == 1 and self.Sensor_R.value() == 1) and (self.Sensor_T.value() == 1 or self.Sensor_B.value() == 1):
                    self.LEFT_Vel_Desired = self.speed_nor
                    self.RIGHT_Vel_Desired = self.speed_nor
                    self.state = 2 # Always go to set the Duty Cycle
                    
                    print("going straight")
                    
                # pivot left
                elif self.Sensor_L.value() == 1 or (self.Sensor_L.value() == 1 and self.Sensor_T.value() == 0): 
                    self.state = 7
                    


                # pivot right
                elif self.Sensor_R.value() == 1 or (self.Sensor_R.value() == 1 and self.Sensor_T.value() == 0): 
                    self.state = 8
                    

                        
                # For some reason only the bottom reads, go forward
                elif self.Sensor_B.value() == 1:# or self.Sensor_B.value() == 1:#self.Sensor_Values == [0,0,1,0] or self.Sensor_Values == [0,1,0,0] or self.Sensor_Values == [0,1,1,0]:# or self.Sensor_Values == [1,1,1,1]: # Go Straight
                    self.LEFT_Vel_Desired = self.speed_nor
                    self.RIGHT_Vel_Desired = self.speed_nor
                    self.state = 2 # Always go to set the Duty Cycle
                    print("going straight")
                    
                
                # else:
                #     print("you're fucked")
                #     self.Sensor_Values = self.Previous_Values
                #     self.LEFT_Vel_Desired = self.speed_nor
                #     self.RIGHT_Vel_Desired = self.speed_nor
                #     self.state = 2 # Always go to set the Duty Cycle
                    
            elif self.state == 1: # Pivot State
                if self.Sensor_R.value() == 1: # Pivot Right
                    self.LEFT_Vel_Desired = self.pivot 
                    self.RIGHT_Vel_Desired = -self.pivot
                    self.state = 2
                    if self.sensor_B.value() == 0:
                        self.LEFT_Vel_Desired = self.pivot 
                        self.RIGHT_Vel_Desired = -self.pivot
                        self.state = 2
                    elif self.Sensor_T.value() == 1 or self.Sensor_B.value() == 1:# or self.Sensor_B.value() == 1:
                        self.state = 0
                        self.LEFT_Vel_Desired = self.speed_nor
                        self.RIGHT_Vel_Desired = self.speed_nor
                elif self.Sensor_L.value() == 1: # Pivot Left
                    self.LEFT_Vel_Desired = -self.pivot 
                    self.RIGHT_Vel_Desired = self.pivot
                    
                    if self.sensor_B.value() == 0:
                        self.LEFT_Vel_Desired = -self.pivot 
                        self.RIGHT_Vel_Desired = self.pivot
                        self.state = 2
                    elif self.Sensor_T.value() == 1 or self.Sensor_B.value() == 1:# or self.Sensor_B.value() == 1:
                        self.state = 0
                        self.LEFT_Vel_Desired = self.speed_nor
                        self.RIGHT_Vel_Desired = self.speed_nor
                        self.state = 2
                else: # If neither value are read, go back to hub
                     self.state = 0
                     self.LEFT_Vel_Desired = self.speed_nor
                     self.RIGHT_Vel_Desired = self.speed_nor
                     
            elif self.state == 2: # Set Duty Cycle / Implement Duty Cycle Here
                self.LEFT.set_duty(self.LEFT_Vel_Desired+self.offset)
                self.RIGHT.set_duty(self.RIGHT_Vel_Desired)
                self.state = -1 # Always go back to the button
                
            elif self.state ==  3: # OFF MODE
                self.LEFT.set_duty(0)
                self.RIGHT.set_duty(0)
                self.state = -1
                
            elif self.state == 4: # Obstacle Manuveur
                self.obstacle = True
                if self.started == False:
                     self.ticks4 = ticks_ms()
                     self.LEFT.set_duty(-22)
                     self.RIGHT.set_duty(-20)
                     self.backup = True
                     self.Pivoting = False
                     self.Turning = False
                     self.done = False 
                     self.started = True 
                     
                # Back UP
                if self.backup:
                     self.state = -1
                     self.LEFT.set_duty(-22)
                     self.RIGHT.set_duty(-20)
                     if ticks_diff(ticks_ms(), self.ticks4) > 250:
                         self.ticks4 = ticks_ms()
                         self.backup = False
                         self.Pivoting = True
                         
                elif self.Pivoting:
                    self.state = -1
                    self.LEFT.set_duty(20)
                    self.RIGHT.set_duty(-20)
                    if ticks_diff(ticks_ms(), self.ticks4) > 750:
                        self.ticks4 = ticks_ms()
                        self.Pivoting = False
                        self.Turning = True

                elif self.Turning:
                    self.state = -1
                    if ticks_diff(ticks_ms(), self.ticks4) > 2500: 
                        if self.Sensor_Values != [0,0,0,0]:
                            self.Turning = False
                            self.done = True
                    elif ticks_diff(ticks_ms(), self.ticks4) < 100:
                        self.LEFT.set_duty(35)
                        self.RIGHT.set_duty(40)
                        # self.ticks4 = ticks_ms()
                    elif ticks_diff(ticks_ms(), self.ticks4) > 200 and ticks_diff(ticks_ms(), self.ticks4) < 2500:
                        self.LEFT.set_duty(25)
                        self.RIGHT.set_duty(37.5)
                    
                elif self.done:
                    self.state = -1 
                    self.started = False
                    self.done = False
                    self.obstacle = False
            elif self.state == 5: # Returning home sequence
                # print("Returning Home")
                self.state = -1
                # Stop
                if self.return_initiated == False:
                    print("return init stuck")
                    self.return_ticks = ticks_ms()
                    self.LEFT.set_duty(0)
                    self.RIGHT.set_duty(0)
                    self.turn_around = True
                    self.Forward = False
                    self.return_initiated = True
                # Turn Around
                elif self.turn_around:
                    print("turning around")
                    self.state = -1
                    self.LEFT.set_duty(-25)
                    self.RIGHT.set_duty(25)
                    if ticks_diff(ticks_ms(), self.return_ticks) > 1500:
                        self.return_ticks = ticks_ms()
                        self.turn_around = False
                        self.forward = True
                    
                # Forward
                elif self.forward:
                    print("forward")
                    self.state = -1
                    self.LEFT.set_duty(self.speed_nor)
                    self.RIGHT.set_duty(self.speed_nor)
                    self.forward = False
                    # self.Return_Done = True
                    self.At_End = True
                    # if ticks_diff(ticks_ms(), self.return_ticks) > 1500:
                    #     self.forward = False
                    #     # self.Return_Sequence = 2
                    #     self.state = -1
                        
            elif self.state == 6:
                print("i got stuck in 6")
                self.LEFT.set_duty(0)
                self.RIGHT.set_duty(0)
                self.At_Start = False
                # self.state = -1
                
            elif self.state == 7: # Pivot Left
                self.state = -1
                if self.Sensor_T.value() != 1:
                    self.LEFT_Vel_Desired = -self.pivot - self.offset
                    self.RIGHT_Vel_Desired = self.pivot
                    # self.pivot_done = True
                    self.state = 2
                    print("turning left")

                
                    # self.pivot_done = True
            elif self.state == 8: # Pivot Right
                self.state = -1 
                if self.Sensor_T.value() != 1:
                    self.LEFT_Vel_Desired = self.pivot- self.offset
                    self.RIGHT_Vel_Desired = -self.pivot
                    # self.pivot_done = True
                    self.state = 2
                    print("turning right")
                
                # if self.Sensor_T.value() == 1:
                #     self.pivot_done = True

            yield
                        



