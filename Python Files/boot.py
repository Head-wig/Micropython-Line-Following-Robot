from pyb import Pin


# Right motor
B8 = Pin(Pin.cpu.B8, mode = Pin.OUT_PP)# PWM Pin
B0 = Pin(Pin.cpu.B0, mode = Pin.OUT_PP)# En Pin
A4 = Pin(Pin.cpu.A4, mode = Pin.OUT_PP)# Dir Pin

# Left motor
C8 = Pin(Pin.cpu.C8, mode = Pin.OUT_PP) # PWM Pin
A10 = Pin(Pin.cpu.A10, mode = Pin.OUT_PP) # EN Pin
B3 = Pin(Pin.cpu.B3, mode = Pin.OUT_PP) # Dir Pin

# Disable them
B8.low() # PWM Pin
B0.low() # En Pin
A4.low() # Dir Pin

C8.low() # PWM Pin
A10.low() # EN Pin
B3.low()# Dir Pin
