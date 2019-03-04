#!/usr/bin/python

import math
#import amsmath
import matplotlib.pyplot as plt
import numpy as np 
import  minuit

# written according to brokenpowlawandpulsar.py but with solar modulation  
datapath = '/home/suvo/Downloads/experimentdata' 
DMfluxpath = '/home/suvo/Downloads/Analysis/CALETfit/DMspectra/'
fluxatsixteen=5.073244e-02 # GeV^{-1} m^{-2}
MDM = input("Mass of DM:")


#+++++++++++++++++++++++++++++++++++++++++
# CALET new data 
#+++++++++++++++++++++++++++++++++++++++++
def readCALnewdat():
	newCALfile = open(datapath+'/CALET3TeV.dat','r')
	headerline = newCALfile.readline()
	newCALvals = {}
	while True :
		stringline = newCALfile.readline()
		if stringline =='':
			break
		stringlist = stringline.split()
		El = float(stringlist.pop(0))
		Eh = float(stringlist.pop(0))
		E = float(stringlist.pop(0))
		Enerr = float(stringlist.pop(0))
		candidate = float(stringlist.pop(0))
		contam = float(stringlist.pop(0))
		flux = float(stringlist.pop(0))
		statl = float(stringlist.pop(0))
		stath = float(stringlist.pop(0))
		statav = (statl + stath )/2.
		systnorm = float(stringlist.pop(0))
		systl = float(stringlist.pop(0))
		systh = float(stringlist.pop(0))
		systav = ( systl + systh )/2 
		toterr = math.sqrt(statav**2)
		newCALvals[E] = [flux, toterr]
		#newCALvals[E] = [flux, ]
	return newCALvals 


def plotnewCALvals(fig, newCALvals=False):
	if not newCALvals :
		newCALvals = readCALnewdat()
		Enewcal = []
		flux = []
		err = []
	for point in sorted(newCALvals.keys()):
		Enewcal.append(point)
		flux.append(newCALvals[point][0]*(point**3))
		err.append(newCALvals[point][1]*(point**3))
	#plt.plot(Enewcal,flux,'k.')	
	p = plt.errorbar(Enewcal,flux,yerr=err,fmt='k.')
	return p

CALvals = readCALnewdat()
Ecal = sorted(CALvals.keys())
'''

#+++++++++++++++++++++++++++++++++++++++++
# CALET new data 
#+++++++++++++++++++++++++++++++++++++++++
def readCALnewdat():
	newCALfile = open(datapath+'/CALET3TeV.dat','r')
	headerline = newCALfile.readline()
	newCALvals = {}
	while True :
		stringline = newCALfile.readline()
		if stringline =='':
			break
		stringlist = stringline.split()
		El = float(stringlist.pop(0))
		Eh = float(stringlist.pop(0))
		E = float(stringlist.pop(0))
		Enerr = float(stringlist.pop(0))
		candidate = float(stringlist.pop(0))
		contam = float(stringlist.pop(0))
		flux = float(stringlist.pop(0))
		statl = float(stringlist.pop(0))
		stath = float(stringlist.pop(0))
		statav = (statl + stath )/2.
		systnorm = float(stringlist.pop(0))
		systl = float(stringlist.pop(0))
		systh = float(stringlist.pop(0))
		#systav = ( systl + systh )/2 
		systerr = ( (flux * systl) + (flux * systh) )/2.
		toterr = math.sqrt(statav**2 + systerr**2)
		newCALvals[E] = [flux, toterr]
		#newCALvals[E] = [flux, ]
	return newCALvals 


def plotnewCALvals(fig, newCALvals=False):
	if not newCALvals :
		newCALvals = readCALnewdat()
		Enewcal = []
		flux = []
		err = []
	for point in sorted(newCALvals.keys()):
		Enewcal.append(point)
		flux.append(newCALvals[point][0]*(point**3))
		err.append(newCALvals[point][1]*(point**3))
	#plt.plot(Enewcal,flux,'k.')	
	p,q,r = plt.errorbar(Enewcal,flux,yerr=err,fmt='g.')
	return p

CALvals = readCALnewdat()
Ecal = sorted(CALvals.keys())

'''



#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+ Number of CALET total flux Data points in the fit range
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

