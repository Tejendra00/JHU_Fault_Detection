#!/usr/bin/env python
# coding: utf-8

# In[14]:


import matplotlib.pyplot as plt
import time
import numpy as np

class filterData():
    def __init__(self):
        self.filename="2.txt"
        self.timme="2.csv"
        self.numSensors = 16
        self.data_dict = { '1':[],  '2':[],  '3':[], '4':[], 
                    '5':[],  '6':[],  '7':[],  '8':[], 
                    '9':[],  '10':[], '11':[], '12':[],
                    '13':[], '14':[], '15':[], '16':[] }

        self.stats_dict = { '1':[],  '2':[],  '3':[], '4':[], 
                    '5':[],  '6':[],  '7':[],  '8':[], 
                    '9':[],  '10':[], '11':[], '12':[],
                    '13':[], '14':[], '15':[], '16':[] }
        
        self.simple_movingAverages = dict()
        self.cumulative_movingAverages = dict()

        self.isFilter = 0 #Mark True if want to filter
        
#         self.isPlot = 0
#         self.isFindD = 0
    
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
        
        if self.isFilter:
            self.SMA()
            self.CMA()
            self.plot_together()
            
#         if self.isPlot:
#             self._stackPlot_grid()
#             self._stackPlot_single()
            
#         if self.isFindD: #if you want to find the dominant
#             self.find_dominant()

        return self.data_dict, self.stats_dict

    
    def SMA(self,): #Simple Moving Average
        import numpy as np
        
        window_size = 15

        for j in range(self.numSensors):
            i = 0
            # Initialize an empty list to store moving averages
            self.simple_movingAverages[str(j+1)] = list()

            # Loop through the array to
            #consider every window of size 15
            while i < len(self.data_dict[str(j+1)]) - window_size + 1:

                # Calculate the average of current window
                window_average = np.sum(self.data_dict[str(j+1)][
                  i:i+window_size]) / window_size

                # Store the average of current
                # window in moving average list
                self.simple_movingAverages[str(j+1)].append(window_average)

                # Shift window to right by one position
                i += 1

#             print(moving_averages)
        
        figure, axis = plt.subplots(4, 4)

        for i in range(16):
            axis[i//4, i%4].plot(self.simple_movingAverages[str(i+1)])
#             axis[i//4, i%4].plot(self.)
            axis[i//4, i%4].set_title('Sensor: '+str(i+1))
            axis[i//4, i%4].grid()
        figure.tight_layout(pad=0.1)
        plt.show()
        
        return self.simple_movingAverages
    
    def CMA(self,): #Cumulative Moving Average
        import numpy as np
        
        for j in range(self.numSensors):
            i = 1
            # Initialize an empty list to store cumulative moving
            # averages
            self.cumulative_movingAverages[str(j+1)] = list()
            
            # Store cumulative sums of array in cum_sum array
            cum_sum = np.cumsum(self.data_dict[str(j+1)]);

            # Loop through the array elements
            while i <= len(self.data_dict[str(j+1)]):

                # Calculate the cumulative average by dividing
                # cumulative sum by number of elements till 
                # that position
                window_average = cum_sum[i-1] / i

                # Store the cumulative average of
                # current window in moving average list
                self.cumulative_movingAverages[str(j+1)].append(window_average)

                # Shift window to right by one position
                i += 1
                
#             print(moving_averages)
        
        figure, axis = plt.subplots(4, 4)

        for i in range(16):
            axis[i//4, i%4].plot(self.cumulative_movingAverages[str(i+1)])
#             axis[i//4, i%4].plot(self.)
            axis[i//4, i%4].set_title('Sensor: '+str(i+1))
            axis[i//4, i%4].grid()
        figure.tight_layout(pad=0.1)
        plt.show()
        
        return self.cumulative_movingAverages

    def plot_together(self,):
    
        figure, axis = plt.subplots(4, 4)

        for i in range(16):
            axis[i//4, i%4].plot(self.simple_movingAverages[str(i+1)])
            axis[i//4, i%4].plot(self.cumulative_movingAverages[str(i+1)])

    #             axis[i//4, i%4].plot(self.)
            axis[i//4, i%4].set_title('Sensor: '+str(i+1))
            axis[i//4, i%4].grid()
        figure.tight_layout(pad=0.1)
        plt.show()        

#     def _stackPlot_grid(self,):
#         figure, axis = plt.subplots(4, 4)

#         for i in range(16):
#             axis[i//4, i%4].bar(range(len(self.data_dict[str(i+1)])),self.data_dict[str(i+1)], width = 0.1)
#             #axis[i//4, i%4].plot(self.)
#             axis[i//4, i%4].set_title('Sensor: '+str(i+1))
#             axis[i//4, i%4].grid()
#         figure.tight_layout(pad=0.1)
#         plt.show()

    
#     def _stackPlot_single(self,):
# #         figure, axis = plt.subplots(4, 4)
# #         plt.bar(range(len(self.data_dict['1'])),self.data_dict['1'], width = 0.1)

#         for i in range(16):
#             shift = 10 #To distinguish the bars 
#             plt.bar(add_(range(len(self.data_dict[str(i+1)])),shift*i),self.data_dict[str(i+1)], width = 0.1)
# #             axis[i//4, i%4].plot(self.)
        
#         plt.legend(["Sensor-1","Sensor-2","Sensor-3","Sensor-4","Sensor-5","Sensor-6","Sensor-7","Sensor-8","Sensor-9","Sensor-10","Sensor-11","Sensor-12","Sensor-13","Sensor-14","Sensor-15","Sensor-16"])
#         plt.title('16 sensors data for 1 sec')
#         plt.grid()
# #         figure.tight_layout(pad=0.1)
#         plt.show()
    
#     def find_dominant(self,):
#         stage_max = list()
#         n = len(self.data_dict['1'])
#         for i in range(n):
#             temp_list = list()
#             for j in range(16):
#                 temp_list.append(self.data_dict[str(j+1)][i])
            
#             temp_max_element = max(temp_list);
#             temp_max_key = str(temp_list.index(temp_max_element)+1)
#             stage_max.append(temp_max_key)
            
#         count_list = list()
#         for i in range(16):
#             count_list.append(stage_max.count(str(i+1)))
        
#         dominant_sensor_index = str(count_list.index(max(count_list))+1)
#         print("Dominant Sensor is: Sensor -",dominant_sensor_index)
        
#         return dominant_sensor_index

if __name__=='__main__':
    c = filterData()
#     c.isPlot = 0
#     c.isFindD = 1
    c.isFilter = 1
    c.clean()
    
    figure, axis = plt.subplots(4, 4)


# In[ ]:




