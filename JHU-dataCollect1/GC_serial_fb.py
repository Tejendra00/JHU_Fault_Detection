import os
import numpy as np
# from config import config
import serial
import time
from tactileRead import main


fNum = 1
# while True:
x = int(input('start iter? press ENTER'))

ser = serial.Serial('COM6', 115200)
# time.sleep(5)
r = ser.readline().decode('ascii')
main(x)
ser.close()
fNum +=1
    # print(fNum)
#     r = ser.readline().decode('ascii')

# print("START ############!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")