freepointtot=[]
for i in range(len(CALvals)):
	if Ecal[i]>10. and Ecal[i]<=3000. :
		freepointtot.append(Ecal[i])
print len(freepointtot)




#++++++++++++++++++++++++++++++++++++++++++++++
#+     AMS-02 Positron Data
#++++++++++++++++++++++++++++++++++++++++++++++
def readAMSposiflux():
	posifile = open(datapath+'/AMS-02positron.dat','r')
	posivals = {}
	headerline = posifile.readline()
	while True :
		stringline = posifile.readline()
		if stringline =="":
			break 
		stringlist = stringline.split()
		E1 = float(stringlist.pop(0))
		E2 = float(stringlist.pop(0))
		E = (E1 + E2)/2. 
		Flux = float(stringlist.pop(0))
		stat = float(stringlist.pop(0))
		sys  = float(stringlist.pop(0))
		index = float(stringlist.pop(0))
		Flux = Flux*(10**(-index))
		stat = stat*(10**(-index))
		sys  = sys*(10**(-index))
		posivals[E] = [Flux,stat,sys] 
	return posivals 

AMSposivals = readAMSposiflux()
Eamsposi    = sorted(AMSposivals.keys())
def plotAMSposivals(fig,AMSposivals=readAMSposiflux()):
	Eams = []
	AMSposi = []
	AMSposierr = []
	for point in sorted(AMSposivals.keys()):	
		Eams.append(point)
		AMSposi.append(AMSposivals[point][0]*(point**3))
		err = math.sqrt(AMSposivals[point][1]**2 + AMSposivals[point][2]**2)
		AMSposierr.append(err*(point**3))		
	p=plt.errorbar(Eams,AMSposi,yerr=AMSposierr,fmt='.',color="black")
	return p 

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+ Number of AMS-02 total flux energy bins between the choosen fit boundary
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
freepointposi=[]
for i in range(len(AMSposivals)):
	if Eamsposi[i]>10. and Eamsposi[i]<=900. :
		freepointposi.append(Eamsposi[i])
print len(freepointposi)



#++++++++++++++++++++++++++++++
#+     Energy
#++++++++++++++++++++++++++++++
Den = []
for l in range(4000):
	ploten = 10**(l*0.001)
	Den.append(ploten)





#+++++++++++++++++++++++++++++++++++++++++++++++++++
#+ Read DM to 100 % electron flux  flux $\mu\mu\nu$
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


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+ Read 1 TeV DM to 100 % tau lepton flux $\tau\tau\nu$
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def readDMtauflux():
	DMtaufluxfile = open(DMfluxpath+ '/tauflux/GAL-D2d9-d0d40-4point-tau-M%dcheckdiff15z7kpc.d'%(MDM),'r')
	DMtauvals = {}
	while True :
		stringline = DMtaufluxfile.readline()
		if stringline == '':
			break 
		stringlist = stringline.split()
		E = float(stringlist.pop(0))/(10**3)
		Flux = float(stringlist.pop(0))*(10**7)
		DMtauvals[E] = [Flux]
	return DMtauvals

DMtau = readDMtauflux()
Edmtau = sorted(DMtau.keys())








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



#+++++++++++++++++++++++++++++++++++++++++++++
#+ Interpolation of tau Flux
#+++++++++++++++++++++++++++++++++++++++++++++
def DMtauinterpol(Etau,phi):
	inttauflux = 0. 
	for t in range(len(Edmtau)):
		E2 = Edmtau[t]
		if E2 > Etau + phi:
			E1 = Edmtau[t-1]
			y1 = DMtau[E1][0]
			y2 = DMtau[E2][0]
			intelflux  = y1 + (y2 -y1)*(Etau+phi-E1)/(E2-E1)
			#print intelflux
			soldmtfact =  (Etau**2 - (0.05**2))/( (Etau+phi)**2 - (0.05 **2))
			return inttauflux * soldmtfact











#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+ Parametrization According to arXiv: 1612.06634 / 
#+ Different for electron and positron, best realized with 
#+ solar modulation potential. This version is with SM 
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Positron parametrization 
# Similar to AMS-02 Positron fraction parametrization in 2013,2015 papers 


