import numpy as np
import matplotlib.pyplot as plt
import time
from math import pi

class cleanTactileData():
    def __init__(self):
        self.filename="7.txt"
        self.timme="7.csv"
        self.numSensors = 16
        self.data_dict = { '1':[],  '2':[],  '3':[], '4':[], 
                    '5':[],  '6':[],  '7':[],  '8':[], 
                    '9':[],  '10':[], '11':[], '12':[],
                    '13':[], '14':[], '15':[], '16':[] }

        self.stats_dict = { '1':[],  '2':[],  '3':[], '4':[], 
                    '5':[],  '6':[],  '7':[],  '8':[], 
                    '9':[],  '10':[], '11':[], '12':[],
                    '13':[], '14':[], '15':[], '16':[] }
    
        self.isPlot = 0
    
    def clean(self,):
        file = open(self.filename,'r')
        self.dataset=[]
        for line in file:
            if len(line.strip().split())==16:
                self.dataset.append(line.strip().split())

                # print(len(line.strip().split()))

        for gridData in self.dataset:
            for j in range(len(gridData)):
                self.data_dict[str(j+1)].append(float(gridData[j]))

        for i in range(self.numSensors):
            # 0 - MAX , 1 - MIN , 2 - MEAN , 3 - STD
            self.stats_dict[str(i+1)].append(max(self.data_dict[str(i+1)]))
            self.stats_dict[str(i+1)].append(min(self.data_dict[str(i+1)]))
            self.stats_dict[str(i+1)].append(np.mean(self.data_dict[str(i+1)]))
            self.stats_dict[str(i+1)].append(np.std(self.data_dict[str(i+1)]))
        
        if self.isPlot:
            self._stackPlot()

        return (self.data_dict['10'])