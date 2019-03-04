#!/usr/bin/python

#!/usr/bin/python 
import math 
import numpy
#import time
import sys, time, glob
import operator

sm = raw_input("smoothness without decimal (0.3 as 0d3) :") 

#time.sleep(1)
phi = raw_input("sol mod potential without decimal: ")


savefigpath = '/home/suvo/Downloads/Analysis/CALETfit/plot/checktwop/tryexpect/bplawandpulsar/fixEpulcut/checksolmod/checksmoo/fixbreakenergy/finebreaken/finalfits/sm%sphi%s/'%(sm,phi)

savefilename = savefigpath+"minchism%sphi%s.d"%(sm,phi)

d_file = open(savefilename,'w')
selectfiles =  glob.glob(savefigpath+"formaxminEpul*")
print selectfiles



for sel in selectfiles :
	newfiles = open(sel, 'r')
	#headerline = newfiles.readline()
	savedvals = {}
	while True :
		stringline = newfiles.readline()
		if stringline =='':
			break
		stringlist=stringline.split()
		#print stringlist
		E = float(stringlist.pop(0))
		eg = float(stringlist.pop(0))
		chi = float(stringlist.pop(0))
		savedvals[eg] = [chi]
	d_file.write('{0:2} {1:3} {2:4}' .format(E, min(savedvals.iteritems(), key=operator.itemgetter(1))[0], min(savedvals.iteritems(), key=operator.itemgetter(1))[1] ) + "\n")  


d_file.close()


