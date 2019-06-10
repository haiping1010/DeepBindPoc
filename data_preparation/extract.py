import sys
if len(sys.argv) <1 :
   print("python python2_L.py xxx")
filebase=sys.argv[1]
##filebase=file.replace(".pdb","")
import glob

pdball=glob.glob('pockets/pocket*_atm.pdb')

for name in  pdball:
   fr=open(name,'r')
   arr=[]
   poc_ID=name.replace('pockets/pocket','')
   poc_ID=poc_ID.replace('_atm.pdb','')
   for name in fr.readlines():
      if name[0:4]=='ATOM':
         id=name[17:26]
         #print id
         arr.append(id)
   frr=open('../'+filebase+'.pdb', 'r')
   fw=open(filebase+'_pocket_n'+poc_ID+'.pdb','w')
   for nameline in frr.readlines():
      for id in list(set(arr)):
          if nameline[17:26]==id and nameline[16:17]!='B' and  nameline[16:17]!='C' and nameline[16:17]!='D':
               fw.write(nameline)


