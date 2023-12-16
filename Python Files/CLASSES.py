from pyb import Pin,Timer
from time import sleep_ms, ticks_ms, ticks_diff
from array import array
import micropython
from machine import I2C
micropython.alloc_emergency_exception_buf(100)

def Convert_byte(byte_data): # Convert data into one readable integer
    integer_value = 0
    
    for byte in byte_data:
        integer_value = (integer_value << 8) | byte
    return integer_value  

class Motor:
    '''!@brief A driver class for one channel of the L6206.
    @details Objects of this class can be used to apply PWM to a given
    DC motor on one channel of the L6206 from ST Microelectronics.
    '''

    def __init__ (self, PWM_tim, IN1_pin, IN2_pin, EN_pin ):
        '''!@brief Initializes and returns an object associated with a DC motor.
        '''
        # Creates a pin object from the enable pin specified as an input parameter, and then stores the pin object in a calss attributes
        self.timer = PWM_tim
        self.pwm_1 = PWM_tim.channel(3, pin = IN1_pin, mode =Timer.PWM,  pulse_width_percent = 0)
        self.Dir = Pin(IN2_pin, mode = Pin.OUT_PP)
        self.EN = Pin(EN_pin, mode = Pin.OUT_PP)
        
 
    def set_duty (self, duty):
        '''!@brief Set the PWM duty cycle for the DC motor2
        @details This method sets the duty cycle to be sent
        to the L6206 to a given level. Positive values
        cause effort in one direction, negative values
        in the opposite direction.
        @param duty A signed number holding the duty
        cycle of the PWM signal sent to the L6206
        '''
        # IN2 stays constant and pwm_1 is fluctuating values wise
       
        if(duty > 100):
            duty = 100
        elif(duty < -100):
            duty = -100
        # turns on pwm constantly
       
        if duty >= 0:
            self.pwm_1.pulse_width_percent(abs(duty))
            self.Dir.low()
        elif duty < 0:
            self.pwm_1.pulse_width_percent(abs(duty))
            self.Dir.high()
            
    
   
    def enable (self):
        '''!@brief Enable one channel of the L6206.
        @details This method sets the enable pin associated with one
        channel of the L6206 high in order to enable that
        channel of the motor driver.
        '''
        self.EN.high()
        
    def disable (self):
        self.EN.low()
                                
   
class Encoder:

    '''!@brief Interface with quadrature encoders

    @details Objects of this class can be used to read quadrature encoder,
    allowing the position and the change in position to be seen, thereby velocity
    as well.

    '''

    def __init__(self, enc_timer, channelA_Pin, channelB_Pin):
        '''!@brief Constructs an encoder object
        @details This method initializes the class and reset all input parameters
         The reload value and prescale value are set.
        @param enc_timer set up the timer for the channel
        @param channelA_Pin set up the serial communication for channel A
        @param channelB_Pin set up the serial communication for channel A
        '''

        #self.AR = 256*4*16 - 1
        self.AR = 1440 - 1
        self.PS = 0
        self.Delta = 0
        self.position = 0
        self.value = 0
        self.time =  Timer(enc_timer, period = self.AR, prescaler = self.PS)
        self.channelA = self.time.channel(1, pin = channelA_Pin, mode = Timer.ENC_AB)
        self.channelB = self.time.channel(2, pin = channelB_Pin, mode = Timer.ENC_AB)
        self.lastvalue = self.time.counter()

    def update(self):
        '''!@brief Updates encoder position and delta
        @details Get current position from encoder read. If the difference betweeen
        the current value and the last value to be greater than 15000, add the
        auto reload value to the position then subtract the previous position value.
        Otherwise, subtract current position by the previous position for delta.
        Then,current position is saved as the previous position for the next loop cycle
        '''
        self.value = self.time.counter()
        self.Delta = self.value - self.lastvalue
        if self.Delta > (self.AR + 1)//2:
            self.Delta -= self.AR + 1
        elif self.Delta < -(self.AR + 1)//2:
            self.Delta += self.AR +1
       
        self.lastvalue = self.value
       
        self.position = self.position + self.Delta
       
        pass

    def get_position(self):
        '''!@brief Gets the most recent encoder position
        @detaelf.NewVal ils Get the numerical result from update() and print value
        @return printed motor position
        '''
        print(self.position)
       
   
    def get_delta(self):
        '''!@brief Gets the most recent encoder delta
        @details Get the numerical result from update() and print delta
        @return printed motor position difference
        '''
        print(self.Delta)

    def zero(self):
        '''!@brief Resets the encoder position to zero
        @details reset the delta, position, and last position value of
        the motor to zero
        '''
        self.Delta = 0
        self.postion = 0
        self.value = 0
        pass
    
    
