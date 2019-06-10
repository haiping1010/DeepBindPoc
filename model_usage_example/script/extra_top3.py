import os
import os
import shutil
import numpy as np

import pandas as pd

if (len(os.sys.argv)<2):

    print "usage: python compare.py file1 file2"


nf=open(os.sys.argv[1], 'r')
old=[]
oldvalue=[]
oldline=[]
dictory={}
print os.sys.argv[1]
newlines=nf.readlines()
for name in newlines:
    dictory[name.strip()] =pd.DataFrame() 


f=open(os.sys.argv[2], 'r')
lines=f.readlines()
i=0
for name in lines:
  i=i+1
  if i>1:
    arrs=name.split(' ')
    df=pd.DataFrame()
    df=pd.DataFrame({'value1':[arrs[0]], 'value2':[arrs[1]], 'value3':[arrs[2].strip()]})
    df.value2=df.value2.astype(float)
    df.value3=df.value3.astype(float)
    dictory[name[0:4].strip()]=dictory[name[0:4].strip()].append(df)
    
for k,v in  dictory.items():
     
     v=v.sort_values(by=['value2'],ascending=False)
     v.index=range(len(v.values))
     #print v
     v.value2=v.value2.astype(str)
     v.value3=v.value3.astype(str)
     #print v
     print '  '.join(v.iloc[0].values)
     print '  '.join(v.iloc[1].values)
     print '  '.join(v.iloc[2].values)        




