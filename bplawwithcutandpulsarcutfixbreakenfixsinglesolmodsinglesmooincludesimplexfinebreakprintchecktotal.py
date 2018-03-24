#!/usr/bin/python

import math
#import amsmath
import matplotlib.pyplot as plt
import numpy as np 
import  minuit
import time

# written according to brokenpowlawandpulsar.py but with solar modulation  
datapath = '/home/suvo/Downloads/experimentdata' 
savefigpath = '/home/suvo/Downloads/Analysis/CALETfit/plot/checktwop/tryexpect/bplawandpulsar/fixEpulcut/checksolmod/checksmoo/fixbreakenergy/finebreaken/Ed2TeV/newfiles1/'

fluxatsixteen=5.073244e-02 # GeV^{-1} m^{-2}
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
	p,q,r = plt.errorbar(Enewcal,flux,yerr=err,fmt='g.')
	return p

CALvals = readCALnewdat()
Ecal = sorted(CALvals.keys())


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
	p,q,r=plt.errorbar(Eams,AMSposi,yerr=AMSposierr,fmt='.',color="blue")
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





#++++++++++++++++++++++++++++++++++++***********
#* Source Parametrization 
#(((((((((((((((((((((((((((())))))))))))))))))))

def sourceparam(ce,ge,ratpe,indpul,phi,Epn,Epul):
	sE = Epul + phi
	sourceflux = (ce *fluxatsixteen* ((sE/16.)**(-ge)) ) * (ratpe * (sE**(indpul))) * math.exp(-sE/Epn)
	solfacts = (Epul **2 - (0.05**2))/( sE**2 - (0.05 **2))
	return sourceflux * solfacts

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




#+++++++++++++++++++++++++++++++++++++++++++++++++++
#+ Chi Square Calculation for total flux 
#+++++++++++++++++++++++++++++++++++++++++++++++++++
def chitot(ce,ge,ratse,delta,Eg,de,s,phi,ratpe,indpul,Epn,E_d):
	ctot = 0. 
	kitot = []
	for i in  range(len(Ecal)):
		if Ecal[i] > 10. and Ecal[i] <= 3000. :
			sourceterm = sourceparam(ce,ge,ratpe,indpul,phi,Epn,Ecal[i])
			ctot =ctot + ((sourceterm +elecparam(ce,ge,ratse,delta,Eg,de,s,phi,E_d,Ecal[i])+ posiparam(ce,ge,ratse,delta,phi,Ecal[i])-CALvals[Ecal[i]][0])**2 / CALvals[Ecal[i]][1] **2  )
			kitot.append(ctot)
			
	#print kitot[-1]
	#print ctot

	return ctot 
	


def chivaltot(ce,ge,ratse,delta,Eg,de,s,phi,ratpe,indpul,Epn,E_d):
	ctotval = 0. 
	kitotval = []
	for i in  range(len(Ecal)):
		if Ecal[i] > 10. and Ecal[i] <= 3000. :
			sourceterm = sourceparam(ce,ge,ratpe,indpul,phi,Epn,Ecal[i])
			ctotval =ctotval + ((sourceterm +elecparam(ce,ge,ratse,delta,Eg,de,s,phi,E_d,Ecal[i])+posiparam(ce,ge,ratse,delta,phi,Ecal[i])-CALvals[Ecal[i]][0])**2 / CALvals[Ecal[i]][1] **2  )
			kitotval.append(ctotval)
			#print Ecal[i], ctotval
			
	#print Ecal[i], kitot[-1]
	#print ctot
	return kitotval[-1]
#+++++++++++++++++++++++++++++++++++++++++++++++++++
#+ Chi Square Calculation for Positron Flux 
#+++++++++++++++++++++++++++++++++++++++++++++++++++

def chiposi(ce,ge,ratse,delta,phi,ratpe,indpul,Epn):
	cposi = 0. 
	kiposi = []
	for i in range(len(Eamsposi)):
		if Eamsposi[i] > 10. and Eamsposi[i] <= 900. :
			sourceterm = sourceparam(ce,ge,ratpe,indpul,phi,Epn,Eamsposi[i])
			cposi = cposi + ( (sourceterm + posiparam(ce,ge,ratse,delta,phi,Eamsposi[i]) - AMSposivals[Eamsposi[i]][0] )**2 / (AMSposivals[Eamsposi[i]][1] **2 + AMSposivals[Eamsposi[i]][2] **2 ) ) 
			kiposi.append(cposi)
	#print kiposi[-1]
	return cposi 

