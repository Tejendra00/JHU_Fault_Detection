import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm
from .get3Dmap import CoordinateDesc
import cv2

class mapPoints():
    def __init__(self,className = '3_Bumps'):
        '''
        13 14 15 16
         9 10 11 12
         5  6  7  8
         1  2  3  4

         y
         ^
         |
         |
         |
         |------------> x
         (0,0)

        '''

        self.sensorWidth = 2 # mm
        self.sensorSpacing = 1 # mm

        self.specimenWidth = 36 # x-direction
        self.specimenLength = 108 # y-direction
        self.xShift = 5 # distance moved in shift pass 
        self.sensorPos = { '1':[],  '2':[],  '3':[],  '4':[],
                           '5':[],  '6':[],  '7':[],  '8':[],
                           '9':[], '10':[], '11':[], '12':[],
                          '13':[], '14':[], '15':[], '16':[]}
                          
        self.queuePos = { '1':[],  '2':[],  '3':[],  '4':[],
                            '5':[],  '6':[],  '7':[],  '8':[],
                            '9':[], '10':[], '11':[], '12':[],
                            '13':[], '14':[], '15':[], '16':[]}
        # Finger params
        self.xloc = 0
        self.yloc = 0
        self.vel = 5 # Data cleaned such that we only take y-direction as our input

        # File Params
        self.dataset_dir = 'E:/rwik stuff/PROJECTS/JHU/JHU-Intern/Present-Work/Main Code/DataCollection/Datasets/vel300'
        # self.dataset_dir = './DataCollection/Datasets/vel600'

        self.className = className
        self.class_dir = os.path.join(self.dataset_dir, self.className)
        if className!='plain':
            self.pat = self.className.split('_')[1]
            self.num = int(self.className.split('_')[0])
        else:
            self.pat = self.className
            self.num = 0
        
        
        
        self.faltuTime = 0.67 # removed 500 time steps for vel 6000
        self.verbose = 1
        self.imageNum = 0
        self.imgdim = 32
    
    def reset(self,):

        self.class_dir = os.path.join(self.dataset_dir, self.className)
        if self.className!='plain':
            self.pat = self.className.split('_')[1]
            self.num = int(self.className.split('_')[0])
        else:
            self.pat = self.className
            self.num = 0
        
        self.sensorPos = { '1':[],  '2':[],  '3':[],  '4':[],
                           '5':[],  '6':[],  '7':[],  '8':[],
                           '9':[], '10':[], '11':[], '12':[],
                          '13':[], '14':[], '15':[], '16':[]}
                          
        self.queuePos = { '1':[],  '2':[],  '3':[],  '4':[],
                            '5':[],  '6':[],  '7':[],  '8':[],
                            '9':[], '10':[], '11':[], '12':[],
                            '13':[], '14':[], '15':[], '16':[]}
    
    def move(self,t_prev, t):

        dist = self.vel*(t-t_prev)
        self.yloc +=dist
        return 0
    
    def _genImg(self,):
        xstart = self.xloc - 32*3/16
        ystart = self.yloc - 32*3/16

        img = np.zeros((self.imgdim,self.imgdim))
        # smallimg = np.zeros((self.imgdim//8,self.imgdim//8))

        for i in range(self.imgdim):
            for j in range(self.imgdim):
            # pass    
                z = self.zDescriptor.get_Z_coord([np.round(xstart + j*3/8,3),np.round(ystart + i*3/8,3)])
                # print((z+2.5)/5)
                img[i][j] = (z+2.5)/5

        cv2.imwrite('3_Bumps/'+str(self.imageNum)+'.jpg',255*img)
        self.imageNum += 1
        # cv2.waitKey(1)
            
    def sensorPos_update(self,reset=False,t = 0,v = None):
        # Initial position of first sensor
        if reset==True:
            self.xloc = 0
            self.yloc = 0

        # print('yo')

        x1 = -3/2*(self.sensorWidth + self.sensorSpacing) + self.xloc
        y1 = -3/2*(self.sensorWidth + self.sensorSpacing) + self.yloc

        for sensorNum in self.queuePos.keys():
            if reset:
                self.queuePos[sensorNum] = [] # re-initializing
            else:
                if (int(sensorNum)-1)%4!=0 or (int(sensorNum)-1)==0:
                    xCent = x1 + ((int(sensorNum)-1)%4)*(self.sensorWidth + self.sensorSpacing)
                    yCent = y1                
                else:
                    xCent = x1
                    y1 = y1 + (self.sensorWidth + self.sensorSpacing)
                    yCent = y1
                z = self.zDescriptor.get_Z_coord([np.round(xCent,3),np.round(yCent,3)])
                # X,Y,voltage,T
                self.queuePos[sensorNum].append([np.round(xCent,3),np.round(yCent,3), z, v[str(int(sensorNum)-1)],t, self.xloc, self.yloc])    
    
    def pointMap(self,iterNum, passNo):
        self.reset()
        self.zDescriptor = CoordinateDesc(pat = self.pat, num = self.num)
        iterPath = os.path.join(self.class_dir,str(iterNum))
        
        
        check = 0
        
        tprev = 0
        self.sensorPos_update(reset=True)

        if self.verbose:
            print("Generating X-Y-Z-V-T map for : ", self.className +' | Iteration Number: ',str(iterNum) +'...')
        # for fileNum in tqdm(os.listdir(iterPath), total=8*2+1):
        # if fileNum.endswith('.csv'):
        # # if fileNum=='5.csv':
        filePath = os.path.join(iterPath, str(passNo+1)+'.csv')
        df = pd.read_csv(filePath)

        for index,row in tqdm(df.iterrows(), total=df.shape[0]):
            t = df['Time'][index]
            voldata = row
            if self.yloc < 108:
                if t>self.faltuTime:

                    self.move(tprev, t)           
                    self.sensorPos_update(t=t,v = voldata)
                    # if self.yloc > 40:

                    # self._genImg()

                tprev = t
            else:
                self.yloc = 0
                self.xloc = self.xloc + self.xShift
                tprev = 0

                for key in self.queuePos.keys():
                    self.sensorPos[key].append(self.queuePos[key])
                    self.queuePos[key] = []
                check = 1
                break
                
        # print(len(self.sensorPos['1']))

        a = self.sensorPos.copy()
        if check:
            return a
        else:
            for key in self.queuePos.keys():
                self.queuePos[key] = [self.queuePos[key]]
            
            a = self.queuePos.copy()
            return a





if __name__=='__main__':
    map = mapPoints()    

    pointmap = map.pointMap(2)    

    print(pointmap['1'][500:550])