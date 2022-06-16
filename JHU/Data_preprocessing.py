from typing_extensions import final
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
'''
For values xtravel, ytravel, zelevate etc..
Please refer config.py file in Gcode folder.
'''

parent_path="./Datasets/raw_vel6000"
dir_list=os.listdir(parent_path)
Total_time=100 # sec
for file_name in dir_list:
    class_path=os.path.join(parent_path,file_name)
    if os.path.isdir(class_path):
        
        files=os.listdir(class_path)
        c=0
        
        for f in files: 
        

            file_path=os.path.join(class_path,f)
            a=open(str(file_path),'r')   
            lines=a.readlines()
            ############################

            #### File Cleaning Code ####

            ############################
            i=0
            final_file=open(os.path.join(class_path,"Clean_"+f),'w')
            for line in lines:
            
                if len(line.split())!=16:
                    temp=lines[i-1]
                    final_file.write(temp)
                    lines[i]=temp
                    c+=1
                else:
                    final_file.write(line)  
                i+=1
            final_file.close()
            cleanedfile_path=os.path.join(class_path,"Clean_"+f)

            ############################

            #### File to csv Code ####

            ############################
            df1=pd.read_csv(str(cleanedfile_path),sep='\s+',header=None)
            df1.to_csv(os.path.join(class_path,'Clean_'+os.path.splitext(f)[0]+'.csv'), index = None)

            ############################

            #### Time of Clean file code ####

            ############################
            
            cleanedfile=open(cleanedfile_path,'r')
            number_lines = [line.strip("\n") for line in cleanedfile if line != "\n"]
            cleanedfile.close()
            Time_int=Total_time/len(number_lines)
            new_file_name='time_Clean_'+f
            new_file=open(os.path.join(class_path,new_file_name),'w')
            tim=0
            while(tim<Total_time):
                new_file.write(str(tim)+'\n')

                tim+=Time_int
            new_file.close()
            ############################

            #### Merging Clean file with Time Code ####

            ############################

            mergefile_path=os.path.join(class_path,"time_Clean_"+f)
            df2=pd.read_csv(mergefile_path)
            df3=pd.read_csv(os.path.join(class_path,'Clean_'+os.path.splitext(f)[0]+'.csv'))
        
            df2=df2.rename(columns={'0':'Time'})
            df_final=df3.join(df2)
        
            df_final.to_csv(os.path.join(class_path, os.path.splitext(f)[0]+'.csv'),index=None)

            os.remove(os.path.join(class_path,'Clean_'+os.path.splitext(f)[0]+'.csv'))
            os.remove(os.path.join(class_path,new_file_name))
            # os.remove(cleanedfile_path)
            print('Number of discrepancies in the file : '+str(file_name) +'/' +str(f), c) # Number of discrepancies in raw file

    # except:
    #     pass
   
        