class ClosedLoop_Left:
    def __init__(self, CurrentVelocity, SetVelocity, P_Gain, I_Gain, D_Gain):
        self.CurrentVel = CurrentVelocity
        self.SetVel = SetVelocity 
        self.Gain = P_Gain, I_Gain, D_Gain
        self.newval = 0 
        self.time = 0
        self.time_previous = 0
        self.error = 0
        self.error_previous = 0
        self.I_term = 0
        
    def updategain(self,P_Gain, I_Gain, D_Gain):
        self.kp = P_Gain
        self.ki = I_Gain
        self.kd = D_Gain
    def updatevel(self,NewVel):
        self.SetVel = NewVel
    
    def Run(self, CurentVelocity):
        self.time = ticks_ms()
        self.CurrentVel = CurentVelocity
        self.error = self.SetVel - self.CurrentVel
        self.P_term = self.kp*self.error
        self.I_term = self.I_term + self.ki*self.error*ticks_diff(self.time,self.time_previous)
        if abs(self.I_term) > 10:
            if self.I_term < 0:
                self.I_term = -10
            else:
                self.I_term = 10
        self.D_term = self.kd*(self.error - self.error_previous) / (self.time-self.time_previous)
        print(self.P_term, self.I_term, self.D_term)
        self.NewVal = (self.P_term + self.I_term + self.D_term)#/5.522
        self.error_previous = self.error
        self.time_previous = self.time
        if self.NewVal > 100:
            self.NewVal = 100
        elif self.NewVal < -100:
            self.NewVal = -100
            
class ClosedLoop_Right:
    def __init__(self, CurrentVelocity, SetVelocity, P_Gain, I_Gain, D_Gain):
        self.CurrentVel = CurrentVelocity
        self.SetVel = SetVelocity 
        self.Gain = P_Gain, I_Gain, D_Gain
        self.newval = 0 
        self.time = 0
        self.time_previous = 0
        self.error = 0
        self.error_previous = 0
        self.I_term = 0
        
    def updategain(self,P_Gain, I_Gain, D_Gain):
        self.kp = P_Gain
        self.ki = I_Gain
        self.kd = D_Gain
    def updatevel(self,NewVel):
        self.SetVel = NewVel
    
    def Run(self, CurentVelocity):
        self.time = ticks_ms()
        self.CurrentVel = CurentVelocity
        self.error = self.SetVel - self.CurrentVel
        self.P_term = self.kp*self.error
        self.I_term = self.I_term + self.ki*self.error*ticks_diff(self.time,self.time_previous)
        if abs(self.I_term) > 10:
            if self.I_term < 0:
                self.I_term = -10
            else:
                self.I_term = 10
        self.D_term = self.kd*(self.error - self.error_previous) / (self.time-self.time_previous)
        self.NewVal = (self.P_term + self.I_term + self.D_term)#/5.522
        self.error_previous = self.error
        self.time_previous = self.time
        if self.NewVal > 100:
            self.NewVal = 100
        elif self.NewVal < -100:
            self.NewVal = -100
            
