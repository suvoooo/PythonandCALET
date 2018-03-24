#!/usr/bin/python 

import math 
import numpy as np 
import matplotlib.pyplot as plt

effarea = 0.1040 # m^2
efficiency = 0.8
fiveyear = 5*365*24*3600

eventpath = '/home/suvo/Downloads/Analysis/errorbarfiles/eventfile'


Eminmax = [1,4]
nbins = 60
yax = []


def binsize(a,b):
	return (10**b) - (10**a)




#csn = input("case_number: ")


#def readeventfile():
#	eventfile = open('./checkeventfiles/bplawwithcutoffandDM1100GeVsm0d5phi0d5CALenergies%dcasenoTau.d'%(csn),'r')
#	Event = []
#	while True :
#		stringline = eventfile.readline()
#		if stringline =='':
#			break 
#		stringlist = stringline.split()
#		E = float(stringlist.pop(0))
#		Event.append(E)
#	#print Event[14149650]
#	return Event 

#Event1 = readeventfile() 	

seedlist =[]
for t in range(1901,2501):
	seedlist.append(t)

filen = len(seedlist)

#def readeventfile():
for se in range(filen):
	eventfile = open(eventpath+'/eventsfor0d8TeVDM/bplawwithcutoffandDM800GeVsm0d5phi0d5CALenergies%dcase.d'%(seedlist[se]),'r')
	Event = []
	while True :
		stringline = eventfile.readline()
		if stringline =='':
			break 
		stringlist = stringline.split()
		E = float(stringlist.pop(0))
		Event.append(E)
	for a in Event :
		yax.append(math.log10(a))
	k, bins, patches=plt.hist(yax,histtype='step',bins=nbins, range=Eminmax)
	del yax[:]
	d_file = open(eventpath+'/CALET5yrsdata0d8TeVwithoutTau/CALET5yeardatacase%dwithTauDM0d8TnoTau.d'%(seedlist[se]),'w')
	for i in range(len(bins)-1):
		bincenter=10**(0.5*(bins[i]+bins[i+1]))
		if k[i] > 5 :
			flux=k[i]/binsize(bins[i],bins[i+1])/effarea/efficiency/fiveyear
			staterr=math.sqrt(k[i])/binsize(bins[i],bins[i+1])/effarea/efficiency/fiveyear
			#k[:]
			#bins[:]
			#print k
			d_file.write('{0:2} {1:3} {2:4}' .format(bincenter, flux, staterr) + "\n")
			
		
d_file.close()





#print Event1[450006] # just for check 





#print yax



#print len(bins)

#print bins
#print len(k)


#print k



#d_file = open('./CALET5yearDM1d1noTau/CALET5yeardatacase%dnoTauDM1d1.d'%(csn),'w')

#for i in range(len(bins)-1):
#	bincenter=10**(0.5*(bins[i]+bins[i+1]))
#	if k[i] > 5 :
#		flux=k[i]/binsize(bins[i],bins[i+1])/effarea/efficiency/fiveyear
#		staterr=math.sqrt(k[i])/binsize(bins[i],bins[i+1])/effarea/efficiency/fiveyear
#		d_file.write('{0:2} {1:3} {2:4}' .format(bincenter, flux, staterr) + "\n")

#d_file.close()






