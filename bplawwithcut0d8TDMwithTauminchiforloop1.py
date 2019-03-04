#!/usr/bin/python

import math
#import amsmath
import matplotlib.pyplot as plt
import numpy as np 
import  minuit
import time
import sys

# written according to brokenpowlawwithcutoffandDMnewplotfreebranchallleptonNewCALET3TeVsolmod1norm.py but decay-time as variable for individual channel  
datapath = '/home/suvo/Downloads/experimentdata' 



DMfluxpath = '/home/suvo/Downloads/cpDMflux/'
#simCALETpath = '/home/suvo/Downloads/Analysis/DMfitDM/CAL1d1DMsimdatacopy' 
simCALETpath = '/home/suvo/Downloads/Analysis/CALET5yrs0d8TDMS1phi0d5Ed10T'
savefigpath = '/home/suvo/Downloads/Analysis/DMfitDM/newfiles/'
lownum = int(float(sys.argv[1])) #input("low val of seed:")
highnum = int(float(sys.argv[2]))  # input("high value of seed:")
caselist = []










for lo in range(lownum,highnum):
	caselist.append(lo)

print caselist
time.sleep(1)
#try :

smooth = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.0]


for sm in range(len(smooth)):
	s = smooth[sm]
	for cs in range(len(caselist)):
		fcase = caselist[cs]
		print "case No: ", fcase
		#fcase =  float(sys.argv[1])   
		#input("select sample CALET data number: ")

		fluxatsixteen=5.073244e-02 # GeV^{-1} m^{-2}
		MDM = 800 #input("Mass of DM:")

		#MDM =[600,700,720,740,760,780,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000,2400,3000,4000]

		#savefigpath = '/home/suvo/Downloads/Analysis/CALETfit/plot/checktwop/tryexpect/bplawandDM/noTau/fixrigchecksmoo/newfits/newfiles/'
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
		'''


		#+++++++++++++++++++++++++++++++++++++++++
		# CALET new data 
		#+++++++++++++++++++++++++++++++++++++++++
		def readCALnewdat():
			newCALfile = open(simCALETpath+'/CALET5yeardatacase%dwithTauDM0d8TS1p0d5noTau.d'%(fcase),'r')
			#headerline = newCALfile.readline()
			newCALvals = {}
			while True :
				stringline = newCALfile.readline()
				if stringline =='':
					break
				stringlist = stringline.split()
				E = float(stringlist.pop(0))
				flux = float(stringlist.pop(0))
				stat = float(stringlist.pop(0))
				#toterr = math.sqrt(statav**2)
				newCALvals[E] = [flux, stat]
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

		#+++++++++++++++++++++++++++++++++++++++++++++++++++
		#+ Read DM to 100 % tau flux  flux $\mu\mu\nu$
		#+++++++++++++++++++++++++++++++++++++++++++++++++++
		def readDMtauflux():
			DMtaufluxfile = open(DMfluxpath+ 'GAL-D2d9-d0d40-4point-tau-M800checkdiff15z7kpc.d','r')
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





		#+++++++++++++++++++++++++++++++++++++++++++++++++++
		#+ Read DM to 100 % muon flux  flux $\mu\mu\nu$
		#+++++++++++++++++++++++++++++++++++++++++++++++++++
		def readDMmuflux():
			DMmufluxfile = open(DMfluxpath+ 'GAL-D2d9-d0d40-4point-mu-M800checkdiff15z7kpc.d','r')
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
			DMelfluxfile = open(DMfluxpath+ 'GAL-D2d9-d0d40-4point-el-M800checkdiff15z7kpc.d','r')
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
		#+ Interpolation of tau flux 
		#+++++++++++++++++++++++++++++++++++++++++++++++++++++++
		def DMtauinterpol(Eintpol,phi):
			inttauflux = 0. 
			for m in range(len(Edmtau)):
				E2 = Edmtau[m]
				if E2 > Eintpol + phi :
					E1 = Edmtau[m-1]
					y1 = DMtau[E1][0]
					y2 = DMtau[E2][0]
					inttauflux  = y1 + ((y2 -y1)*(Eintpol+phi-E1)/(E2-E1))
					soldmmfact =  (Eintpol **2 - (0.05**2))/( (Eintpol+phi)**2 - (0.05 **2))
					#print E2, intmuflux
					return inttauflux * soldmmfact




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








		#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
		#+ Parametrization According to arXiv: 1612.06634 / 
		#+ Different for electron and positron, best realized with 
		#+ solar modulation potential. This version is with SM 
		#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
		# Positron parametrization 
		# Similar to AMS-02 Positron fraction parametrization in 2013,2015 papers 


		def posiparam(ce,ge,ratse,delta,phi,Eposi):
			nE = Eposi + phi
			checkposiflux = (ce * fluxatsixteen* ((nE/16.)**(-ge)) ) * (ratse* (nE**(-delta)))
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
			solfact = (Eelec **2 - 0.05**2)/( newE**2 - 0.05 **2)
			#print Eelec, check1 
			return elecflux * solfact





		#+++++++++++++++++++++++++++++++++++++++++++++++++++
		#+ Chi Square Calculation for total flux 
		#+++++++++++++++++++++++++++++++++++++++++++++++++++
		#+++++++++++++++++++++++++++++++++++++++++++++++++++
		#+ Chi Square Calculation for total flux 
		#+++++++++++++++++++++++++++++++++++++++++++++++++++
		def chitot(ce,ge,ratse,delta,Eg,de,s,phi,decayel,decaymu,decaytau,E_d):
			ctot = 0. 
			kitot = []
			for i in  range(len(Ecal)):
				if Ecal[i] > 10. and Ecal[i] <= 3000. :
					muflux = decaymu * DMmuinterpol(Ecal[i],phi)
					tauflux = decaytau * DMtauinterpol(Ecal[i],phi)
					#fel = max([0.01, 1-(fmu+ftau)])
					elflux = decayel * DMelinterpol(Ecal[i],phi) 
					#if elflux<0  :
					#	break
					bkgflux =  elecparam(ce,ge,ratse,delta,Eg,de,s,phi,E_d,Ecal[i])+ posiparam(ce,ge,ratse,delta,phi,Ecal[i]) 
					DMflux = (muflux + elflux+tauflux)  *2 
					ctot =ctot + ((DMflux  + bkgflux - CALvals[Ecal[i]][0])**2 / CALvals[Ecal[i]][1] **2  )
					kitot.append(ctot)
		
			#print kitot[-1]
			#print ctot

			return ctot 




		def chivaltot(ce,ge,ratse,delta,Eg,de,s,phi,decayel,decaymu,decaytau,E_d):
			ctotval = 0. 
			kitotval = []
			for i in  range(len(Ecal)):
				if Ecal[i] > 10. and Ecal[i] <= 3000. :
					muflux = decaymu * DMmuinterpol(Ecal[i],phi)
					tauflux = decaytau * DMtauinterpol(Ecal[i],phi)
					elflux = decayel * DMelinterpol(Ecal[i],phi) 
					#elflux = (1.-(fmu+ftau)) * DMelinterpol(Ecal[i],phi) 
					bkgflux =  elecparam(ce,ge,ratse,delta,Eg,de,s,phi,E_d,Ecal[i])+ posiparam(ce,ge,ratse,delta,phi,Ecal[i]) 
					DMflux = (muflux + elflux + tauflux)  *2 
					ctotval =ctotval + ((DMflux + bkgflux - CALvals[Ecal[i]][0])**2 / CALvals[Ecal[i]][1] **2  )
					kitotval.append(ctotval)
					#print Ecal[i], ctotval
		
			#print Ecal[i], kitot[-1]
			#print ctot
			return kitotval[-1]







		#+++++++++++++++++++++++++++++++++++++++++++++++++++
		#+ Chi Square Calculation for Positron Flux 
		#+++++++++++++++++++++++++++++++++++++++++++++++++++


		def chiposi(ce,ge,ratse,delta,phi,decayel,decaymu,decaytau):
			cposi = 0. 
			kiposi = []
			for i in range(len(Eamsposi)):
				if Eamsposi[i] > 10. and Eamsposi[i] <= 900. :
					muflux = decaymu * DMmuinterpol(Eamsposi[i],phi)
					tauflux = decaytau * DMtauinterpol(Eamsposi[i],phi)
					elflux = decayel * DMelinterpol(Eamsposi[i],phi)
					DMposiflux = (muflux + elflux + tauflux)  
					cposi = cposi + ( (DMposiflux + posiparam(ce,ge,ratse,delta,phi,Eamsposi[i]) - AMSposivals[Eamsposi[i]][0] )**2 / (AMSposivals[Eamsposi[i]][1] **2 + AMSposivals[Eamsposi[i]][2] **2 ) ) 
					kiposi.append(cposi)
			#print kiposi[-1]
			return cposi 

		def chiposival(ce,ge,ratse,delta,phi,decayel,decaymu,decaytau):
			cposival = 0. 
			kiposival = []
			for i in range(len(Eamsposi)):
				if Eamsposi[i] > 10. and Eamsposi[i] <= 900. :
					muflux = decaymu * DMmuinterpol(Eamsposi[i],phi)
					tauflux = decaytau * DMtauinterpol(Eamsposi[i],phi)
					elflux = decayel * DMelinterpol(Eamsposi[i],phi)
					DMposiflux = (muflux + elflux + tauflux)  
					cposival = cposival + ( (DMposiflux + posiparam(ce,ge,ratse,delta,phi,Eamsposi[i]) - AMSposivals[Eamsposi[i]][0] )**2 / (AMSposivals[Eamsposi[i]][1] **2 + AMSposivals[Eamsposi[i]][2] **2 ) ) 
					kiposival.append(cposival)
			#print kiposival[-1]
			return kiposival[-1] 







		#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
		#+ List of parameters (test)
		#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++  
		#rig = [20,25,27,30,31,33,35,37,40,42,45,48,50,53,55,60,65,70,75,80,85,90,95,100,105,110,120,130,140,150] # break energy in the power law spectrum  
		#rig = [20,22,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,55,57,60,63,65,70,75,80,85,90,95,100,110,120,135,150,180,200] # break energy in the power law spectrum  
		#smooth = [0.05,0.08,0.1,0.2,0.3,0.4,0.5,0.6,0.7] # smoothness 
		#smooth = [0.01,0.05,0.2]
		smooth = [0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.0]
		bkcutscan = [2e3,3e3,5e3,7e3,10e3]
		#solmod = [0.1,0.2,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.0] # solar modulation potential 
		solmod = [0.35,0.4,0.45,0.5,0.55,0.6,0.65]

		chilist = [] 
		minchi = {}



		#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
		#+ looped minimization (try/expect)
		#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

		def totchi(ce,ge,ratse,delta,Eg,de,s,phi,decayel,decaymu,decaytau,E_d):
			return chitot(ce,ge,ratse,delta,Eg,de,s,phi,decayel,decaymu,decaytau,E_d) + chiposi(ce,ge,ratse,delta,phi,decayel,decaymu,decaytau)




		chilist = [] 
		minchi = {}





		#for sm in range(len(smooth)):
		for p in range(len(solmod)): 
			for bkc in range(len(bkcutscan)):
				m=minuit.Minuit(totchi) 
				m.maxcalls = None	
				m.values['s'] = smooth[sm]
				m.values['phi'] = solmod[p]
				#m.fixed['Eg'] = True
				#m.fixed['E_d'] = True
				#m.fixed['Epn'] = True
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

				m.values['Eg'] = 50
				m.limits['Eg'] = (30,200)
				#m.fixed['Eg'] = True



				m.values['de'] = 0.1
				m.limits['de'] = (0.0,0.9) 
				#m.fixed['delta'] = True


				#m.values['s'] = 0.05
				#m.limits['s'] = (0.01,0.6)
				#m.fixed['s']=True


				m.values['decayel'] = 1e-4
				m.limits['decayel'] = (0.,10e2)
				#m.fixed['decay'] = True


				m.values['decaymu'] = 1e-4
				m.limits['decaymu'] = (0.,10e2)
				#m.fixed['fmu'] = True


				m.values['decaytau'] = 1e-4
				m.limits['decaytau'] = (0.,10e2)



				m.values['E_d'] = bkcutscan[bkc]
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

					m.values['Eg'] = 50
					m.limits['Eg'] = (30,200)
					#m.fixed['Eg'] = True



					m.values['de'] = 0.1
					m.limits['de'] = (0.0,0.9) 
					#m.fixed['delta'] = True


					m.values['decayel'] = 1e-4
					m.limits['decayel'] = (0.,10e2)
					#m.fixed['decay'] = True


					m.values['decaymu'] = 1e-4
					m.limits['decaymu'] = (0.,10e2)
					#m.fixed['fmu'] = True


					m.values['decaytau'] = 1e-4
					m.limits['decaytau'] = (0.,10e2)




					#m.values['E_d'] = 10000
					#m.limits['s'] = (0.01,0.6)
					#m.fixed['E_d']=True

					#print rig[b], pulcut[c], smooth[sm], solmod[p]
					#print 
					#print m.tol
					#print "Back to Drawingboard"
					#else : 
					#	break
					m.tol = 10.0*m.tol
					try :
						m.migrad()
					except:
						print "!!!!! Danger !!!!!"
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
		
				#acheck = min(chilist)	
				#if  m.fval >= acheck :
				#	pass
				#else :
				if m.fval < 110. :	
					info_file = open('./newfiles1/brpowlawcase%dchi%04dDM%2dGeVfrg%3.2fdel%0.2fdele%1.3fdmu%1.3fE_g%2dfixedsmoo%.2fslmod%1.2finfocutoff%dprcheck.d'%(fcase,m.fval,MDM,m.values['ge'],m.values['de'],m.values['decayel'],m.values['decaymu'],m.values['Eg'],m.values['s'],m.values['phi'],m.values['E_d']),'w')
			#print >>info_file, MDM, m.values['Eg'], m.fval 
					print >>info_file, m.fval
					print >>info_file, m.values
					info_file.close()




#print chilist



print "case number :", fcase
# finished guys 