def chiposival(ce,ge,ratse,delta,phi,ratpe,indpul,Epn):
	cposival = 0. 
	kiposival = []
	for i in range(len(Eamsposi)):
		if Eamsposi[i] > 10. and Eamsposi[i] <= 900. :
			sourceterm = sourceparam(ce,ge,ratpe,indpul,phi,Epn,Eamsposi[i])
			cposival = cposival + ( (sourceterm + posiparam(ce,ge,ratse,delta,phi,Eamsposi[i]) - AMSposivals[Eamsposi[i]][0] )**2 / (AMSposivals[Eamsposi[i]][1] **2 + AMSposivals[Eamsposi[i]][2] **2 ) ) 
			kiposival.append(cposival)
	#print kiposival[-1]
	return kiposival[-1] 

#++++++++++++++++++++++++++++++++++++++++++++++
#+ Minimization Using Migrad 
#++++++++++++++++++++++++++++++++++++++++++++++
#def totchi(ce,ge,ratse,delta,Eg,de,s,phi,ratpe,indpul,Epn,E_d):
#	return chitot(ce,ge,ratse,delta,Eg,de,s,phi,ratpe,indpul,Epn,E_d) + chiposi(ce,ge,ratse,delta,phi,ratpe,indpul,Epn)
	

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+ List of parameters (test)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#rig = [25,30,31,33,35,37,40,42,45,48,50,53,55,60] # break energy in the power law spectrum  
rig = [20,22,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,55,57,60,63,65,70,75,80,85,90,95,100,110,120,135,150,180,200] # break
#smooth = [0.01,0.03,0.05,0.1] # smoothness 
smooth=[0.2]
#solmod = [0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.0] # solar modulation potential 
#solmod=[0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1]
solmod = [0.4]


pulcut=[100,110,120,130,140,150,160,170,180,190,200,220,240,270,290,300,350,400,450,500,550,600,650,700,800,900,1000,2000,3000,4000,5000,6000,7000,9000,10000]
#pulcut = [500]



#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+ looped minimization (try/expect)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def totchi(ce,ge,ratse,delta,Eg,de,s,phi,ratpe,indpul,Epn,E_d):
	return chitot(ce,ge,ratse,delta,Eg,de,s,phi,ratpe,indpul,Epn,E_d) + chiposi(ce,ge,ratse,delta,phi,ratpe,indpul,Epn)
	



chilist = [] 
minchi = {}





