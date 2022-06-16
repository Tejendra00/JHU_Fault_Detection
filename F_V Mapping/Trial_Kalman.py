import numpy as np
from numpy.linalg import inv
from numpy import tile,dot
import matplotlib.pyplot as plt
import time
from math import pi
from numpy import *

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

    # def _stackPlot(self,):
    #     figure, axis = plt.subplots(4, 4)

    #     for i in range(16):
    #         axis[i//4, i%4].plot(self.data_dict[str(i+1)])
    #         # axis[i//4, i%4].plot(self.)
    #         axis[i//4, i%4].set_title('Sensor: '+str(i+1))
    #         axis[i//4, i%4].grid()
    #     figure.tight_layout(pad=0.1)
    #     plt.show()

class KalmanFilter(object):
    def __init__(self, F = None, B = None, H = None, Q = None, R = None, P = None, x0 = None):

        if(F is None or H is None):
            raise ValueError("Set proper system dynamics.")

        self.n = F.shape[1]
        self.m = H.shape[1]

        self.F = F
        self.H = H
        self.B = 0 if B is None else B
        self.Q = np.eye(self.n) if Q is None else Q
        self.R = np.eye(self.n) if R is None else R
        self.P = np.eye(self.n) if P is None else P
        self.x = np.zeros((self.n, 1)) if x0 is None else x0

    def predict(self, u = 0):
        self.x = np.dot(self.F, self.x) + np.dot(self.B, u)
        self.P = np.dot(np.dot(self.F, self.P), self.F.T) + self.Q
        return self.x,self.P

    def gauss_pdf(self,x,M,S):
        if M.shape()[1] == 1:
            DX = x - tile(M, x.shape()[1])
            E = 0.5 * sum(DX * (dot(inv(S), DX)), axis=0)
            E = E + 0.5 * M.shape()[0] * np.log(2 * np.pi) + 0.5 * np.log(np.linalg.det(S))
            P= np.exp(-E)
        elif x.shape()[1] == 1:
            DX = tile(x, M.shape()[1])- M
            E = 0.5 * sum(DX * (dot(inv(S), DX)), axis=0)
            E = E + 0.5 * M.shape()[0] * np.log(2 * np.pi) + 0.5 * np.log(np.linalg.det(S))
            P = np.exp(-E)
        else:
            DX = x-M
            E = 0.5 * dot(DX.T, dot(inv(S), DX))
            E = E + 0.5 * M.shape()[0] * np.log(2 * np.pi) + 0.5 * np.log(np.linalg.det(S))
            P = np.exp(-E)
        return (P[0],E[0])

    def update(self,):
        self.IM=np.dot(self.H,self.x)
        self.IS = self.R + np.dot(self.H, np.dot(self.P, self.H.T))
        self.K = np.dot(self.P, np.dot(self.H.T, inv(self.IS)))
        self.x = self.x + np.dot(self.K, (self.y-self.IM))
        self.P = self.P - np.dot(self.K, np.dot(self.IS, self.K.T))
        self.LH = self.gauss_pdf(self.y, self.IM, self.IS)
        return (self.x,self.P,self.K,self.IM,self.IS,self.LH)
    
    

    # def update(self, z):
    #     y = z - np.dot(self.H, self.x)
    #     S = self.R + np.dot(self.H, np.dot(self.P, self.H.T))
    #     K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))
    #     self.x = self.x + np.dot(K, y)
    #     I = np.eye(self.n)
    #     self.P = np.dot(np.dot(I - np.dot(K, self.H), self.P), 
    #     	(I - np.dot(K, self.H)).T) + np.dot(np.dot(K, self.R), K.T)
    #     # return self.x

def example(data):
    dt=1/20
    F= np.array([[1, dt, 0], [0, 1, -dt], [0, 0, 1]])
    H = np.array([1, 0, 0]).reshape(1, 3)
    Q = np.array([[0.01, 0.01, 0.0], [0.01, 0.01, 0.0], [0.0, 0.0, 0.0]])
    R = np.array([5]).reshape(1, 1)
        # x = np.linspace(-10, 10, 100)
        # measurements = - (x**2 + 2*x - 2)  + np.random.normal(0, 2, 100)
    a=data
    kf = KalmanFilter(F = F, H = H, Q = Q, R = R)
    predictions = []

    for z in range(len(data)):
        predictions.append(np.dot(H,  kf.predict())[0])
        kf.update(data[z])

    import matplotlib.pyplot as plt
    plt.plot(range(len(a)), a, label = 'Measurements')
    plt.plot(range(len(predictions)), np.array(predictions), label = 'Kalman Filter Prediction')
    plt.xlim(-100,3250)
    plt.ylim(2.3458,2.353)
    plt.legend()
    plt.show()

if __name__ == '__main__':
    c=cleanTactileData()
    g=c.clean()
    print(len(g))
    #     print(g[i])
    example(g)