class BMO:
   
    def __init__(self):
        # Initializer that takes in a pyb.I2C object preconfigured in CONTROLLER mode
        self.i2c = I2C(3, freq = 200000)
        self.BNO_Address = 40 # alternative address 0x28
        self.MODE_Addr = 61# Mode address 0x3D
        
    def Mode(self, mode):
        # A method to change the operating mode of the IMU and parse it into its individual statuses
        # i2c.mem_write(data, addr, memaddr, timeout = 5000, addr_size = 8 )

        # NDOF will be the one used
        self.i2c.writeto_mem(self.BNO_Address, self.MODE_Addr, bytearray([mode]))       

    def Get_Calibration_Status(self):
        # A method to retrieve the calibration status byte from the IMU and parse it into its statuses
        # For reading calibration, 0x35
        # if we read 3: fully calib, 0 = not calibrated
        self.CalibVals  = Convert_byte(self.i2c.readfrom_mem(40, 53, 1))
        self.Systemcoef = ((self.CalibVals >> 6) & 0b11)
        self.Gyrocoef   = ((self.CalibVals >> 4) & 0b11)
        self.Accelcoef  = ((self.CalibVals >> 2) & 0b11)
        self.Magcoef    = (self.CalibVals & 0b11)
        
        return self.Systemcoef, self.Gyrocoef, self.Accelcoef, self.Magcoef
                
    def Get_Calibration_Coefficients(self):   
        # A method to retrieve the calibration coefficients from the IMU as an array of packed binary data
        # self.Calib_Coef = Convert_byte(self.i2c.readfrom_mem(40, 85, 22)) # 0x55
        self.Calib_Coef = (self.i2c.readfrom_mem(40, 85, 22))
        
        return self.Calib_Coef

    def Read_Euler_Angles(self):   
        # A method to read Euler angles from the IMU to use as measurements for feedback

        self.Euler_x = Convert_byte(self.i2c.readfrom_mem(40, 27, 1) + self.i2c.readfrom_mem(40, 26, 1)) # read LSB and MSB (in such order)
        self.Euler_y = Convert_byte(self.i2c.readfrom_mem(40, 27, 1) + self.i2c.readfrom_mem(40, 26, 1))
        self.Euler_z = Convert_byte(self.i2c.readfrom_mem(40, 31, 1) + self.i2c.readfrom_mem(40, 30, 1))
        self.Euler = Convert_byte(self.i2c.readfrom_mem(40, 27, 1))
        print("Euler:" , self.i2c.readfrom_mem(40, 27, 1) + self.i2c.readfrom_mem(40, 26, 1) , self.i2c.readfrom_mem(40, 27, 1) + self.i2c.readfrom_mem(40, 26, 1), self.i2c.readfrom_mem(40, 31, 1) + self.i2c.readfrom_mem(40, 30, 1))
        return self.Euler_x, self.Euler_y, self.Euler_z, self.Euler  # Return value all at once as a list
        
    def Read_Angular_Velocity(self):    
        # A method to read angular velocity from the IMU to use as measurements for feedback

        self.Gyro_x = Convert_byte(self.i2c.readfrom_mem(40, 21, 2) + self.i2c.readfrom_mem(40, 20, 2)) # read LSB and MSB (in such order)
        self.Gyro_y = Convert_byte(self.i2c.readfrom_mem(40, 23, 2) + self.i2c.readfrom_mem(40, 22, 2))
        self.Gyro_z = Convert_byte(self.i2c.readfrom_mem(40, 25, 2) + self.i2c.readfrom_mem(40, 24, 2))
        print("Gyro: " , self.i2c.readfrom_mem(40, 21, 2) + self.i2c.readfrom_mem(40, 20, 2) , self.i2c.readfrom_mem(40, 23, 2) + self.i2c.readfrom_mem(40, 22, 2), self.i2c.readfrom_mem(40, 25, 2) + self.i2c.readfrom_mem(40, 24, 2))
        return self.Gyro_x, self.Gyro_y, self.Gyro_z # Return value all at once as a list

