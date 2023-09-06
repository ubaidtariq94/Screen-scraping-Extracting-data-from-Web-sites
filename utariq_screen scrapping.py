#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import re
import numpy as np
from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


ur = requests.get("https://top500.org/statistics/sublist/", verify=True)


# In[3]:


bsoup = BeautifulSoup(ur.content, 'html.parser')


# In[4]:


filename = "C:/Users/ubaid.LAPTOP-60AEGHFJ/Desktop/TOP500.csv"
f = open(filename, "w",encoding="utf-8")


# In[5]:


header = []
for record in bsoup.findAll('th'):
    header.append(record.text)
f.write("|".join(header) + '\n')
    
for record in bsoup.findAll('tr')[1:]:
    tbltxt = ""
    for data in record.findAll('td'):
        tbltxt = tbltxt + data.text + "|"
        
    tbltxt = re.sub("\s+", " ", tbltxt)
    tbltxt = tbltxt[0:-1] + '\n'  
    print(tbltxt)
    f.write(tbltxt)
f.close()


# In[6]:


df = pd.read_csv("C:/Users/ubaid.LAPTOP-60AEGHFJ/Desktop/TOP500.csv", delimiter="|")
df.head()


# In[7]:


df['Power (kW)'] = df['Power (kW)'].apply(lambda x: round(float(str(x).replace(",","")),2))
df['Cores'] = df['Cores'].apply(lambda x: int(x.replace(",","")))
df['Rpeak (TFlop/s)'] = df['Rpeak (TFlop/s)'].apply(lambda x: float(x.replace(",","")))


# In[8]:


df['Rmax (TFlop/s)'] = df['Rmax (TFlop/s)'].apply(lambda x: float(x.replace(",","")))


# In[9]:


df.head()


# In[10]:


df.describe()


# In[11]:


plt.figure(figsize=(12,6))
x = df['Cores']
y = df['Rpeak (TFlop/s)']
plt.xscale('log')
plt.yscale('log')
plt.scatter(x,y,color='Red')
plt.title("Relationship Between Cores and Rpeak")
plt.xlabel("Cores")
plt.ylabel("Rpeak (TFlop/s)")
plt.show()


# In[15]:


plt.figure(figsize=(12,6))
x = df['Cores']
y = df['Power (kW)']
plt.xscale('log')
plt.yscale('log')
plt.scatter(x,y,color='Green')
plt.title("Relationship Between Cores and Power")
plt.xlabel("Cores")
plt.ylabel("Power (kW)")
plt.show()


# In[21]:


plt.figure (figsize=[10,5])
plt.title("Graphical Interpretaion of Cores")
plt.yscale('log')
plt.boxplot(df['Cores'])
print("")


# In[22]:


plt.figure (figsize=[10,5])
plt.title("Graphical Interpretaion of Rpeak")
plt.yscale('log')
plt.boxplot(df['Rpeak (TFlop/s)'])


# In[23]:


plt.figure (figsize=[10,5])
plt.title("Graphical Interpretaion of Power")
plt.yscale('log')
plt.boxplot(df['Power (kW)'].dropna().astype(int))

