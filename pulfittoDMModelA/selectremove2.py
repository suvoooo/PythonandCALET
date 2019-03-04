#!/usr/bin/python 

import os 
import numpy 
import sys, time, glob
#import numpy as np 
import  minuit
import time



def last_8chars(x):
    return float(x[-8:-2])



fn = input("folder num:")

savefigpath = '/home/suvo/Downloads/Analysis/pulfitto1d1TDMEd10T_aftrersubmission_pulsarcontrib/newfiles%d/'%(fn)

lowcasenum = input("lcase num: ")
highcasenum = input("hcase num: ")

caselist=[]

for lo in range(lowcasenum,highcasenum):
	caselist.append(lo)


print caselist


#selectfiles =sorted( glob.glob(savefigpath+"brpowlawcase%dch*"%(71)))

#print selectfiles

#casenum = int(float(sys.argv[1]))

#maxheaderline=float(170)
for cs in range(len(caselist)):
	fcase = caselist[cs]
	print fcase
	selectfiles = sorted(glob.glob(savefigpath+"brpowlawcase%dch*"%(fcase)))
	#nfiles = sorted(selectfiles,key=last_8chars)
	print selectfiles[-1:]
	del selectfiles[:3]


	for sel in selectfiles :
		#while selectfiles > 3 :
		os.remove(sel)
#
				

'''

x = [2,3,4,5,6,7,8,9]

print x[-4:-1]

'''
