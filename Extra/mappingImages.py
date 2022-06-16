import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm
from get3Dmap import CoordinateDesc
import cv2

class mapPoints():
    def __init__(self,className = '3_Bumps', saveloc = '.'):
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
        self.saveloc = saveloc
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
        self.vel = 10 # Data cleaned such that we only take y-direction as our input

        # File Params
        self.dataset_dir = './Datasets/vel600'
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
        self.imgdim = 32
        self.imgName = 0
    
    def reset(self,):

        self.class_dir = os.path.join(self.dataset_dir, self.className)
        if self.className!='plain':
            self.pat = self.className.split('_')[1]
            self.num = int(self.className.split('_')[0])
        else:
            self.pat = self.className
            self.num = 0
    
    def move(self,t_prev, t):

        dist = self.vel*(t-t_prev)
        self.yloc +=dist
        return 0
            
            
    def _genImg(self,):
        xstart = self.xloc - 32*3/16
        ystart = self.yloc - 32*3/16

        img = np.zeros((self.imgdim,self.imgdim))
        for i in range(self.imgdim):
            for j in range(self.imgdim):
            # pass    
                z = self.zDescriptor.get_Z_coord([np.round(xstart + j*3/8,3),np.round(ystart + i*3/8,3)])
                # print((z+2.5)/5)
                img[i][j] = (z+2.5)/5
        

        img = cv2.resize(img, (128,128))
        cv2.imshow('img',img)
        cv2.waitKey(1)
    
    def generateImages(self,iterNum):
        self.reset()
        self.zDescriptor = CoordinateDesc(pat = self.pat, num = self.num)
        iterPath = os.path.join(self.class_dir,str(iterNum))
        
        
        tprev = 0
        # self.sensorPos_update(reset=True)

        if self.verbose:
            print("Generating Images for : ", self.className +' | Iteration Number: ',str(iterNum) +'...')
        for fileNum in tqdm(os.listdir(iterPath), total=8*2+1):
            if fileNum.endswith('.csv'):
                filePath = os.path.join(iterPath, fileNum)
                df = pd.read_csv(filePath)

                for index,row in df.iterrows():
                    t = df['Time'][index]
                    if self.yloc < 108:
                        print(self.yloc)
                        if t>self.faltuTime:
                            self.move(tprev, t)
                            if self.yloc>40:
                                self._genImg()
                        tprev = t
                    else:
                        self.yloc = 0
                        self.xloc = self.xloc + self.xShift
                        tprev = 0
                        break
                # exit()

                        # for key in self.queuePos.keys():
                        #     self.sensorPos[key].append(self.queuePos[key])
                        #     self.queuePos[key] = []
                        # break
        # print(len(self.sensorPos['1']))
        # return self.sensorPos





if __name__=='__main__':
    map = mapPoints('4_Waves')    

    # pointmap = map.generateImages(2)    

    # print(pointmap['1'][500:550])