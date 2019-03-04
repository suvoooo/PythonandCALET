#!/usr/bin/python 

import os 
import numpy 
import sys, time, glob
#import numpy as np 
import  minuit
import time

sm = raw_input("smoothness without decimal (0.3 as 0d3) :") 
time.sleep(2)
phi = raw_input("sol mod potential without decimal: ")

# written according to brokenpowlawandpulsar.py but with solar modulation  
datapath = '/home/suvo/Downloads/experimentdata' 
savefigpath = '/home/suvo/Downloads/Analysis/CALETfit/plot/checktwop/tryexpect/bplawandpulsar/aftersubmission_pulsarcontrib/Ed10TeV/phi%s/smoo%sphi%s/'%(phi,sm,phi)
savefilename = savefigpath+"infosmoo%sphi%s.d"%(sm,phi)
fluxatsixteen=5.073244e-02 # GeV^{-1} m^{-2}

dirs=os.listdir(savefigpath)
print dirs
#for filename in dirs :
#	newfitfiles = open

d_file = open(savefilename,'w')
selectfiles1 =  glob.glob(savefigpath+"brpowlaw*")
print selectfiles1

selectfiles = glob.glob(savefigpath+"brpowlaw*")
print selectfiles 
for sel in selectfiles :
	newfiles = open(sel, 'r')
	#headerline = newfiles.readline()
	newvals = {}
	while True :
		stringline = newfiles.readline()
		infoline=newfiles.readline()
		if stringline=='':
			break
		stringlist=stringline.split()
		E = float(stringlist.pop(0))
		chi   = float(stringlist.pop(0))
		eg = float(stringlist.pop(0))
		newvals[E] = [chi,eg]
		for point in sorted(newvals.keys()):
			d_file.write('{0:2} {1:3} {2:4}' .format(point, newvals[point][0], newvals[point][1]) + "\n")



#files()
#if __name__=='__main__' : 
#	sys.exit(main())

