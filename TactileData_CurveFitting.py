import matplotlib.pyplot as plt
import time
import numpy as np
from scipy.optimize import curve_fit

def test(x,a,b,c,d,e,f):
    return [a*(i**5)+b*(i**4)+c*(i**3)+d*(i**2)+e*(i)+f for i in x]
           

class CurveFit():
    def __init__(self):
        self.filename="1.txt"
        self.timme="1.csv"
        self.numSensors = 16
        self.data_dict = { '1':[],  '2':[],  '3':[], '4':[], 
                    '5':[],  '6':[],  '7':[],  '8':[], 
                    '9':[],  '10':[], '11':[], '12':[],
                    '13':[], '14':[], '15':[], '16':[] }

        self.stats_dict = { '1':[],  '2':[],  '3':[], '4':[], 
                    '5':[],  '6':[],  '7':[],  '8':[], 
                    '9':[],  '10':[], '11':[], '12':[],
                    '13':[], '14':[], '15':[], '16':[] }
        
        self.fit_dict = { '1':[],  '2':[],  '3':[], '4':[], 
                    '5':[],  '6':[],  '7':[],  '8':[], 
                    '9':[],  '10':[], '11':[], '12':[],
                    '13':[], '14':[], '15':[], '16':[] }
        

        self.isPlot = 0
        self.isFit = 0            
    
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

        if self.isFit: #if you want to do curve fitting
            self.fit()

        if self.isPlot:
            self._stackPlot()            

        return self.data_dict, self.stats_dict, self.fit_dict
    
    def _stackPlot(self,):
        figure, axis = plt.subplots(4, 4)

        for i in range(16):
            axis[i//4, i%4].plot(self.data_dict[str(i+1)], label = "Org")
            axis[i//4, i%4].plot(self.fit_dict[str(i+1)], label = "Fit")
            axis[i//4, i%4].legend(loc="upper left")
            
            #axis[i//4, i%4].plot(self.)
            axis[i//4, i%4].set_title('Sensor: '+str(i+1))
            axis[i//4, i%4].grid()
        figure.tight_layout(pad=0.1)
        plt.show()

    
    def fit(self,):
        x = range(len(self.data_dict[str(1)]))
        
        for i in range(self.numSensors):
            y = self.data_dict[str(i+1)]
            param, param_cov = curve_fit(test, x, y)
            print('Parameters for Sensor: '+str(i+1),param)
            self.fit_dict[str(i+1)] = test(x,param[0],param[1], param[2],param[3], param[4], param[5])
        
            
            
        

    

if __name__=='__main__':
    c = CurveFit()
    c.isPlot = 1
    c.isFit = 1
    c.clean()
    # a = [1,2,3,4]
    # print(test(a,1,1,1,1,1))

