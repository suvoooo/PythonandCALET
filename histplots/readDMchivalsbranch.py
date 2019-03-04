#!/usr/bin/python 

import os 
import numpy 
import sys, time, glob
#import numpy as np 
import  minuit
import time



datapath = '/home/suvo/Downloads/experimentdata' 
savefigpath = '/home/suvo/Downloads/Analysis/DMfitDM/fitto1d1TDMwithTauEd10Ts1d0p0d5correct2/newfiles/'
savefilename = savefigpath+"info1d1TDMs1d0Ed10Tfitallvalsalldecay.d"
fluxatsixteen=5.073244e-02 # GeV^{-1} m^{-2}



dirs=os.listdir(savefigpath)
#print dirs
#for filename in dirs :
#	newfitfiles = open

d_file = open(savefilename,'w')
selectfiles1 =  glob.glob(savefigpath+"brpowlaw*")
#print selectfiles1

selectfiles = glob.glob(savefigpath+"brpowlaw*")
#print selectfiles 

chilist = []

for sel in selectfiles :
	newfiles = open(sel, 'r')
	headerline = newfiles.readline()
	#print headerline	
	newvals = {}
	#while True :
	stringline = newfiles.read()
	print stringline
	if stringline=='Eg':
		break
	stringlist=stringline.split()
	ratsename=str(stringlist.pop(0))
	ratseval = stringlist.pop(0)
	phival=str(stringlist.pop(0))
	phi = stringlist.pop(0)
	Eg=str(stringlist.pop(0))
	Egval = stringlist.pop(0)
	de=str(stringlist.pop(0))
	deval=stringlist.pop(0)
	Ed = str(stringlist.pop(0))
	Edval = stringlist.pop(0)
	s=str(stringlist.pop(0))
	sval=stringlist.pop(0)
	ce = str(stringlist.pop(0))
	ceval = stringlist.pop(0)
	ge = str(stringlist.pop(0))
	geval = stringlist.pop(0)
	decayel=str(stringlist.pop(0))
	decayelval = stringlist.pop(0)
	decaymu=str(stringlist.pop(0))
	decaymuval = stringlist.pop(0)
	delta = str(stringlist.pop(0))
	deltaval = stringlist.pop(0)
	decaytau = str(stringlist.pop(0))
	decaytauval = stringlist.pop(0)
	newvals[ratseval] = [decayelval,decaymuval,decaytauval]
	for point in newvals.keys():
			d_file.write('{0:2} {1:3} {2:4}' .format(newvals[point][0], newvals[point][1], newvals[point][2]) + "\n")
	



print len(chilist)

#print ratseval
for i in range(len(chilist)):
	d_file.write('{0:2}' .format(chilist[i]) + "\n")

d_file.close()

#for point in sorted(newvals.keys()):
#	d_file.write('{0:2}' .format(point, newvals[point][0], newvals[point][1]) + "\n")



#files()
#if __name__=='__main__' : 
#	sys.exit(main())