for c in range(len(pulcut)):
	for sm in range(len(smooth)):
		for p in range(len(solmod)):
			for b in range(len(rig)): 
				m=minuit.Minuit(totchi) 
				m.maxcalls = None	
				m.values['Eg'] = rig[b]
				m.values['Epn'] = pulcut[c]
				m.values['s'] = smooth[sm]
				m.values['phi'] = solmod[p]
				m.fixed['Eg'] = True
				#m.fixed['E_d'] = True
				m.fixed['Epn'] = True
				m.fixed['s'] = True
				m.fixed['phi'] = True
				m.values['ce'] = 1.0 
				#m.limits['ce'] = (1,1300)
				m.limits['ce'] = (0.001,100)
				#m.fixed['diffelec'] = True


				m.values['ge'] = 3.1
				m.limits['ge'] = (2.5,4)
				#m.fixed['ge'] = True


				m.values['ratse'] = 0.1
				m.limits['ratse'] = (0.01,0.5)


				m.values['delta'] = 0.40 
				#m.limits['delta'] = (3,5)
				m.fixed['delta'] = True 

				#m.values['Eg'] = 35
				#m.limits['Eg'] = (20,100)
				#m.fixed['Eg'] = True



				m.values['de'] = 0.1
				m.limits['de'] = (0.0,0.9) 
				#m.fixed['delta'] = True


				#m.values['s'] = 0.05
				#m.limits['s'] = (0.01,0.6)
				#m.fixed['s']=True


				#m.values['phi'] = 0.6
				#m.fixed['phi'] = True
				#m.limits['phi'] = (0.30,1.2)


				m.values['ratpe'] = 0.008 
				m.limits['ratpe'] = (0.0005,0.1)


				m.values['indpul'] = 0.6
				m.limits['indpul'] = (0.3,1.3)
				#m.values['Epn'] = 500
				#m.limits['Epn'] = (100,4000)
				#m.fixed['Epn'] = True



				m.values['E_d'] = 2000
				#m.limits['s'] = (0.01,0.6)
				m.fixed['E_d']=True
				#m.migrad()
				

				try :
					#m.printMode = 1 
					#m.maxcalls = False # default number of calls is 5000, however if minimum is not found then this command is used
					m.migrad()

					if m.fval < 300. :
						print "inside the migrad loop now"
						
						chilist.append(m.fval)
						minchi[m.fval] = m.values
						print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
						print "!!!!!!minimum chi so far!!!!!!!:%3.2f"%(min(chilist))
						print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
						#print m.fval 
						#print minchi.keys()
						#print m.values, m.fval #>> info_file
						#print >>info_file, m.values['Epn'], m.values['Eg'],  m.fval  						
						#print >>info_file, m.fval 
						#print >>info_file, m.values #['gammah']
						#print m.values['gammah']
					else : 
						continue 



	
				except : 
					time.sleep(2)
					print "inside the simplex loop"
					simpl = False
					simplval = {}
					#m.simplex()
					#simp_file = open(savefigpath+'brpowlawsimplexfrg%3.2fdel%0.2fCpn%.4fgpul%1.3fffixedE_g%dEpul%dsmoo%.3fslmod%1.2fchi%3.1finfocutoff%d.d'%(m.values['ge'],m.values['de'],m.values['ratpe'],m.values['indpul'],m.values['Eg'],m.values['Epn'],m.values['s'],m.values['phi'],m.fval,m.values['E_d']),'w') 
					try :
						#k=abdhsbdhs
						m.simplex()
						print m.fval 
						print m.values
						simpl = m.fval
						for pn in m.values.keys():
							simplval[pn] = m.values[pn]
						#print >>simp_file, m.fval 
						#print >>simp_file, m.values 
						#print >>simp_file, m.values['Epn'], m.values['Eg'], m.fval
					except :
						print "first simplex failed"
					m.values['ce'] = 1.0 
					#m.limits['ce'] = (1,1300)
					m.limits['ce'] = (0.001,100)
					#m.fixed['diffelec'] = True


					m.values['ge'] = 3.1
					m.limits['ge'] = (2.5,4)
					#m.fixed['ge'] = True


					m.values['ratse'] = 0.1
					m.limits['ratse'] = (0.01,0.5)


					m.values['delta'] = 0.40 
					#m.limits['delta'] = (3,5)
					m.fixed['delta'] = True 

					#m.values['Eg'] = 35
					#m.limits['Eg'] = (20,100)
					#m.fixed['Eg'] = True



					m.values['de'] = 0.1
					m.limits['de'] = (0.0,0.9) 
					#m.fixed['delta'] = True


					#m.values['s'] = 0.05
					#m.limits['s'] = (0.01,0.6)
					#m.fixed['s']=True


					#m.values['phi'] = 0.6
					#m.fixed['phi'] = True
					#m.limits['phi'] = (0.30,1.2)


					m.values['ratpe'] = 0.008 
					m.limits['ratpe'] = (0.0005,0.1)


					m.values['indpul'] = 0.6
					m.limits['indpul'] = (0.3,1.3)
					#m.values['Epn'] = 500
					#m.limits['Epn'] = (100,4000)
					#m.fixed['Epn'] = True



					m.values['E_d'] = 2000
					#m.limits['s'] = (0.01,0.6)
					m.fixed['E_d']=True

					#print rig[b], pulcut[c], smooth[sm], solmod[p]
					#print 
					print m.tol
					#print "Back to Drawingboard"
					#else : 
					#	break
					#m.tol = 1.0
					#m.simplex()
					try :
						m.simplex()
						if not simpl or m.fval < simpl :
							simpl = m.fval
							for pn in m.values.keys():
								simplval[pn] = m.values[pn]

					except :
						print "second simplex failed"	
					if m.fval == None :
						break	
				info_file = open('./newfiles/brpowlawfrg%3.2fdel%0.2fCpn%.4fgpul%1.3ffixedE_g%dfEpul%dsmoo%.3fslmod%1.2fchi%3.1finfocutoff%d.d'%(m.values['ge'],m.values['de'],m.values['ratpe'],m.values['indpul'],m.values['Eg'],m.values['Epn'],m.values['s'],m.values['phi'],m.fval,m.values['E_d']),'w')
				print >>info_file, m.values['Epn'], m.values['Eg'],  m.fval 
 				info_file.close()