def posiparam(ce,ge,ratse,delta,phi,Eposi):
	nE = Eposi + phi
	checkposiflux = (ce * ((nE)**(-ge)) ) * (ratse* (nE**(-delta)))
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
	brokepow = ce *  ((newE)**(-ge-de)) * (compliterm)
	diffflux = (ratse* (newE**(-delta))) + math.exp(-newE/E_d) 
	elecflux = brokepow * diffflux
	solfact = (Eelec **2 - 0.05**2)/( newE**2 - 0.05 **2)
	#print Eelec, check1 
	return elecflux * solfact



#+++++++++++++++++++++++++++++++++++++++++++++++++++
#+ Chi Square Calculation for total flux 
#+++++++++++++++++++++++++++++++++++++++++++++++++++
def chitot(ce,ge,ratse,delta,Eg,de,s,phi,fmu,decay,E_d):
	ctot = 0. 
	kitot = []
	for i in  range(len(Ecal)):
		if Ecal[i] > 10. and Ecal[i] <= 3000. :
			muflux = fmu * DMmuinterpol(Ecal[i],phi)
			#tauflux = ftau * DMtauinterpol(Ecal[i],phi)
			#if fmu + ftau >1. :
			#	break
			#fel = max([0.01, 1-(fmu+ftau)])
			elflux = (1-fmu) * DMelinterpol(Ecal[i],phi) 
			bkgflux =  elecparam(ce,ge,ratse,delta,Eg,de,s,phi,E_d,Ecal[i])+ posiparam(ce,ge,ratse,delta,phi,Ecal[i]) 
			DMflux = (muflux + elflux)  *2 * decay 
			ctot =ctot + ((DMflux  + bkgflux - CALvals[Ecal[i]][0])**2 / CALvals[Ecal[i]][1] **2  )
			kitot.append(ctot)
			
	#print kitot[-1]
	#print ctot

	return ctot 
	


def chivaltot(ce,ge,ratse,delta,Eg,de,s,phi,fmu,decay,E_d):
	ctotval = 0. 
	kitotval = []
	for i in  range(len(Ecal)):
		if Ecal[i] > 10. and Ecal[i] <= 3000. :
			muflux = fmu * DMmuinterpol(Ecal[i],phi)
			elflux = (1-fmu) * DMelinterpol(Ecal[i],phi) 
			bkgflux =  elecparam(ce,ge,ratse,delta,Eg,de,s,phi,E_d,Ecal[i])+ posiparam(ce,ge,ratse,delta,phi,Ecal[i]) 
			DMflux = (muflux + elflux)  *2*decay 
			ctotval =ctotval + ((DMflux + bkgflux - CALvals[Ecal[i]][0])**2 / CALvals[Ecal[i]][1] **2  )
			kitotval.append(ctotval)
			#print Ecal[i], ctotval
			
	#print Ecal[i], kitot[-1]
	#print ctot
	return kitotval[-1]





#+++++++++++++++++++++++++++++++++++++++++++++++++++
#+ Chi Square Calculation for Positron Flux 
#+++++++++++++++++++++++++++++++++++++++++++++++++++

def chiposi(ce,ge,ratse,delta,phi,fmu,decay):
	cposi = 0. 
	kiposi = []
	for i in range(len(Eamsposi)):
		if Eamsposi[i] > 10. and Eamsposi[i] <= 900. :
			muflux = fmu * DMmuinterpol(Eamsposi[i],phi)
			elflux = (1-fmu) * DMelinterpol(Eamsposi[i],phi)
			DMposiflux = (muflux + elflux)*decay   
			cposi = cposi + ( (DMposiflux + posiparam(ce,ge,ratse,delta,phi,Eamsposi[i]) - AMSposivals[Eamsposi[i]][0] )**2 / (AMSposivals[Eamsposi[i]][1] **2 + AMSposivals[Eamsposi[i]][2] **2 ) ) 
			kiposi.append(cposi)
	#print kiposi[-1]
	return cposi 

def chiposival(ce,ge,ratse,delta,phi,fmu):
	cposival = 0. 
	kiposival = []
	for i in range(len(Eamsposi)):
		if Eamsposi[i] > 10. and Eamsposi[i] <= 900. :
			muflux = fmu * DMmuinterpol(Eamsposi[i],phi)
			elflux = (1-fmu)*DMelinterpol(Eamsposi[i],phi)
			DMposiflux = (muflux + elflux)*decay  
			cposival = cposival + ( (DMposiflux + posiparam(ce,ge,ratse,delta,phi,Eamsposi[i]) - AMSposivals[Eamsposi[i]][0] )**2 / (AMSposivals[Eamsposi[i]][1] **2 + AMSposivals[Eamsposi[i]][2] **2 ) ) 
			kiposival.append(cposival)
	#print kiposival[-1]
	return kiposival[-1] 





#++++++++++++++++++++++++++++++++++++++++++++++
#+ Minimization Using Migrad 
#++++++++++++++++++++++++++++++++++++++++++++++
def totchi(ce,ge,ratse,delta,Eg,de,s,phi,fmu,decay,E_d):
	return chitot(ce,ge,ratse,delta,Eg,de,s,phi,fmu,decay,E_d) + chiposi(ce,ge,ratse,delta,phi,fmu,decay)
	


m = minuit.Minuit(totchi)

m.values['ce'] = 100 
m.limits['ce'] = (1,15000)
#m.fixed['diffelec'] = True


m.values['ge'] = 3.25
m.limits['ge'] = (2.5, 4)
#m.fixed['ge'] = True


m.values['ratse'] = 0.1
m.limits['ratse'] = (0.001,0.5)


m.values['delta'] = 0.40 
#m.limits['delta'] = (3,5)
m.fixed['delta'] = True 



m.values['Eg'] = 110.0
m.limits['Eg'] = (20,80)
m.fixed['Eg'] = True



m.values['de'] = 0.3
m.limits['de'] = (0.05,0.9) 
#m.fixed['delta'] = True


m.values['s'] = 0.5
m.limits['s'] = (0.01,0.6)
m.fixed['s']=True


m.values['phi'] = 0.50
m.fixed['phi'] = True
#m.limits['phi'] = (0.4,1.2)




#m.values['decay'] = 0.45
#m.limits['decay'] = (0.001,1)
#m.fixed['decay'] = True


m.values['fmu'] = 0.3
m.limits['fmu'] = (0.,10e5)
#m.fixed['fmu'] = True

m.values['decay'] = 0.5
m.limits['decay'] = (0.001,1)
#m.fixed['decay'] = True





m.values['E_d'] = 2000
#m.limits['s'] = (0.01,0.6)
m.fixed['E_d']=True







#m.printMode = 1 
m.maxcalls = None # default number of calls is 5000, however if minimum is not found then this command is used
m.migrad()

print m.values 


#print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
ndftot  = len(freepointtot) - 7
ndfposi = len(freepointposi) - 4
#print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"



C_e = m.values['ce']
C_p = m.values['ratse']
g_e = m.values['ge']
delta = m.values['delta']
d = m.values['de']
s_f = m.values['s']
E_g = m.values['Eg']
phi = m.values['phi']
E_d = m.values['E_d']
BFm = m.values['fmu']
dt = m.values['decay']


#elbr = BFel/(BFm + BFel)
#print "elbr:", elbr

#mubr = BFm/(BFm + BFel)
#print "mubr:", mubr


#timefac = BFm + BFel 

#print "timefac:", timefac

mltfac = 3e-26
decayt = 1/(dt*mltfac)

print "total decay time:", decayt


print "calculating 1 sigma countour p5 vs p6"
sig1c=m.contour("decay","ratse",1.0)
print "calculating 2 sigma countour p5 vs p6"
sig2c=m.contour("decay","ratse",2.0)

contourlist=[sig1c,sig2c]
print contourlist

'''
print "******************************"
print "****"
print "******************************"
for cont in contourlist:
        xs=[]
        ys=[]
	tandict=[]
	atandict = {}
        for xy in cont:
		newval = math.atan2(xy[1],xy[0])
		atandict[newval]= xy
		#print newval
	for point in sorted(atandict.keys()):
		xy=atandict[point]
    		lte=1/((mltfac)*xy[0])
    		
    		xs.append(lte) 	
    		ys.append(xy[1])


print "********************"
print xs 

'''





#print for a in contourlist[sig1c[a]]

