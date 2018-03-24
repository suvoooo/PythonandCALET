#!/usr/bin/python 

import  math 
#import matplolib.pyplot as plt 

#+++++++++++++++++++++++++++++++
#+ parameters for errorbar
#+++++++++++++++++++++++++++++++
fiveyear = 5*365*24*3600 #yrtosec
eff = 0.80 
apperture = 0.1040 # m^2/sr

#++++++++++++++++++++++++++++++++++++++++++++
#+	Energy bin calculation
#++++++++++++++++++++++++++++++++++++++++++++
binwidthnumber = 0.001
rangenumber    = 3900
En = []
for i in range(rangenumber):
	en = 10**(i*binwidthnumber)
	En.append(en)


# normalization flux at 16 GeV
fluxatsixteen=5.073244e-02 # GeV^{-1} m^{-2}
DMfluxpath = '/home/suvo/Downloads/Analysis/CALETfit/DMspectra/'
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+ Parametrization According to arXiv: 1612.06634 / 
#+ Different for electron and positron, best realized with 
#+ solar modulation potential. This version is with SM 
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Positron parametrization 
# Similar to AMS-02 Positron fraction parametrization in 2013,2015 papers 


def posiparam(ce,ge,ratse,delta,phi,Eposi):
	nE = Eposi + phi
	checkposiflux = (ce *fluxatsixteen* ((nE/16.)**(-ge)) ) * (ratse* (nE**(-delta)))
	#posiflux = diffpos * ((Eposi+phi)**(-gammaposi)) + ( scoeff * ((Eposi+phi)**(-gammas)) * math.exp(-(Eposi+phi)/sourcecut) )
	solfactposi = (Eposi **2 - (0.05**2))/( (Eposi+phi)**2 - (0.05 **2))
	return checkposiflux * solfactposi



#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+   Electron Parametrization 
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++            
# Electron parametrization includes a primary component which includes a power law break just as AMS-02 proton parametrization, 
# It also includes the source term just as in the positron flux term as mentioned in the paper due to lack of evidence for a deficit in electrons 
# the parametrization is later corrected for the smoothness term # (1+ (E/E_g)**(delta/s))**s


def elecparam(ce,ge,ratse,delta,Eg,de,s,phi,E_d,Eelec):
	newE = Eelec + phi 
	compliterm = (1. + (newE/Eg)**(de/s) )**s
	brokepow = ce * fluxatsixteen* ((newE/16.)**(-ge-de)) * (compliterm)
	diffflux = (ratse* (newE**(-delta))) + math.exp(-newE/E_d) 
	elecflux = brokepow * diffflux
	solfact = (Eelec **2 - 0.05**2)/( (Eelec+phi)**2 - 0.05 **2)
	#print Eelec, check1 
	return elecflux * solfact


MDM = input("Mass of Dark Matter: ")



#+++++++++++++++++++++++++++++++++++++++++++++++++++
#+ Read DM to 100 % muon flux  flux $\mu\mu\nu$
#+++++++++++++++++++++++++++++++++++++++++++++++++++
def readDMmuflux():
	DMmufluxfile = open(DMfluxpath+ '/muflux/GAL-D2d9-d0d40-4point-mu-M%dcheckdiff15z7kpc.d'%(MDM),'r')
	DMmuvals = {}
	while True :
		stringline = DMmufluxfile.readline()
		if stringline == '':
			break 
		stringlist = stringline.split()
		E = float(stringlist.pop(0))/(10**3)
		Flux = float(stringlist.pop(0))*(10**7)
		DMmuvals[E] = [Flux]
	return DMmuvals

DMmu = readDMmuflux()
Edmmu = sorted(DMmu.keys())


#+++++++++++++++++++++++++++++++++++++++++++++++++++
#+ Read DM to 100 % electron flux $ee\nu$
#+++++++++++++++++++++++++++++++++++++++++++++++++++
def readDMelflux():
	DMelfluxfile = open(DMfluxpath+ '/elflux/GAL-D2d9-d0d40-4point-el-M%dcheckdiff15z7kpc.d'%(MDM),'r')
	DMelvals = {}
	while True :
		stringline = DMelfluxfile.readline()
		if stringline == '':
			break 
		stringlist = stringline.split()
		E = float(stringlist.pop(0))/(10**3)
		Flux = float(stringlist.pop(0))*(10**7)
		DMelvals[E] = [Flux]
	return DMelvals

