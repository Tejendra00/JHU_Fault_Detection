import os, sys, glob
sys.path.append('./framework/libraries/general')
sys.path.append('./framework/libraries/neuromorphic')

import time
from threading import Thread, Lock #control access in threads
from copy import copy #useful for copying data structures

from frameworks.libraries.neuromorphic.tactileboard import * #tactile board library
from frameworks.libraries.general.threadhandler import ThreadHandler #manage threads

def init_tactile():
    global tactileBoard
    thMain = ThreadHandler(tactile_update)
    tactileBoard = TactileBoard('COM12',_sensitivity=TBCONSTS.DEFAULT_SENS)
    tactileBoard.start()
    thMain.start()
    # tactileBoard.startCalibration(1000) #ask for 1000 samples --> 1s calibration
    # time.sleep(2) #make sure that you wait for calibration to be finished
    # tactileBoard.loadCalibration()
    # tactileBoard.useCalib = True
    print('--TACTILE READY--')

def tactile_update():
    global tactileBoard, dataQueue, fileHandler, taxel_array
    taxel_array=[]
    dataQueue = tactileBoard.getData()
    if (len(dataQueue)>0):
        n = len(dataQueue)
        for k in range(n):
            # print(dataQueue)
            try:
                data = dataQueue.popleft()
                for i in range(TBCONSTS.NROWS): #number of rows
                    for j in range(TBCONSTS.NCOLS):
                        taxel = data[0][i][j] #this is normalized value
                        rawv = tactileBoard.conv2raw(taxel,0,i,j)
                        fileHandler.write(str(rawv) + ' ') #write the normalized value to the file
                    #  print(rawv)
                        taxel_array.append(rawv)
                fileHandler.write('\n') #new line
            except:
                pass
    time.sleep(0.001)
    return taxel_array

'''
see from horizontal

1 5  9 13
2 6 10 14
3 7 11 15
4 8 12 16

'''
def main(fNum):
    global fileHandler
    st = time.time()
    init_tactile()

    filename = str(fNum)+".txt"
    fileHandler = open(filename,'w')
    t1=time.time()
    init_time = t1 -st
    print("Initialisation time: " , str(init_time))
    t2=t1
    Time=[]
    while(t2-t1<4):

        tactile_update()
        Time.append(t2-t1)
        t2=time.time()

    fileHandler.close()

        # fNum+=1
    

if __name__ == '__main__':
	main(11)
