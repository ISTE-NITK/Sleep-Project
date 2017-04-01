
# coding: utf-8

# In[1]:

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.dates import date2num
import datetime
import matplotlib.dates as mdates
import time
import numpy as np
from datetime import date
import matplotlib.lines as mlines
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as mpatches
import category_encoders as ce
import glob
from sklearn.cluster import KMeans


# In[2]:

#Getting all the data
def get_all_data(file_path):
    
    data = pd.DataFrame()
    quality = pd.DataFrame()
    
    avg_illuminance = pd.DataFrame()
    avg_airquaility = pd.DataFrame()
    avg_temp = pd.DataFrame()
    avg_humididty = pd.DataFrame()
    avg_quality = pd.DataFrame()
    
    sleep_quality_data = get_data('/home/prajwal/Desktop/istesleep/data/sleepdata.csv',delim=';')
    
    for filename in glob.glob(file_path): 
        
        df = pd.read_csv(filename)
    
        avg_illuminance = avg_illuminance.append([np.mean(df[' illuminance'])])
        avg_airquaility = avg_airquaility.append([np.mean(df['airquality'])])
        avg_temp = avg_temp.append([np.mean(df[' temperature'])])
        avg_humididty = avg_humididty.append([np.mean(df[' humidity'])])
        
        date = df[' timestamp'].astype(str).str[:-22][0]
        date = date[1:11]
        
        sleep_quality = get_sleep_quality(sleep_quality_data,date)
        avg_quality = avg_quality.append(sleep_quality)
        sleep_quality = sleep_quality*df.shape[0]
        
        quality_date = pd.DataFrame(sleep_quality)
        quality = pd.concat([quality,quality_date],axis = 0,ignore_index=True)
        
        data = pd.concat([data,df],axis = 0,ignore_index=True)
    
    avg_data = pd.concat([avg_illuminance,avg_airquaility,avg_temp,avg_humididty,avg_quality],axis = 1,                        ignore_index=True)
    data = pd.concat([data,quality],axis = 1)
    
    return [data, avg_data]


# In[53]:

def split_data(data):
    
    data_light = data[data['illuminance']>50]
    data_dark = data[data['illuminance']<50]
    #data_dark = data_dark[data_dark['illuminance']>5]
    
    return [data_light, data_dark]


# In[ ]:

def get_sleep_quality(data,date):
    
    x = data['Sleep quality'][data['End'].astype(str)==date].tolist()
    
    return x


# In[ ]:

def get_data(filepath,delim=','):
    
    data = pd.read_csv(filepath,sep=delim)
    
    return data


# In[ ]:

def data_sample(data):

    data = data.iloc[::5, :]
    
    return data


# In[ ]:

def data_to_csv(data,file_name):
    
    data.to_csv(file_name, sep=',')


# In[ ]:

def convert_date(data):
    
    data[' timestamp'] = data[' timestamp'].astype(str).str[:-13]
    data[' timestamp'] = pd.to_datetime(data[' timestamp'])
    data['airquality'] = data['airquality'].astype(float)
    
    return data


# In[ ]:

def plot_two(data, x,y):
    
    plt.scatter(data[x], data[y])
    plt.axis('tight')
    plt.ylabel(y)
    plt.xlabel(x)
    plt.show()


# In[ ]:

def plot_simple(data,x,y,c='r',s = 40):
    
    plt.scatter(data[x], data[y], c = c,s=s, alpha=0.5)
    plt.axis('tight')
    plt.ylabel(y)
    plt.xlabel(x)
    plt.show()


# In[ ]:

def plot(data,x,y,c='quality',s = 40):
    
    plt.scatter(data[x], data[y], c = data[c], s=s, alpha=0.5,cmap='viridis')
    plt.axis('tight')
    plt.colorbar()
    plt.ylabel(y)
    plt.xlabel(x)
    plt.show()


# In[54]:

#data, avg_data = get_all_data('/home/prajwal/Desktop/istesleep/data/Data/*.csv')
data = pd.read_csv('/home/prajwal/Desktop/Data/Data.csv')
avg_data = pd.read_csv('/home/prajwal/Desktop/Data/Avg_Data.csv')


# In[55]:

#Splitting data into two components, day and night data.
data_light,data_dark = split_data(data)


# In[56]:

#Plot - pass parameters, data and the column names you want to plot. Color indicates sleep quality
plot(data_dark,'illuminance','airquality')


# In[15]:

#plot(avg_data,'avg_illuminance','avg_airquaility')


# In[16]:

#plot(avg_data,'avg_illuminance','avg_airquaility')


# In[17]:

#Plot - pass parameters, data and the column names you want to plot. 
#plot_two(data,'steps','quality')


# In[18]:

#x = np.mean(data['steps'][data['quality']==70])


# In[19]:

#y = np.mean(data['steps'][data['quality']==68])


# In[20]:

#z = np.mean(data['steps'][data['quality']==75])


# In[21]:

#v = np.mean(data['steps'][data['quality']==77])


# In[22]:

#t = x*70 + y*68 + z*75 + v*77


# In[23]:

#t/(70+71+75+77)

