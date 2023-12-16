




# WARNING

# UNFINISHED FILE DO NOT USE









# import time
# from time import ticks_ms, ticks_diff
# from CLASSES import BMO
# import pyb
# from machine import I2C
# from array import array
# # from numpy import array, arange, zeros, transpose
# from math import pi, cos, sin

# class appa_return: # Calibrating the IMU, use IMU readings to make prediction
#     def __init__(self, Appa_Mode, Left_Wheel_RPM, Right_Wheel_RPM, X_Distance, Y_Distance, DEBUG_VAL):
#         self.state = 0      
#         self.Appa_Mode = Appa_Mode
#         self.Left_Wheel_RPM = Left_Wheel_RPM
#         self.Right_Wheel_RPM = Right_Wheel_RPM
#         self.Appa_Mode = DEBUG_VAL
#         self.X_Distance = X_Distance
#         self.Y_Distance = Y_Distance
#         # Wheel Parameters
#         self.R         = 70/1000/2     # The wheel radius   [m]
#         self.L         = (74.39-(8/2))/1000/2  # Distance from center of Romi to center of the wheel [m]

#         self.x_distance = 0
#         self.y_distance = 0
#     def differential_drive_eqn(self,t,x):
        
#         self.Thd_Left = self.Left_Wheel_RPM.get()   # rad/s
#         self.Thd_Right = self.Right_Wheel_RPM.get()  # rad/s
        
#         self.phi_dot = (self.R/(2*self.L)) * (-self.Thd_Left+ self.Thd_Right)
#         self.phi = x[2]
        
#         self.X_R_dot = (self.R/2)*cos(self.phi)*(self.Thd_Left+ self.Thd_Right)  
#         self.Y_R_dot = (self.R/2)*sin(self.phi)*(self.Thd_Left+ self.Thd_Right)
        
#         self.x_dot = array([ [self.X_R_dot],
#                               [self.Y_R_dot],
#                               [self.phi_dot]
#                                             ])

#         self.y     = array([ [x[0]],
#                               [x[1]],
#                               [x[2]]
#                                       ])

#         return self.x_dot, self.y    
    
#     def RK4_solver(self, fcn, x_0, tspan, tstep):
#         '''!@brief        Implements a first-order forward euler solver
#             @param fcn    A function handle to the function to solve
#             @param x_0    The initial value of the state vector
#             @param tspan  A span of time over which to solve the system specified as a list
#                           with two elements representing initial and final time values
#             @param tstep  The step size to use for the integration algorithm
#             @return       A tuple containing both an array of time values and an array
#                           of output values
#         '''
        
#         # Define a column of time values
#         tout = arange(tspan[0], tspan[1]+tstep, tstep)
    
#         # Preallocate an array of zeros to store state values
#         xout = zeros([len(tout)+1,len(x_0)])
        
#         # Determine the dimension of the output vector
#         r = len(fcn(0,x_0)[1])
        
#         # Preallocate an array of zeros to store output values
#         yout = zeros([len(tout),r])
    
#         # Initialize output array with intial state vector
#         xout[0][:] = x_0.T
        
#         # Iterate through the algorithm but stop one cycle early because
#         # the algorithm predicts one cycle into the future
#         for n in range(len(tout)):
            
#             # Pull out a row from the solution array and transpose to get
#             # the state vector as a column
#             x = xout[[n]].T
            
#             # Pull out the present value of time
#             t = tout[n]
            
#             # Runge Kutta Method 
            
#             K_1, y_1 = fcn(t, x) # f(t,x_n)
#             K_2, y_2 = fcn(t + .5*tstep, x + .5*K_1*tstep) # f(t + .5*dt, x_n +.5*K1*dt)
#             K_3, y_3 = fcn(t + .5*tstep, x + .5*K_2*tstep) # f(t + .5*dt, x_n +.5*K2*dt)
#             K_4, y_4 = fcn(t +  1*tstep, x +  1*K_3*tstep) # f(t +    dt, x_n +   K3*dt)
            
#             # x_n+1 = 1/6*(K1 + 2*K2 + 2*K3 *K4)*tstep
                
#             xout[n+1] = xout[n] + (1/6*(K_1 + 2*K_2 + 2*K_3 + K_4)).T*tstep
#             yout[n] = y_1.T
        
#         return tout, yout

#     def run(self):
#         while True:
#             if self.state == 0: # state 0, check if Appa is ready to return
#                 self.ticks_interval = ticks_ms
#                 if self.Appa_Mode.get() == 10: # Tracking where Appa is
#                     self.state = 1
#                     self.ticks_interval = ticks_ms()
#                 elif self.Appa_Mode.get() == 20: # Compile Appa's final location
#                     self.state = 2
#             elif self.state == 1: # Track where Appa is
#                 t_RK, y_RK = self.RK4_solver(self.differential_drive_eqn, self.x_0, [0,ticks_diff(ticks_ms, self.ticks_interval)], 1e-5)
#                 self.x_distance += y_RK[-1,0]  # Append the last value
#                 self.y_distance += y_RK[-1,1]  # Append the last value
#                 print(self.x_distance, self.y_distance)
#             elif self.state == 2: # Give Appa's final location
#                 self.state = 0
                                     
#             yield
                        


