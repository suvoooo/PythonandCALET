#!/usr/bin/python 
import math 
import numpy
import time


pulcut=[100,110,120,130,140,150,160,170,180,190,200,220,240,270,290,300,350,400,450,500,550,600,650,700,800,900,1000,2000,3000,4000,5000,6000,7000,9000,10000]


sm = raw_input("smoothness without decimal (0.3 as 0d3) :") 

#time.sleep(1)
phi = raw_input("sol mod potential without decimal: ")
#senergy = input("write the cut-off energy: ")


savefigpath = '/home/suvo/Downloads/Analysis/CALETfit/plot/checktwop/tryexpect/bplawandpulsar/fixEpulcut/checksolmod/checksmoo/fixbreakenergy/finebreaken/finalfits/sm%sphi%s/'%(sm,phi)



savedvals = {}


for cut in range(len(pulcut)):
	senergy = pulcut[cut]
	openfilename = savefigpath+"infosmoo%sphi%s.d"%(sm,phi)
	rfile = open(openfilename,'r')
	writefilename = savefigpath+"formaxminEpul%dwithrigsmoo%sphi%s.d"%(senergy,sm,phi)	
	wfile = open(writefilename,'w')
	while True:
		stringline = rfile.readline()
		#print stringline
		if stringline =='':
			break
		stringlist=stringline.split()
		#print stringlist
		E = float(stringlist.pop(0))
		eg = float(stringlist.pop(0))
		chi = float(stringlist.pop(0))
		savedvals[E] = [eg,chi]
		#print E
		if E==senergy :
			wfile.write('{0:2} {1:3} {2:4}' .format(senergy, savedvals[E][0], savedvals[E][1]) + "\n")
		#print savedvals[E]
	#return savedvals
	wfile.close()