#info_file.close()
#simp_file.close()


#print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
ndftot  = len(freepointtot) - 7
ndfposi = len(freepointposi) - 5
#print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"






C_e = m.values['ce']
C_p = m.values['ratse']
C_s = m.values['ratpe']
g_e = m.values['ge']
delta = m.values['delta']
g_s = m.values['indpul']
E_s = m.values['Epn']
d = m.values['de']
s_f = m.values['s']
E_g = m.values['Eg']
phi = m.values['phi']
E_d = m.values['E_d']

#+++++++++++++++++++++++++++++++++++++++++++++++
#+ PLot Total Flux 
#+++++++++++++++++++++++++++++++++++++++++++++++

def totalplot():
	Etot = []
	totflux = []
	for i in range(4000):
		En = 10**(i*0.001)
		totalflux =  elecparam(C_e,g_e,C_p,delta,E_g,d,s_f,phi,E_d,En) + posiparam(C_e,g_e,C_p,delta,phi,En) + sourceparam(C_e,g_e,C_s,g_s,phi,E_s,En)
		Etot.append(En)
		totflux.append(totalflux*(En**3))
	a,=plt.plot(Etot,totflux,linestyle='-',linewidth=1,color='green')
	return a 


def bkgplot():
	Ebkg = []
	bkgflux = []
	for k in range(4000):
		Eb = 10**(k*0.001)
		bacflux = elecparam(C_e,g_e,C_p,delta,E_g,d,s_f,phi,E_d,Eb) + posiparam(C_e,g_e,C_p,delta,phi,Eb)
		Ebkg.append(Eb)
		bkgflux.append(bacflux*(Eb**3))
	b,=plt.plot(Ebkg,bkgflux,linestyle='-.',linewidth=2,color='crimson')
	return b

def sourceintotplot():
	Etots=[]
	totsource = []
	for v in range(4000):
		es = 10**(v*0.001)
		souflux = 2*sourceparam(C_e,g_e,C_s,g_s,phi,E_s,es)
		Etots.append(es)
		totsource.append(souflux*(es**3))
	v,= plt.plot(Etots,totsource,linestyle ='--',linewidth=4,color ='lavender')
	return v

#+++++++++++++++++++++++++++++++++++++++++++++++
#+  Plot poSitrOn Flux  
#+++++++++++++++++++++++++++++++++++++++++++++++

def posiplot():
	Eposi = []
	posiflux = []
	for j in range(4000):
		Ene = 10**(j*0.001)
		pflux = posiparam(C_e,g_e,C_p,delta,phi,Ene) +  sourceparam(C_e,g_e,C_s,g_s,phi,E_s,Ene)
		posiflux.append(pflux*(Ene**3))
		Eposi.append(Ene)
	q,=plt.plot(Den,posiflux,linestyle='-.',linewidth=2,color='blue')
	return q 

def sourceplot():
	Eposis=[]
	posisource = []
	for r in range(4000):
		es = 10**(r*0.001)
		souflux =  sourceparam(C_e,g_e,C_s,g_s,phi,E_s,es)
		Eposis.append(es)
		posisource.append(souflux*(es**3))
	r,= plt.plot(Eposis,posisource,linestyle ='--',linewidth=2,color ='deepskyblue')
	return r 

def bkgposi():
	enposi = []
	bkgposis = []
	for w in range(4000):
		Epos = 10**(w*0.001)
		bkpsi = C_p * (Epos**(-g_p))
		enposi.append(Epos)
		bkgposis.append(bkpsi*(Epos**3))
	j, = plt.plot(enposi,bkgposis,linestyle ='',marker='.', markersize=2, color='mediumpurple')