def ploterrorcontours(contourlist,param1,param2):
    fig = plt.figure()
    fig.patch.set_facecolor('white')
    concol=["b","m","r","orange","goldenrod"]
    ax1 = fig.add_subplot(1,1,1)
    i=0
    plotlist2 = []	
    for cont in contourlist:
        xs=[]
        ys=[]
	atandict = {}
        for xy in cont:
		newval = math.atan2(xy[1]-C_p,xy[0]-dt)
		atandict[newval] = xy
	for point in sorted(atandict.keys()):
		xy=atandict[point]
    		lte=1/((mltfac)*xy[0])
    		
    		xs.append(lte/1e26) 	
    		ys.append(xy[1])
	xs.append(xs[0])
	ys.append(ys[0])	
	#for a,b in zip(xs,ys):
	#	tanf = atan2(b,a)
	#	tandict.append(tanf)	   	   
        q,=plt.plot(xs, ys, color=concol[i])
	plotlist2.append(q)
	#plt.legend(handles=q,numpoints=1,loc='best',prop={'size':12.9})#,frameon=False       
        i=i+1
    #plt.xlabel(r'$\gamma _{e^-}$', fontsize=20)
    plt.xlabel(r'lifetime of DM [s]$\times 10^{26}$', fontsize=15)	
    #plt.xlabel(r'$C_{e^-} [\mathdefault{GeV}^2\,\mathdefault{s}^{-1}\, \mathdefault{m}^{-2}\, \mathdefault{sr}^{-1}]$',fontsize=13) 
    #plt.ylabel(r'$\frac{C_{\mathdefault {pwn}}}{C_{e^-}}$',fontsize=12)
    plt.ylabel(r'$\frac{C_s}{C_{e^-}}$',fontsize=17)			
    plt.xlim(4.6,7.7)
    #plt.xlim(657,703)
    plt.ylim(0.027,0.0373)
    labels=[r'$1 \sigma$ contour',r'$2\sigma$ contour']	
    plt.legend(plotlist2,labels,loc='best',prop={'size':12.9})#,frameon=False		
    #plt.ylim(0.0011,0.0026)
    #plt.subplots_adjust(left=0.1, right=0.98, top=0.97, bottom=0.12)
    #plt.savefig('./contplot/errcontplot-pul-%s-%s'%(param1,param2),dpi=600)
    plt.savefig('./errtimeatan2contplot-DM-%s-%sfinal1.png'%(param1,param2),dpi=2000)
    plt.clf()    





ploterrorcontours(contourlist,"decay","ratse")