DMel = readDMelflux()
Edmel = sorted(DMel.keys())




#+++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+ Interpolation of Muon flux 
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++
def DMmuinterpol(Eintpol,phi):
	intmuflux = 0. 
	for m in range(len(Edmmu)):
		E2 = Edmmu[m]
		if E2 > Eintpol + phi :
			E1 = Edmmu[m-1]
			y1 = DMmu[E1][0]
			y2 = DMmu[E2][0]
			intmuflux  = y1 + ((y2 -y1)*(Eintpol+phi-E1)/(E2-E1))
			soldmmfact =  (Eintpol **2 - (0.05**2))/( (Eintpol+phi)**2 - (0.05 **2))
			#print E2, intmuflux
			return intmuflux * soldmmfact



#+++++++++++++++++++++++++++++++++++++++++++++
#+ Interpolation of Electron Flux
#+++++++++++++++++++++++++++++++++++++++++++++
def DMelinterpol(Eint,phi):
	intelflux = 0. 
	for e in range(len(Edmel)):
		E2 = Edmel[e]
		if E2 > Eint + phi:
			E1 = Edmel[e-1]
			y1 = DMel[E1][0]
			y2 = DMel[E2][0]
			intelflux  = y1 + (y2 -y1)*(Eint+phi-E1)/(E2-E1)
			#print intelflux
			soldmefact =  (Eint**2 - (0.05**2))/( (Eint+phi)**2 - (0.05 **2))
			return intelflux * soldmefact




#++++++++++++++++++++++++++++++++++++++++++++++++++
#+ Fit values obtained from best fit 800 GeV
#++++++++++++++++++++++++++++++++++++++++++++++++++
#82.8104978288
#{'ratse': 0.19234155625338947, 'phi': 0.5, 'Eg': 110.0, 'de': 0.5382823209194012, 's': 0.5, 'ce': 0.9644744480977688, 'ge': 2.9213557727925776, 'decayel': 0.05145088614061377, 'decaymu': 0.03073292636640579, 'delta': 0.4, 'E_d': 10000.0}



ce = 0.9644744480977688
ge = 2.9213557727925776
delta =0.4 
ratse = 0.19234155625338947
Eg = 110.0  
s = 0.5 
de = 0.5382823209194012
phi = 0.5
E_d = 10000
#dt=  0.00010000000000287557
dmu = 0.03073292636640579
delec = 0.05145088614061377



#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+     Generate Events by multiplying flux with bin size 
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
totevent = []
binwidth = []
newFlux = []
for i in range(len(En)):
	enhigh = 10**((i+0.5)*binwidthnumber)
	enlow  = 10**((i-0.5)*binwidthnumber)
	binsize = enhigh - enlow 
	#print binsize, enhigh 
	binwidth.append(binsize)
	bkgflux = posiparam(ce,ge,ratse,delta,phi,En[i]) + elecparam(ce,ge,ratse,delta,Eg,de,s,phi,E_d,En[i]) 
	#tauflux = dt * DMtauinterpol(En[i],phi)
	elflux = delec * DMelinterpol(En[i],phi)
	muflux = dmu * DMmuinterpol(En[i],phi)
	DMposiflux = (muflux + elflux) *2.  
	totflux = bkgflux + DMposiflux	
	newFlux.append(totflux)
	event = totflux * binsize * (fiveyear*apperture*eff)
	print binsize, event, enhigh
	totevent.append(event)


print len(totevent)
print len(binwidth)



errbar_file = open('/home/suvo/Downloads/Analysis/errorbarfiles/bplawwithcutoffandDM%dGeVnoTausm0d5phi0d5CALevent.d'%(MDM),'w')

for i in range(len(En)):
	#staterr = (math.sqrt(totevent[i]) )/ (binwidth[i] *  fiveyear*apperture*eff)  
 	calevent = totevent[i] 
	errbar_file.write('{0:2} {1:3}' .format(En[i], calevent) + "\n")
errbar_file.close()