#+++++++++++++++++++++++++++++++++++++++++++++
#+       Figure Options 
#++++++++++++++++++++++++++++++++++++++++++++
fig = plt.figure()
fig.patch.set_facecolor('white')
#ax1 = plt.subplot2grid((10,1),(0,0),rowspan=10)
ax1 = plt.subplot(111)
#ax1 = plt.subplots()
#ytot = [100,300,500] 
#labels = [r'$100$',r'$300$',r'$500$']

plt.xscale('log')
plt.yscale('linear')
plt.xlabel('Energy (GeV)', fontsize=18)
#plt.yscale('linear')
#plt.xlim(0.4,9200)
#ax1.set_xlim(1.1,5200)
#ax1.set_ylim(1e1,750) general
#ax1.set_ylim(4e1,350) #special
ax1.set_ylim(0,260) #special
#ax1.text('10','250',r'$ \phi_T =\, 2\, C_{pn}E^{-\gamma _{pn}}e^{-E/E_{pn}} +\, C_pE^{-\gamma _p}\, +\, C_{\mathdefault{snr}}E^{-\gamma _{\mathdefault{snr}}}e^{-E/E_ {\mathdefault{snr}}}  +\, 1.55\, C_sE^{-\gamma _s}  $',fontsize=13, color = 'green')
ax1.set_ylabel(r'$\mathdefault{JE}^{3}[\mathdefault{GeV}^{2} \mathdefault{s}^{-1}\mathdefault{m}^{-2}\mathdefault{sr}^{-1}]\,\, (e^+\, +\, e^-)$',fontsize=19,color='green')
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
ax1.text('3','169',r'$\mathdefault{\chi ^2 / ndf} = %3.1f/%3d$'%(chivaltot(C_e,g_e,C_p,delta,E_g,d,s_f,phi,C_s,g_s,E_s,E_d), ndftot), fontsize = 16,color = 'green')
#plt.text('10','370',r'$e^+\, +\, e^- \mathdefault{Flux}$',fontsize = 14)
#plt.yticks(ytot,labels,rotation='horizontal',fontsize=12)


ptot = plotnewCALvals(fig) 
a1=totalplot()
#b1 = bkgplot()
#c1 = plotsourcetot()
#d1 = plotthesnr()
v1=sourceintotplot()
#q1=plotsourceparam1()
#r1=plotsourceparam2()

#labels = ['CALET (Total)','Parametrization','Background','Source']
#labels = ['CALET (Total)','Parametrization','Background']
#plt.legend(labels,loc='best',prop={'size':11})#,frameon=False)



ax2=ax1.twinx()
plt.xscale('log')
plt.yscale('linear')
ax2.set_xlim(1.1,3200)
ax2.set_ylim(0, 29)   #positron
ax2.set_ylabel(r'$\mathdefault{JE}^{3}[\mathdefault{GeV}^{2} \mathdefault{s}^{-1}\mathdefault{m}^{-2}\mathdefault{sr}^{-1}]\, (e^+)$',fontsize=19, color='blue')
#ax2.spines['left'].set_color('blue')
ax2.text('200','5',r'$\mathdefault{\chi ^2 / ndf} = %3.1f/%3d$'%(chiposival(C_e,g_e,C_p,delta,phi,C_s,g_s,E_s), ndfposi), fontsize =16,color='blue')
#plt.text('15','80',r'$e^+ \mathdefault{Flux}$',fontsize =14)
#plt.text('30','3',r'$\phi _{e^+} =\, C_s E^{\gamma _s} +\, C_{pn}E^{\gamma _{pn}} e^{-E/E_{pn}}$', color='blue',fontsize=13)
posipl = plotAMSposivals(fig)
q2 = posiplot()
r2 = sourceplot()
#q2 = plotsourceparaposi()
#s2 = plotsecondary()
#labels = ['GALPROP','AMS-02']
#labels = ['AMS-02 (Positron Flux)','Parametrization','Pulsar']
#labels = ['Fit (Proton like Function)','AMS-02']
#labels = [r'$C\times\phi_{30}(E/30.)^{\gamma}(1+ (E/R_0)^{\delta /s})^s$','AMS-02']
#labels = ['AMS-02 (Positron)','Parametrization','Background']
#plt.legend(labels,loc='best',prop={'size':11})#,frameon=False)
#plt.legend(labels,bbox_to_anchor=(800,600),loc=2)
#plt.grid(True,which='both')
#fig.savefig("icrc.png",dpi=80)

plt.show()




