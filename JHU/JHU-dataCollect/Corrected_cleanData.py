import matplotlib.pyplot as plt
import time
import numpy as np
from math import pi
# import pyKalman
# from pyalman import KalmanFilter

class cleanTactileData():
    def __init__(self):
        self.filename="10.txt"
        self.timme="10.csv"
        self.filename1="11.txt"
        self.timme1="11.csv"
        self.numSensors = 16
        self.data_dict = { '1':[],  '2':[],  '3':[], '4':[], 
                    '5':[],  '6':[],  '7':[],  '8':[], 
                    '9':[],  '10':[], '11':[], '12':[],
                    '13':[], '14':[], '15':[], '16':[] }
        self.data_dict1 = { '1':[],  '2':[],  '3':[], '4':[], 
                    '5':[],  '6':[],  '7':[],  '8':[], 
                    '9':[],  '10':[], '11':[], '12':[],
                    '13':[], '14':[], '15':[], '16':[] }
        self.stats_dict = { '1':[],  '2':[],  '3':[], '4':[], 
                    '5':[],  '6':[],  '7':[],  '8':[], 
                    '9':[],  '10':[], '11':[], '12':[],
                    '13':[], '14':[], '15':[], '16':[] }
        self.a = { '1':[],  '2':[],  '3':[], '4':[], 
                    '5':[],  '6':[],  '7':[],  '8':[], 
                    '9':[],  '10':[], '11':[], '12':[],
                    '13':[], '14':[], '15':[], '16':[] }
    
        self.isPlot = 0
       
    
    def clean(self,):
        file = open(self.filename,'r')
        file1= open(self.filename1,'r')
        self.dataset=[]
        self.dataset1=[]
        for line in zip(file,file1):
            if len(line[0].strip().split())==16:
                self.dataset.append(line[0].strip().split())
                self.dataset1.append(line[1].strip().split())    
                # print(len(line.strip().split()))
        

        for gridData in zip(self.dataset,self.dataset1):
            for j in range(len(gridData[0])):
                self.data_dict[str(j+1)].append(float(gridData[0][j]))
                self.data_dict1[str(j+1)].append(float(gridData[1][j]))
        
        # for i in range(self.numSensors):
        #     # 0 - MAX , 1 - MIN , 2 - MEAN , 3 - STD
        #     self.stats_dict[str(i+1)].append(max(self.data_dict[str(i+1)]))
        #     self.stats_dict[str(i+1)].append(min(self.data_dict[str(i+1)]))
        #     self.stats_dict[str(i+1)].append(np.mean(self.data_dict[str(i+1)]))
        #     self.stats_dict[str(i+1)].append(np.std(self.data_dict[str(i+1)]))
        
        for i in range(self.numSensors):
            self.a[str(i+1)].append(list(np.subtract(self.data_dict[str(i+1)],self.data_dict1[str(i+1)])))
        if self.isPlot:
            self._stackPlot()
        return self.a

    def _stackPlot(self,):
        figure, axis = plt.subplots(4, 4)
        print(self.a)
        for i in range(16):
            axis[i//4, i%4].plot(self.a[str(i+1)])
            # axis[i//4, i%4].plot(self.)
            axis[i//4, i%4].set_title('Sensor: '+str(i+1))
            axis[i//4, i%4].grid()
        figure.tight_layout(pad=0.1)
        plt.show()

if __name__=='__main__':
    c = cleanTactileData()
    c.isPlot = 1
    c.clean()
