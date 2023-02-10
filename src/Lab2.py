"""!
@file Lab1.py
This file contains code which initializes a motors encoder connected to the designated pins
using the encoder_reader class. Then it initializes the motor driver using the motor_driver
class. After both are initialized, the program gives the motor a set of duty cycles to run for 2 seconds each.
Finally, the encoder is called to read position every .5 seconds.

TODO:  Test edge cases

@author Mech-07
@date   2-Feb-2023
@copyright (c) 2023 by Mech-07 and released under GNU Public License v3
"""

import pyb
import utime

import motor_driver    #Classes we have written for driving the motor and reading the encoder
import encoder_reader
import porportional_controller

def main():
    """!
    Main code of program which initializes the encoder, the motor driver, runs the motor through a series of pwm speeds,
    then prints the encoder output every .5 seconds.
    
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
    
    
    
    data_x = []
    data_y = []
    
    u2 = pyb.UART(2, baudrate=115200, timeout= 50)
    
    #logic for checking for user input 
    kp = 0
    while kp == 0 or kp == None:
        kp = u2.readline()
    
    kp = float(kp)
    
    encode.zero()
    controller = porportional_controller.PorportionalController(kp)
    
    
    inittime = utime.ticks_ms()
    time = [0]
    pos = [0]

    while (utime.ticks_ms() - inittime <= 2000):
            
        if ((utime.ticks_ms() - inittime)%10 == 0):
            
            position = encode.read()
            control_output = controller.run(1000, position)

            #print(control_output)
            moe.set_duty_cycle(control_output)
                
            time.append(utime.ticks_ms() - inittime)
            pos.append(position)
            
            utime.sleep_ms(5)
            print(position)
            
    i = 0
    
    while i <= 200:
        
        timedata = bytes(time[i])
        posdata = bytes(pos[i])
        u2.write(f"{timedata},{posdata}\r\n")
        print(pos[i])
        
        i+=1


if __name__ == "__main__":
    main()
        