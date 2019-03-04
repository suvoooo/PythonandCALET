#!/usr/bin/python

import math
#import amsmath
import matplotlib.pyplot as plt
import numpy as np 
import  minuit
import time
import sys

# written according to brokenpowlawandpulsar.py but with solar modulation  
datapath = '/home/suvo/Downloads/experimentdata'
simCALETpath = '/home/suvo/Downloads/Analysis/pulfitto1d1TDMEd10T_aftrersubmission_pulsarcontrib/CALET1d1TDMs1d0phi0d5sample' 
#savefigpath = '/home/suvo/Downloads/Analysis/CALET5yrsforDM1d1TnoTau/5yearsCALETfitwithpulsar/newfiles/'

fluxatsixteen=5.073244e-02 # GeV^{-1} m^{-2}
#fcase = 886 #float(sys.argv[1])   #input("select sample CALET data number: ")
lownum = int(float(sys.argv[1])) #input("low val of seed:")
highnum = int(float(sys.argv[2])) #1421 #input("high value of seed:")
caselist = []
for lo in range(lownum,highnum):
	caselist.append(lo)

print caselist

smooth=[0.0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.0]
for sm in range(len(smooth)):
	s = smooth[sm]
	for cs in range(len(caselist)):
		fcase = caselist[cs]
		#+++++++++++++++++++++++++++++++++++++++++
		# CALET new data 
		#+++++++++++++++++++++++++++++++++++++++++
		def readCALnewdat():
			newCALfile = open(simCALETpath+'/CALET5yeardatacase%dwithTauDM1d1TS1p0d5noTau.d'%(fcase),'r')
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


		#++++++++++++++++++++++++++++++++++++++++++++++++++++++
		#+ Hard Break Electron parametrization
		#++++++++++++++++++++++++++++++++++++++++++++++++++++++
		def elecparamhardbreak(ce,ge,ratse,delta,Eg,de,phi,E_d,Eelec):
			newE = Eelec + phi 
			if Eelec < Eg :
				flb =	ce * fluxatsixteen* ((newE/16.)**(-ge-de)) 
				diffflux = (ratse* (newE**(-delta))) + math.exp(-newE/E_d) 
				elecflux = flb * diffflux
			else :
				fll = ce * fluxatsixteen* ( newE/(Eg) )**(-ge)  * ((Eg/16.)**(-ge-de))
				diffflux = (ratse* (newE**(-delta))) + math.exp(-newE/E_d)
				elecflux = fll * diffflux
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
					sourceterm = 2*sourceparam(ce,ge,ratpe,indpul,phi,Epn,Ecal[i])
					if s == 0.:
						ctot =ctot + ((sourceterm +elecparamhardbreak(ce,ge,ratse,delta,Eg,de,phi,E_d,Ecal[i])+ posiparam(ce,ge,ratse,delta,phi,Ecal[i])-CALvals[Ecal[i]][0])**2 / CALvals[Ecal[i]][1] **2  )
						kitot.append(ctot)
					else: 
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
					sourceterm = 2*sourceparam(ce,ge,ratpe,indpul,phi,Epn,Ecal[i])
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
		#rig = [38,39,40,42,44,45,46,48,50,52,55,57,60,65,70,75,80,85,90,95,100] # break
		#smooth = [0.01,0.03,0.05,0.1] # smoothness 
		#smooth=[0.0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.0]
		#smooth = [0.01,0.03,0.05,0.1,0.3,0.5,0.7]
		#solmod = [0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.0] # solar modulation potential 
		#solmod=[0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1]
		solmod = [0.35,0.4,0.45,0.5,0.55,0.6,0.65]

		bkgcutscan = [2e3,3e3,5e3,7e3,10e3] 
		#pulcut=[140,160,180,200,240,270,300,350,400,450,500,550,600]
		#pulcut = [500]



		#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
		#+ looped minimization (try/expect)
		#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
		def totchi(ce,ge,ratse,delta,Eg,de,s,phi,ratpe,indpul,Epn,E_d):
			return chitot(ce,ge,ratse,delta,Eg,de,s,phi,ratpe,indpul,Epn,E_d) + chiposi(ce,ge,ratse,delta,phi,ratpe,indpul,Epn)




		chilist = [] 
		minchi = {}





		#for c in range(len(pulcut)):
		#for sm in range(len(smooth)):
		for p in range(len(solmod)):
			#for b in range(len(rig)): 
			for bkc in range(len(bkgcutscan)):
				m=minuit.Minuit(totchi) 
				m.maxcalls = None	
				#m.values['Eg'] = rig[b]
				m.values['Epn'] = 200
				m.limits['Epn'] = (100,10e3)
				m.values['s'] = smooth[sm]
				m.values['phi'] = solmod[p]
				#m.fixed['Eg'] = True
				#m.fixed['E_d'] = True
				#m.fixed['Epn'] = 
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

				m.values['Eg'] = 35
				m.limits['Eg'] = (20,170)
				#m.fixed['Eg'] = True



				m.values['de'] = 0.1
				m.limits['de'] = (0.0,0.9) 
				#m.fixed['delta'] = True

				m.values['ratpe'] = 0.008 
				m.limits['ratpe'] = (0.0001,0.1)


				m.values['indpul'] = 0.6
				m.limits['indpul'] = (0.3,1.5)

				m.values['E_d'] = bkgcutscan[bkc]
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

					m.values['Eg'] = 35
					m.limits['Eg'] = (20,170)
					#m.fixed['Eg'] = True

					m.values['de'] = 0.1
					m.limits['de'] = (0.0,0.9) 
					#m.fixed['delta'] = True

					m.values['ratpe'] = 0.008 
					m.limits['ratpe'] = (0.0001,0.1)


					m.values['indpul'] = 0.6
					m.limits['indpul'] = (0.3,1.5)
					m.values['Epn'] = 200
					m.limits['Epn'] = (100,10000)
					#m.fixed['Epn'] = True



					#m.values['E_d'] = 10000
					#m.limits['s'] = (0.01,0.6)
					#m.fixed['E_d']=True

					#print rig[b], pulcut[c], smooth[sm], solmod[p]
					#print 
					print m.tol
					#print "Back to Drawingboard"
					#else : 
					#	break
					m.tol = 10.0* m.tol
					try:						
						m.migrad()
					except:
						print "!!!!! Danger !!!!"
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
				#if  m.fval > acheck:
				#	pass 
				#else :
				if m.fval < 172. :
					info_file = open('./newfiles4/brpowlawcase%dchi%04dfrg%3.2fdel%0.2ffixedE_g%dfEpul%dsmoo%.3fslmod%1.2finfocutoff%d.d'%(fcase,m.fval,m.values['ge'],m.values['de'],m.values['Eg'],m.values['Epn'],m.values['s'],m.values['phi'],m.values['E_d']),'w')
					print >>info_file, m.fval 
					print >>info_file, m.values
					info_file.close()





print "case number :", fcase 

#info_file.close()
#simp_file.close()


