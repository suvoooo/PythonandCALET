#!/usr/bin/python
import math
import os,sys,numpy
import random 
try:
   import cPickle as pickle
except:
   import pickle

import matplotlib.pyplot as plt

errbarfilepath = '/home/suvo/Downloads/Analysis/errorbarfiles/generatesamples/DM/' 
eventpath = '/home/suvo/Downloads/Analysis/errorbarfiles/eventfile/'
DMfluxpath = '/home/suvo/Downloads/Analysis/CALETfit/DMspectra/'


binwidthnumber = 0.001
rangenumber = 3900
Elowbound = 9.8 # GeV
En = []
for i in range(rangenumber):
	energy = 10**(i*binwidthnumber)
	En.append(energy)

#+++++++++++++++++++++++++++++++
#+ parameters for errorbar
#+++++++++++++++++++++++++++++++
fiveyear = 5*365*24*3600 #yrtosec
eff = 0.80 
apperture = 0.1040 # m^2/sr


#+++++++++++++++++++++++++++++++++++++++++++++
#Best fit DM values 
#++++++++++++++++++++++++++++++++++++++
#{'ratse': 0.19123592377310364, 'phi': 0.5, 'Eg': 100.0, 'de': 0.5105560935874954, 'E_d': 10000.0, 's': 0.5, 'ce': 0.9516709887340581, 'ge': 2.959433796261762, 'decayel': 0.04965941992807199, 'decaymu': 0.08509499189102154, 'delta': 0.4, 'decaytau': 0.00010000000000287557}
#++++++++++++++++++++++++++++++++++++++


#++++++++++++++++++++++++++++++++++++++++++++
#+  checking radom number 
#++++++++++++++++++++++++++++++++++++++++++_++

#print random.gauss(25,50/3)
#mu, sigma = 3, 1 # mean and standard deviation
#s = numpy.random.normal(mu, sigma, 10000)

#print s 



#count, bins, ignored = plt.hist(s, 60, normed=True)
#plt.plot(bins, 1/(sigma * numpy.sqrt(2 * numpy.pi)) * numpy.exp( - (bins - mu)**2 / (2 * sigma**2) ),linewidth=2, color='r')
#plt.show()






def readeventfile():
	eventfile = open(eventpath+'bplawwithcutoffandDM800GeVnoTausm0d5phi0d5CALevent.d','r')	
	eventvals = {}
	while True:
		stringline = eventfile.readline()
		if stringline =='':
			break 
		stringlist= stringline.split()
		E=float(stringlist.pop(0))
		event=float(stringlist.pop(0))
		eventvals[E] = [event]
	return eventvals

eventvals = readeventfile()
es = sorted(eventvals.keys())

print len(es)

#seedinput = input("random seed :")
#seedinput = []


seedlist =[]
for k in range(1901,1971):
	seedlist.append(k)


lenfi = len(seedlist)

events =[]
#print seedinput
for se in range(lenfi):
	eventfileforDM = open(eventpath+'eventsfor0d8TeVDM/bplawwithcutoffandDM800GeVsm0d5phi0d5CALenergies%dcase.d'%(seedlist[se]),'w')
	#def main():
	random.seed(seedlist[se])
	numpy.random.seed(seedlist[se])
	for sig in range(len(es)):
		ei_min=10**((sig-0.5)*0.001)
		ei_max=10**((sig+0.5)*0.001)
		#print ei_min, ei_max
		if sig > 0 and sig < (len(es) -1) :
			nb = eventvals[es[sig]][0]	
			signals = nb
			if ei_min < Elowbound :
				continue
			#else :
			#	continue
			if signals > 100 :
				nevent = int(round(random.gauss(signals,math.sqrt(signals))))
			else:
				nevent=numpy.random.poisson(signals)
				#print nevent
			for j in range(nevent): 
				chev = random.uniform(ei_min,ei_max)
				events.append(random.uniform(ei_min,ei_max))
				eventfileforDM.write('{0:2}' .format(chev) + "\n")

#for ev in range(len(events)):
#	eventfileforDM.write('{0:2}' .format(events[ev]) + "\n")


eventfileforDM.close()





#def saveresults(rfn,results):
#	sfile=open(rfn,'w')   
#	pickle.dump(results, sfile, protocol=-1)
#	sfile.close



#if __name__ == '__main__':
#	sys.exit(main())	
	



