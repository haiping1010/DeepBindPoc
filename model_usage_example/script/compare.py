import os
import os
import shutil
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
    arrall=name.split(':')
    dictory[arrall[0].replace(".pdb","")] = arrall[1]


f=open(os.sys.argv[2], 'r')
lines=f.readlines()
i=0
for name in lines:
  i=i+1
  if i>1:
    arrs=name.split(',')
    temname=arrs[0].replace('_neg','')
    temname=temname.replace('_pos','')
    temname=temname.replace('_ACP','')
    temname=temname.replace('_GTP','')
    print arrs[0], arrs[1].strip(), dictory[temname].strip()

        


