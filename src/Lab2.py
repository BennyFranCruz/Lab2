"""!
@file Lab2.py
This file contains code which initializes a motors encoder connected to the designated pins
using the encoder_reader class. Then it initializes the motor driver using the motor_driver
class. After both are initialized, the program waits to recieve a Kp value from the ST_link.
After the Kp value is recieved, the program performs a step response test with the given Kp value
with a given goal position. After this test is performed, the recorded data of time vs motor
position is sent back over the ST_Link connection.

TODO:  Clean up code

@author Mech-07
@date   10-Feb-2023
@copyright (c) 2023 by Mech-07 and released under GNU Public License v3
"""

import pyb
import utime

import motor_driver    #Classes we have written for driving the motor, reading the encoder, and calculating porportional control
import encoder_reader
import porportional_controller

def main():
    """!
    Main code of program which initializes the encoder, the motor driver, waits for Kp value to be sent over ST_link, runs a step response
    test using said Kp value, then sends the test results back over the KP_link.
    
    @param   Always when run as "__main__"
    @returns none
    """
    
    #Encoder initializing. Includes defining the timer and the pins for our encoder class
    pinB6 = pyb.Pin(pyb.Pin.board.PB6, pyb.Pin.IN)
    pinB7 = pyb.Pin(pyb.Pin.board.PB7, pyb.Pin.IN)
    timer = pyb.Timer(4, prescaler=0, period=0xFFFF)
    ch1 = timer.channel (1, pyb.Timer.ENC_AB, pin=pinB6)
    ch2 = timer.channel (2, pyb.Timer.ENC_AB, pin=pinB7)
    
    #calling the encoder class, then calling the zero() function to zero the encoder
    encode = encoder_reader.Encoder(pinB6, pinB7, timer, ch1, ch2)
    
    
    #Motor driver initializing. Includes defining pin and setting up the PWM timer
    pinB4 = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
    pinB5 = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
    pinA10 = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
    timer = pyb.Timer (3, freq=10000)
     
    #calling the motor driver class and giving the object name "moe"
    moe = motor_driver.MotorDriver(pinA10,pinB4,pinB5, timer)
    
    #initializing the UT_Link to be used by the board
    u2 = pyb.UART(2, baudrate=115200, timeout= 50)
    
    #logic for continuously checking the UT_link waiting for a kP value
    kp = 0
    while kp == 0 or kp == None:
        kp = u2.readline()
    
    kp = float(kp)
    
    #Zeroing the encoder, and preparing the porportional controller for use
    encode.zero()
    controller = porportional_controller.PorportionalController(kp)
    
    #Initializing a timer to time the test
    inittime = utime.ticks_ms()
    time = [0]
    pos = [0]

    #while loop that loops while the timer is less than its goal time
    while (utime.ticks_ms() - inittime <= 3000):
          
        #when the timer is a multiple of ten, the p controller is called to update the
        #motors PWM control. This data is then saved 
        if ((utime.ticks_ms() - inittime)%10 == 0):
            
            position = encode.read()
            control_output = controller.run(3000, position)

            #print(control_output)
            moe.set_duty_cycle(control_output)
                
            time.append(utime.ticks_ms() - inittime)
            pos.append(position)
            
            utime.sleep_ms(5)
            #print(position)
    
    #Logic for sending the test data back over the ST_Link. Values are sent one line at a time
    #to be recieved by the second CPU.
    i = 0
    while i <= 300:
        timedata = time[i]
        posdata = pos[i]
        u2.write(f'{timedata},{posdata}\r\n') 
        i+=1
        
    u2.write(f'end,end\r\n')


if __name__ == "__main__":
    main()
        