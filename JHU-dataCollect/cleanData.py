import matplotlib.pyplot as plt
import time
import numpy as np
from scipy.signal import lfilter
from scipy.optimize import curve_fit

def test(x,a,b,c,d,e,f):
    return [a*(i**5)+b*(i**4)+c*(i**3)+d*(i**2)+e*(i)+f for i in x]

class cleanTactileData():
    def __init__(self):
        self.filename="12.txt"
        self.timme="12.csv"
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

        # self.data_dict['1']=self.data_dict['1']*5
        
        return self.data_dict, self.stats_dict

    def _stackPlot(self,):
        # plt.ylim(1.9,2.45)
        figure, axis = plt.subplots(4, 4)
        n = 120 # the larger n is, the smoother curve will be
        b = [1.0 / n] * n
        a = 1
        
        param_mat=np.zeros((4,4,6))
        
        for i in range(16):
            # yy=lfilter(b,a,self.data_dict[str(i+1)])
            # f1=open('filea{}.txt'.format(i+1),'w')
            # f2=open('fileb{}.txt'.format(i+1),'w')
            # f1.writelines(str(self.data_dict[str(i+1)]))
            # f2.writelines(str(yy))
            # f1.close()
            # f2.close()
            param,param_cov=curve_fit(test,range(len(self.data_dict[str(i+1)])),self.data_dict[str(i+1)])
            fit_dict=test(range(len(self.data_dict[str(i+1)])),param[0],param[1], param[2],param[3], param[4], param[5])
            for j in range(6):
                param_mat[i//4][i%4][j]=param[j]
            axis[i//4, i%4].plot(self.data_dict[str(i+1)])
            # axis[i//4, i%4].plot(yy[300:],c='r')
            axis[i//4, i%4].plot(fit_dict,c='y')
            # axis.plt(1.9,2.45)
            #axis[i//4, i%4].plot(self.)
            axis[i//4, i%4].set_title('Sensor: '+str(i+1))
            axis[i//4, i%4].grid()
        f1=open('param{}.txt'.format(12),'w')
        f1.writelines(str(param_mat))
        f1.close()    
        # print(param_mat)
        figure.tight_layout(pad=0.1)
        plt.show()

if __name__=='__main__':
    c = cleanTactileData()
    c.isPlot = 1
    c.clean()




'''
##########
Deprecated Values
##########

21 May 2021
NOTE : VALUES TAKEN WITH 16 CLUSTERED
Untouched:
Expected outcome for port 4:
Minimum value 2.3638183593749997
Maximum value 2.44886962890625
Mean Value 2.436410742295696
Standard Deviation 0.018984020214603742

Expected outcome for port 3:
Minimum value 2.4403564453124997
Maximum value 2.450830078125
Mean Value 2.4442794346628487
Standard Deviation 0.0023577556727929303

Expected outcome for port 2:
Minimum value 2.3420318603515624
Maximum value 2.4410251464843746
Mean Value 2.426483423039951
Standard Deviation 0.022608812294732383

Expected outcome for port 1:
Minimum value 2.3444260253906246
Maximum value 2.441637451171875
Mean Value 2.426094382075945
Standard Deviation 0.02165582221318424

Expected outcome for port 0:
Minimum value 2.35577783203125
Maximum value 2.447357666015625
Mean Value 2.434048443312799
Standard Deviation 0.02089434145474797

Touched:
Expected outcome for port 0:
Minimum value 2.0909999999999997
Maximum value 2.4500244140625
Mean Value 2.4210151724273525
Standard Deviation 0.05328579688182751
'''