'''
#_______________________________________________
#_ sys err best fit info
#_______________________________________________
#1100 GeV info
#{'ratse': 0.1908761809337098, 'phi': 0.5, 'Eg': 110.0, 'de': 0.5161264620091576, 'E_d': 10000.0, 's': 0.5, 'ce': 0.9603009392302654, 'ge': 2.9480910081231206, 'decayel': 0.052338423168707404, 'decaymu': 0.07632834350168594, 'delta': 0.4, 'decaytau': 0.00010000000000287557}

#800 GeV info
#37.8161647062
#{'ratse': 0.19288871009335098, 'phi': 0.5, 'Eg': 110.0, 'de': 0.5528103138318989, 'E_d': 10000.0, 's': 0.5, 'ce': 0.9692816773623774, 'ge': 2.9114246706036897, 'decayel': 0.05277166742018169, 'decaymu': 0.02433332113788156, 'delta': 0.4, 'decaytau': 0.00010000000000287557}


#800 GeV Ed 2T
#{'ratse': 0.03126345404298806, 'phi': 0.5, 'Eg': 110.0, 'de': 0.643699667517963, 's': 0.5, 'ce': 781.075260290142, 'ge': 2.817293274234041, 'decayel': 0.049686298686346664, 'decaymu': 3.14619809649308e-05, 'delta': 0.4, 'E_d': 2000.0}


C_esys = 781.075260290142
C_psys = 0.03126345404298806
g_esys = 2.817293274234041
delta = m.values['delta']
dsys = 0.643699667517963
s_f = m.values['s']
E_gsys = 110.0
phi = m.values['phi']
E_d = m.values['E_d']
BFmsys = 3.14619809649308e-05
BFtsys = 0.00010000000000287557
BFelsys = 0.049686298686346664








#+++++++++++++++++++++++++++++++++++++++++++++++
#+ PLot Total Flux 
#+++++++++++++++++++++++++++++++++++++++++++++++

def totalplot():
	Etot = []
	totflux = []
	for i in range(3900):
		En = 10**(i*0.001)
		muflux = BFm * DMmuinterpol(En,phi)
		tauflux = BFt * DMtauinterpol(En,phi)
		elflux = BFel * DMelinterpol(En,phi)
		DMposiflux = (tauflux + muflux + elflux)   
		totalflux =  elecparam(C_e,g_e,C_p,delta,E_g,d,s_f,phi,E_d,En) + posiparam(C_e,g_e,C_p,delta,phi,En)  + 2* DMposiflux
		Etot.append(En)
		totflux.append(totalflux*(En**3))
	a,=plt.plot(Etot,totflux,linestyle='-',linewidth=1,color='green')
	return a 



def secondariesplot():
	Esec = []
	secflux = []
	for i in range(3900):
		En = 10**(i*0.001)
		secondaryflux = 2*(C_e*fluxatsixteen*(En/16.)**(-g_e)) * (C_p* (En**(-delta)))
		Esec.append(En)
		secflux.append(secondaryflux)
	sec, = plt.plot(Esec,secflux,linestyle='-.',linewidth=1, color='green')
	return sec	



def totalplotsys():
	Etotsys = []
	totfluxsys = []
	for i in range(3900):
		En = 10**(i*0.001)
		muflux = BFmsys * DMmuinterpol(En,phi)
		tauflux = BFtsys * DMtauinterpol(En,phi)
		elflux = BFelsys * DMelinterpol(En,phi)
		DMposiflux = (tauflux + muflux + elflux)   
		totalflux =  elecparam(C_esys,g_esys,C_psys,delta,E_gsys,dsys,s_f,phi,E_d,En) + posiparam(C_esys,g_esys,C_psys,delta,phi,En)  + 2* DMposiflux
		Etotsys.append(En)
		totfluxsys.append(totalflux*(En**3))
	asys,=plt.plot(Etotsys,totfluxsys,linestyle='--',linewidth=3,color='palegreen')
	return asys 





def bkgplot():
	Ebkg = []
	bkgflux = []
	for k in range(3900):
		Eb = 10**(k*0.001)
		bacflux = elecparam(C_e,g_e,C_p,delta,E_g,d,s_f,phi,E_d,Eb) + posiparam(C_e,g_e,C_p,delta,phi,Eb)
		Ebkg.append(Eb)
		bkgflux.append(bacflux*(Eb**3))
	b,=plt.plot(Ebkg,bkgflux,linestyle='-.',linewidth=2,color='crimson')
	return b

def sourceintotplot():
	Etots=[]
	totsource = []
	for v in range(3900):
		es = 10**(v*0.001)
		muflux = BFm * DMmuinterpol(es,phi)
		tauflux = BFt * DMtauinterpol(es,phi)
		elflux = BFel * DMelinterpol(es,phi)
		DMposiflux = (tauflux + muflux + elflux) *2
		Etots.append(es)
		totsource.append(DMposiflux*(es**3))
	v,= plt.plot(Etots,totsource,linestyle ='--',linewidth=4,color ='lavender')
	return v




#+++++++++++++++++++++++++++++++++++++++++++++++
#+  Plot poSitrOn Flux  
#+++++++++++++++++++++++++++++++++++++++++++++++

def posiplot():
	Eposi = []
	posiflux = []
	for j in range(3900):
		Ene = 10**(j*0.001)
		muflux = BFm * DMmuinterpol(Ene,phi)
		tauflux = BFt * DMtauinterpol(Ene,phi)
		elflux = BFel * DMelinterpol(Ene,phi)
		DMposiflux = (tauflux + muflux + elflux)
		pflux = posiparam(C_e,g_e,C_p,delta,phi,Ene) + DMposiflux 
		posiflux.append(pflux*(Ene**3))
		Eposi.append(Ene)
	q,=plt.plot(Eposi,posiflux,linestyle='-.',linewidth=2,color='blue')
	return q 




def posiplotsys():
	Eposisys = []
	posifluxsys = []
	for j in range(3900):
		Ene = 10**(j*0.001)
		muflux = BFmsys * DMmuinterpol(Ene,phi)
		tauflux = BFtsys * DMtauinterpol(Ene,phi)
		elflux = BFelsys * DMelinterpol(Ene,phi)
		DMposiflux = (tauflux + muflux + elflux)
		pflux = posiparam(C_esys,g_esys,C_psys,delta,phi,Ene) + DMposiflux 
		posifluxsys.append(pflux*(Ene**3))
		Eposisys.append(Ene)
	q,=plt.plot(Eposisys,posifluxsys,linestyle='--',linewidth=2,color='dodgerblue')
	return q 






def sourceplot():
	Eposis=[]
	posisource = []
	for r in range(3900):
		es = 10**(r*0.001)
		muflux = BFm * DMmuinterpol(es,phi)
		tauflux = BFt * DMtauinterpol(es,phi)
		elflux = BFel * DMelinterpol(es,phi)
		DMposiflux = (tauflux + muflux + elflux)
		Eposis.append(es)
		posisource.append(DMposiflux*(es**3))
	r,= plt.plot(Eposis,posisource,linestyle ='-.',linewidth=2,color ='deepskyblue')
	return r 

def bkgposi():
	enposi = []
	bkgposis = []
	for w in range(3900):
		Epos = 10**(w*0.001)
		bkpsi = posiparam(C_e,g_e,C_p,delta,phi,Epos)
		enposi.append(Epos)
		bkgposis.append(bkpsi*(Epos**3))
	j, = plt.plot(enposi,bkgposis,linestyle ='-',linewidth=2, color='mediumpurple')
	return j





#+++++++++++++++++++++++++++++++++++++++++++++
#+       Figure Options 
#++++++++++++++++++++++++++++++++++++++++++++
fig = plt.figure(figsize=(12.,8.))
fig.patch.set_facecolor('white')
ax1 = plt.subplot2grid((10,1),(0,0),rowspan=5)
#ax1 = plt.subplot(111)
#ax1 = plt.subplots()
#ytot = [100,300,500] 
#labels = [r'$100$',r'$300$',r'$500$']

plt.xscale('log')
plt.yscale('linear')
#plt.yscale('linear')
#plt.xlim(0.4,9200)
#ax1.set_xlim(1.1,5200)
#ax1.set_ylim(1e1,750) general
#ax1.set_ylim(4e1,350) #special
ax1.set_ylim(0.0,281) #special
#ax1.text('10','250',r'$ \phi_T =\, 2\, C_{pn}E^{-\gamma _{pn}}e^{-E/E_{pn}} +\, C_pE^{-\gamma _p}\, +\, C_{\mathdefault{snr}}E^{-\gamma _{\mathdefault{snr}}}e^{-E/E_ {\mathdefault{snr}}}  +\, 1.55\, C_sE^{-\gamma _s}  $',fontsize=13, color = 'green')
ax1.set_ylabel(r'$\mathdefault{JE}^{3}[\mathdefault{GeV}^{2} \mathdefault{s}^{-1}\mathdefault{m}^{-2}\mathdefault{sr}^{-1}]\,\, (e^+\, +\, e^-)$',fontsize=15,color='green')
ax1.spines['left'].set_color('green')
ax1.spines['right'].set_color('blue')
#plt.ylim(-0.5,-0.1)
#plt.ylim(7e-5, 200)   #positron
#plt.ylim(1e0,850) #electron
#plt.ylim(5e1,650) # totalflux
#plt.ylim(900,88000)
#plt.ylim(40e2,10e4)#proton
#plt.ylim(10e-4,200)
#plt.xlabel('Energy(GeV)')
#plt.ylabel(r'$ E^{3.0} \times  \frac{df}{dE} {GeV}^2 m^{-1} Sr^{-1} s^{-1}$',fontsize = 15,fontweight='bold')
#plt.ylabel(r'$\gamma$ Energy Index')
#plt.ylabel(r'$\delta $')
ax1.text('90','219',r'$\mathdefault{\chi ^2 / ndf} = %3.1f/%3d$'%(chivaltot(C_e,g_e,C_p,delta,E_g,d,s_f,phi,BFm,BFt,BFel,E_d), ndftot), fontsize = 15,color = 'green')
#plt.text('10','370',r'$e^+\, +\, e^- \mathdefault{Flux}$',fontsize = 14)
#plt.yticks(ytot,labels,rotation='horizontal',fontsize=12)



ax1.text(13, 55, r'$e^+\, +\, e^-$ Flux', fontsize=15.5,
        bbox={'facecolor':'none', 'edgecolor':'green', 'pad':20})


plotlist=[]
ptot = plotnewCALvals(fig) 
plotlist.append(ptot)
a1=totalplot()
plotlist.append(a1)
asys1=totalplotsys()
plotlist.append(asys1)
#s1=secondariesplot()
#plotlist.append(s1)
b1 = bkgplot()
plotlist.append(b1)
#c1 = plotsourcetot()
#d1 = plotthesnr()
v1=sourceintotplot()
plotlist.append(v1)
#q1=plotsourceparam1()
#r1=plotsourceparam2()

#labels = ['CALET (Total)','Parametrization','Background','Source']
labels = [r'$\mathdefault{CALET}\, (e^+\, +\, e^-) $','Fit','Fit (incl. sys. error)','Background','0.8 TeV Dark Matter']

#labels = ['CALET (Total)','Parametrization','Background']
plt.legend(plotlist,labels,numpoints=1,loc='best',prop={'size':12.9})#,frameon=False)

ax1.axes.get_xaxis().set_visible(False)

#ax2=ax1.twinx()
ax2=plt.subplot2grid((10,1),(5,0),rowspan=5,sharex=ax1)

plt.xscale('log')
plt.yscale('linear')
ax2.set_xlim(8.9,3200)
ax2.set_ylim(0, 29)   #positron
ax2.set_xlabel('Energy [GeV]', fontsize=15)
ax2.set_ylabel(r'$\mathdefault{JE}^{3}[\mathdefault{GeV}^{2} \mathdefault{s}^{-1}\mathdefault{m}^{-2}\mathdefault{sr}^{-1}]\, (e^+)$',fontsize=15, color='blue')
#ax2.spines['left'].set_color('blue')
ax2.text('90','3',r'$\mathdefault{\chi ^2 / ndf} = %3.1f/%3d$'%(chiposival(C_e,g_e,C_p,delta,phi,BFm,BFt,BFel), ndfposi), fontsize =15,color='blue')


ax2.text(13, 18, r'$e^+$ Flux', fontsize=15.5,
        bbox={'facecolor':'none', 'edgecolor':'blue', 'pad':20})





#plt.text('15','80',r'$e^+ \mathdefault{Flux}$',fontsize =14)
#plt.text('30','3',r'$\phi _{e^+} =\, C_s E^{\gamma _s} +\, C_{pn}E^{\gamma _{pn}} e^{-E/E_{pn}}$', color='blue',fontsize=13)
plotlist2=[]

posipl = plotAMSposivals(fig)
plotlist2.append(posipl)

q2 = posiplot()
plotlist2.append(q2)


posys=posiplotsys()
plotlist2.append(posys)

r2 = sourceplot()
plotlist2.append(r2)

#q2 = plotsourceparaposi()
s2 = bkgposi()
plotlist2.append(r2)

#labels = ['GALPROP','AMS-02']
#labels = ['AMS-02 (Positron Flux)','Parametrization','Pulsar']
#labels = ['Fit (Proton like Function)','AMS-02']

labels = [r'$\mathdefault{AMS-02}\, (e^+)$','Fit','Fit (incl. sys. error)','0.8 TeV Dark Matter','Background']
#labels = [r'$C\times\phi_{30}(E/30.)^{\gamma}(1+ (E/R_0)^{\delta /s})^s$','AMS-02']
#labels = ['AMS-02 (Positron)','Parametrization','Background']
plt.legend(plotlist2,labels,numpoints=1,loc='best',prop={'size':12.9})#,frameon=False)
#plt.legend(labels,bbox_to_anchor=(800,600),loc=2)
#plt.grid(True,which='both')
#fig.savefig("icrc.png",dpi=80)


plt.savefig('/home/suvo/Downloads/DM0d8TEd2Tsys.eps', format='eps', dpi=1000)
#plt.show()

'''






