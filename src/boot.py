"""!
@file boot.py
This file runs on the boot of the microcontroller. It establishes the UART
connection necessary for serial communication

TODO: N/A

@author Mech-07
@date   10-Feb-2023
@copyright (c) 2023 by Mech-07 and released under GNU Public License v3
"""
import pyb

#creates the UART connection 
pyb.repl_uart(None)