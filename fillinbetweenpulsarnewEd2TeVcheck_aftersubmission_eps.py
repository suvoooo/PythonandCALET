#!/usr/bin/python
import math
#import amsmath
import matplotlib.pyplot as plt
import numpy as np 
# A script to compare Pamela electron flux with GALPROP 
# plot \chi ^2 vs E_pwn with smoothness and solar modulation potential
datapath = '/home/suvo/Downloads/Analysis/CALETfit/plot/checktwop/tryexpect/bplawandpulsar/aftersubmission_pulsarcontrib/Ed2TeV'


#++++++++++++++++++++++++++++++++++++++++++++++++++++
#+ no s, phi = 0.5 marker="*", linestyle='-'
#++++++++++++++++++++++++++++++++++++++++++++++++++++


def readfiles0phi0d5():	
	s0phi0d5file=open(datapath+'/phi0d6/smoo0d0phi0d6/infosmoo0d0phi0d6.d','r')
	#headerline = s0d03phi0d3file.readline()
	s0phi0d5vals={}
	while True:
		stringline=s0phi0d5file.readline()
		if stringline=='':
			break
		stringlist=stringline.split()
		Epul=float(stringlist.pop(0))
		rig = float(stringlist.pop(0))
		chi=float(stringlist.pop(0))
		s0phi0d5vals[Epul] = [rig,chi]
	return s0phi0d5vals


Evals1 = readfiles0phi0d5()
E = sorted(Evals1.keys())
#print Evals
Egraph1 = []
chigraph1 = []
for point in sorted(Evals1.keys()):
	Egraph1.append(point)
	chigraph1.append(Evals1[point][1])


print len(Egraph1)

def plots0phi0d5chisquare(fig,s0phi0d5vals=readfiles0phi0d5()):
	cut =[]
	chisquare = []
	for point in sorted(s0phi0d5vals.keys()):
		cut.append(point)
		#cut.append(pul1info[point][1])
		chisquare.append(s0phi0d5vals[point][1])
	plt.plot(cut,chisquare,linestyle='-.',linewidth=1,marker='*',markersize=5,color='palegreen',label=r'$s=0$')




###############################################################################
#             Second s = 0.01, phi =0.5
################################################################################




#+++++++++++++++++++++++++++++++++++++++++++++++++++
#+ 3rd s=0.05, phi =0.5
#+++++++++++++++++++++++++++++++++++++++++++++++++++



def readfiles0d05phi0d5():	
	s0d05phi0d5file=open(datapath+'/phi0d5/smoo0d05phi0d5/infosmoo0d05phi0d5.d','r')
	#headerline = s0d03phi0d5file.readline()
	s0d05phi0d5vals={}
	while True:
		stringline=s0d05phi0d5file.readline()
		if stringline=='':
			break
		stringlist=stringline.split()
		Epul=float(stringlist.pop(0))
		rig = float(stringlist.pop(0))
		chi=float(stringlist.pop(0))
		s0d05phi0d5vals[Epul] = [rig,chi]
	return s0d05phi0d5vals

def plots0d05phi0d5chisquare(fig,s0d05phi0d5vals=readfiles0d05phi0d5()):
	cut =[]
	chisquare = []
	for point in sorted(s0d05phi0d5vals.keys()):
		cut.append(point)
		#cut.append(pul1info[point][1])
		chisquare.append(s0d05phi0d5vals[point][1])
	plt.plot(cut,chisquare,linestyle='-',linewidth=1,marker='o',markersize=5,color='red',label=r'$s=0.05, \phi = 0.5\,$ GV')




Evals1 = readfiles0d05phi0d5()
E = sorted(Evals1.keys())
#print Evals
Egraph1 = []
chigraph5 = []
for point in sorted(Evals1.keys()):
	Egraph1.append(point)
	chigraph5.append(Evals1[point][1])








#print Egraph3
#print chigraph3


#print len(Egraph3)



#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+  4th   s = 0.1, phi =0.5
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def readfiles0d1phi0d5():	
	s0d1phi0d5file=open(datapath+'/phi0d6/smoo0d1phi0d6/infosmoo0d1phi0d6.d','r')
	s0d1phi0d5vals={}
	while True:
		stringline=s0d1phi0d5file.readline()
		if stringline=='':
			break
		stringlist=stringline.split()
		Epul=float(stringlist.pop(0))
		rig = float(stringlist.pop(0))
		chi=float(stringlist.pop(0))
		s0d1phi0d5vals[Epul] = [rig,chi]
	return s0d1phi0d5vals

def plots0d1phi0d5chisquare(fig,s0d1phi0d5vals=readfiles0d1phi0d5()):
	cut =[]
	chisquare = []
	for point in sorted(s0d1phi0d5vals.keys()):
		cut.append(point)
		#cut.append(pul1info[point][1])
		chisquare.append(s0d1phi0d5vals[point][1])
	a,=plt.plot(cut,chisquare,linestyle='-',linewidth=1,marker='o',markersize=5,color='grey',label='s=0.1')
	#plt.plot(cut[27],chisquare[27],linestyle='',marker='o',markersize=6,color='black')
	return a










#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+  6th   s = 0.3, phi =0.5
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def readfiles0d3phi0d5():	
	s0d3phi0d5file=open(datapath+'/phi0d6/smoo0d3phi0d6/infosmoo0d3phi0d6.d','r')
	s0d3phi0d5vals={}
	while True:
		stringline=s0d3phi0d5file.readline()
		if stringline=='':
			break
		stringlist=stringline.split()
		Epul=float(stringlist.pop(0))
		rig = float(stringlist.pop(0))
		chi=float(stringlist.pop(0))
		s0d3phi0d5vals[Epul] = [rig,chi]
	return s0d3phi0d5vals

def plots0d3phi0d5chisquare(fig,s0d3phi0d5vals=readfiles0d3phi0d5()):
	cut =[]
	chisquare = []
	for point in sorted(s0d3phi0d5vals.keys()):
		cut.append(point)
		#cut.append(pul1info[point][1])
		chisquare.append(s0d3phi0d5vals[point][1])
	plt.plot(cut,chisquare,linestyle='-',linewidth=1,marker='p',markersize=5,color='purple',label='s=0.3')














#++++++++++++++++++++++++++++++++++++++++++++
#+  7th  s =0.5 , phi = 0.5
#++++++++++++++++++++++++++++++++++++++++++++




def readfiles0d5phi0d5():	
	s0d5phi0d5file=open(datapath+'/phi0d6/smoo0d5phi0d6/infosmoo0d5phi0d6.d','r')
	#headerline = s0d1phi0d5file.readline()
	s0d5phi0d5vals={}
	while True:
		stringline=s0d5phi0d5file.readline()
		if stringline=='':
			break
		stringlist=stringline.split()
		Epul=float(stringlist.pop(0))
		rig = float(stringlist.pop(0))
		chi=float(stringlist.pop(0))
		s0d5phi0d5vals[Epul] = [rig,chi]
	return s0d5phi0d5vals

def plots0d5phi0d5chisquare(fig,s0d5phi0d5vals=readfiles0d5phi0d5()):
	cut =[]
	chisquare = []
	for point in sorted(s0d5phi0d5vals.keys()):
		cut.append(point)
		#cut.append(pul1info[point][1])
		chisquare.append(s0d5phi0d5vals[point][1])
	plt.plot(cut,chisquare,linestyle='-',linewidth=1,marker='^',markersize=5,color='cyan',label='s=0.5')













#++++++++++++++++++++++++++++++++++++++++++++
#+  7th  s =0.7 , phi = 0.5
#++++++++++++++++++++++++++++++++++++++++++++




def readfiles0d7phi0d5():	
	s0d7phi0d5file=open(datapath+'/phi0d6/smoo0d7phi0d6/infosmoo0d7phi0d6.d','r')
	#headerline = s0d1phi0d5file.readline()
	s0d7phi0d5vals={}
	while True:
		stringline=s0d7phi0d5file.readline()
		if stringline=='':
			break
		stringlist=stringline.split()
		Epul=float(stringlist.pop(0))
		rig = float(stringlist.pop(0))
		chi=float(stringlist.pop(0))
		s0d7phi0d5vals[Epul] = [rig,chi]
	return s0d7phi0d5vals

def plots0d7phi0d5chisquare(fig,s0d7phi0d5vals=readfiles0d7phi0d5()):
	cut =[]
	chisquare = []
	for point in sorted(s0d7phi0d5vals.keys()):
		cut.append(point)
		#cut.append(pul1info[point][1])
		chisquare.append(s0d7phi0d5vals[point][1])
	plt.plot(cut,chisquare,linestyle='-',linewidth=1,marker='^',markersize=5,color='grey',label='s=0.7')













#++++++++++++++++++++++++++++++++++++++++++++
#+  7th  s =0.9 , phi = 0.5
#++++++++++++++++++++++++++++++++++++++++++++




def readfiles0d9phi0d5():	
	s0d9phi0d5file=open(datapath+'/phi0d6/smoo0d9phi0d6/infosmoo0d9phi0d6.d','r')
	#headerline = s0d1phi0d5file.readline()
	s0d9phi0d5vals={}
	while True:
		stringline=s0d9phi0d5file.readline()
		if stringline=='':
			break
		stringlist=stringline.split()
		Epul=float(stringlist.pop(0))
		rig = float(stringlist.pop(0))
		chi=float(stringlist.pop(0))
		s0d9phi0d5vals[Epul] = [rig,chi]
	return s0d9phi0d5vals

def plots0d9phi0d5chisquare(fig,s0d9phi0d5vals=readfiles0d9phi0d5()):
	cut =[]
	chisquare = []
	for point in sorted(s0d9phi0d5vals.keys()):
		cut.append(point)
		#cut.append(pul1info[point][1])
		chisquare.append(s0d9phi0d5vals[point][1])
	plt.plot(cut,chisquare,linestyle='-',linewidth=1,marker='<',markersize=5,color='magenta',label='s=0.9')


















#+++++++++++++++++++++++++++++++++++++++++++++++++
#+ 8th  s = 1, phi = 0.4
#++++++++++++++++++++++++++++++++++++++++++++++++++


def readfiles1phi0d5():	
	s1phi0d5file=open(datapath+'/phi0d6/smoo1d0phi0d6/infosmoo1d0phi0d6.d','r')
	#headerline = s0d1phi0d5file.readline()
	s1phi0d5vals={}
	while True:
		stringline=s1phi0d5file.readline()
		if stringline=='':
			break
		stringlist=stringline.split()
		Epul=float(stringlist.pop(0))
		rig = float(stringlist.pop(0))
		chi=float(stringlist.pop(0))
		s1phi0d5vals[Epul] = [rig,chi]
	return s1phi0d5vals

def plots1phi0d5chisquare(fig,s1phi0d5vals=readfiles1phi0d5()):
	cut =[]
	chisquare = []
	for point in sorted(s1phi0d5vals.keys()):
		cut.append(point)
		#cut.append(pul1info[point][1])
		chisquare.append(s1phi0d5vals[point][1])
	plt.plot(cut,chisquare,linestyle='-',linewidth=1,marker='>',markersize=5,color='crimson',label='s=1.0')












#+++++++++++++++++++++++++++++++++++++++++++++++++++
#+ 3rd s=0.05, phi =0.4
#+++++++++++++++++++++++++++++++++++++++++++++++++++



def readfiles0d05phi0d4():	
	s0d05phi0d4file=open(datapath+'/phi0d4/smoo0d05phi0d4/infosmoo0d05phi0d4.d','r')
	#headerline = s0d03phi0d5file.readline()
	s0d05phi0d4vals={}
	while True:
		stringline=s0d05phi0d4file.readline()
		if stringline=='':
			break
		stringlist=stringline.split()
		Epul=float(stringlist.pop(0))
		rig = float(stringlist.pop(0))
		chi=float(stringlist.pop(0))
		s0d05phi0d4vals[Epul] = [rig,chi]
	return s0d05phi0d4vals

def plots0d05phi0d4chisquare(fig,s0d05phi0d4vals=readfiles0d05phi0d4()):
	cut =[]
	chisquare = []
	for point in sorted(s0d05phi0d4vals.keys()):
		cut.append(point)
		#cut.append(pul1info[point][1])
		chisquare.append(s0d05phi0d4vals[point][1])
	plt.plot(cut,chisquare,linestyle='-',linewidth=1,marker='*',markersize=5,color='green',label=r'$s=0.05,\, \phi = 0.4\, $GV')










#+++++++++++++++++++++++++++++++++++++++++++++++++++
#+ 3rd s=0.05, phi =0.6
#+++++++++++++++++++++++++++++++++++++++++++++++++++



def readfiles0d05phi0d6():	
	s0d05phi0d6file=open(datapath+'/phi0d6/smoo0d05phi0d6/infosmoo0d05phi0d6.d','r')
	#headerline = s0d03phi0d5file.readline()
	s0d05phi0d6vals={}
	while True:
		stringline=s0d05phi0d6file.readline()
		if stringline=='':
			break
		stringlist=stringline.split()
		Epul=float(stringlist.pop(0))
		rig = float(stringlist.pop(0))
		chi=float(stringlist.pop(0))
		s0d05phi0d6vals[Epul] = [rig,chi]
	return s0d05phi0d6vals

def plots0d05phi0d6chisquare(fig,s0d05phi0d6vals=readfiles0d05phi0d6()):
	cut =[]
	chisquare = []
	for point in sorted(s0d05phi0d6vals.keys()):
		cut.append(point)
		#cut.append(pul1info[point][1])
		chisquare.append(s0d05phi0d6vals[point][1])
	plt.plot(cut,chisquare,linestyle='-',linewidth=1,marker='>',markersize=5,color='navy',label=r'$s=0.05,\, \phi = 0.6\, $GV')










'''
############################################################



#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# phi -0.4 section 
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



############################################################



#+++++++++++++++++++++++++++++++++++++++++++++++++++
#+ 3rd s=0.05, phi =0.4
#+++++++++++++++++++++++++++++++++++++++++++++++++++



def readfiles0d05phi0d4():	
	s0d05phi0d4file=open(datapath+'/Ed2TeV/sm0d05phi0d4/minchism0d05phi0d4.d','r')
	#headerline = s0d03phi0d5file.readline()
	s0d05phi0d4vals={}
	while True:
		stringline=s0d05phi0d4file.readline()
		if stringline=='':
			break
		stringlist=stringline.split()
		Epul=float(stringlist.pop(0))
		rig = float(stringlist.pop(0))
		chi=float(stringlist.pop(0))
		s0d05phi0d4vals[Epul] = [rig,chi]
	return s0d05phi0d4vals

def plots0d05phi0d4chisquare(fig,s0d05phi0d4vals=readfiles0d05phi0d4()):
	cut =[]
	chisquare = []
	for point in sorted(s0d05phi0d4vals.keys()):
		cut.append(point)
		#cut.append(pul1info[point][1])
		chisquare.append(s0d05phi0d4vals[point][1])
	plt.plot(cut,chisquare,linestyle='-',linewidth=1,marker='d',markersize=5,color='red')




#++++++++++++++++++++++++++++++++++++++++++++
#+  5th  s =0.5 , phi = 0.6
#++++++++++++++++++++++++++++++++++++++++++++




def readfiles0d5phi0d6():	
	s0d5phi0d6file=open(datapath+'/Ed2TeV/sm0d5phi0d6/minchism0d5phi0d6.d','r')
	#headerline = s0d1phi0d5file.readline()
	s0d5phi0d6vals={}
	while True:
		stringline=s0d5phi0d6file.readline()
		if stringline=='':
			break
		stringlist=stringline.split()
		Epul=float(stringlist.pop(0))
		rig = float(stringlist.pop(0))
		chi=float(stringlist.pop(0))
		s0d5phi0d6vals[Epul] = [rig,chi]
	return s0d5phi0d6vals

def plots0d5phi0d6chisquare(fig,s0d5phi0d6vals=readfiles0d5phi0d6()):
	cut =[]
	chisquare = []
	for point in sorted(s0d5phi0d6vals.keys()):
		cut.append(point)
		#cut.append(pul1info[point][1])
		chisquare.append(s0d5phi0d6vals[point][1])
	plt.plot(cut,chisquare,linestyle='-',linewidth=1,marker='^',markersize=5,color='cyan')






'''





#++++++++++++++++++++++++++++++++++++++++++++++++


maxlistphi0d6=[221.5,210.2,198.8,189.3,182.5,178.2,174.3,168.8,162.7,158.9,155.4,149.1,142.4,136.7,132.2,130.5,120.3,113.7,109.4,105.6,102.6,100.1,98.1,95.5,92,87.7,85.4,86.9,89.2,92,96.9,99.9,101.9,103.41,104.52,106.3,106.5]

minlistphi0d6=[143,124,113.7,105.2,98.5,95.5,89.1,86,83.8,82.3,81.3,81,81.3,81.8,82.1,82.2,82.7,82.96,82.9,82.7,82.22,81.9,81.6,81.4,79.96,79.0,78.4,77.8,77.78,78.19,80,81.6,82.9,83.9,84.6,85.7,86.1]


print len (maxlistphi0d6)
print len(minlistphi0d6)




maxlistphi0d5 = [197.63,185.4,176.6,174.7,173.7,167.9,162.8,158.1,153.9,150.,146.4,140.1,134.6,127.8,123.93,121.4,114.7,106.9,102,98.2,95.1,92.6,90.5,88.8,84.58,85.1,85.6,87,89.1,92.2,96.7,99.9,101.5,103.2,105,106.3,107.73]
minlistphi0d5 = [126.7,114.1,104.6,97.5,92.4,88.5,85.2,82.96,81.5,80.7,80.0,79.97,80.42,81.02,81.4,81.5,82.1,82.6,82.60,82.45,82.2,81.98,81.11,80.33,79.70,78.31,77.3,76.2,75.7,76,77.7,79.2,80.3,81.2,82,83,83.4]

#print len (maxlistphi0d5)
#print len(minlistphi0d5)





maxlistphi0d4=[178.3,159.4,151.6,145.9,143.5,142.1,142.2,144.1,146.8,144.8,141.2,134.7,129.2,123.2,119.9,117.1,108.9,103.1,97.6,93.7,90.5,87.9,85.8,85.0,85.4,85.7,86.1,87.0,88.6,91.3,95.3,98.1,100.7,102.2,103.5,105.6,107.3]

minlistphi0d4=[121.1,109,100.,93,88.7,86.34,83.3,81.3,79.96,79.80,79.32,79.23,79.8,80.6,81.1,81.3,82.1,82.7,82.8,82.7,82.7,82.6,80.8,80.2,78.5,77.25,76.4,75.3,74.9,75.2,76.7,78.1,79.2,80.1,80.8,81.8,82.1]


#print len (maxlistphi0d4)
#print len(minlistphi0d4)
#print len(Egraph1)




#++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+ figure options
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++

fig=plt.figure()
fig.patch.set_facecolor('white')
#plt.xscale('linear')
plt.xscale('log')
#plt.yscale('log')
plt.yscale('log')
#plt.xlim(0.6,3.1) # this is most general
#plt.xlim(0.4,522000) #vela pulsar
#plt.ylim(70,117)
#plt.ylim(-0.5,-0.1)
#plt.ylim(7e-5, 200)   #positron
plt.xlim(80,10350)
plt.ylim(69,200)

ychi = [75,100,150,200]
labelsychi = [r'$75$',r'$100$',r'$150$',r'$200$']

#plt.xticks(xen,labelsxen,rotation='horizontal',fontsize=14)
plt.yticks(ychi,labelsychi, rotation='horizontal',fontsize=14)




#plots0phi0d5chisquare(fig)
plots0d05phi0d5chisquare(fig)
#plots0d1phi0d5chisquare(fig)
#plots0d3phi0d5chisquare(fig)
#plots0d5phi0d5chisquare(fig)
#plots0d7phi0d5chisquare(fig)
#plots0d9phi0d5chisquare(fig)
#plots1phi0d5chisquare(fig)












plots0d05phi0d4chisquare(fig)







plots0d05phi0d6chisquare(fig)




#plt.yticks(y)
#plt.plot(y)
#plt.fill_between(Egraph1,chigraph1-error,chigraph1+error ,facecolor='blue',alpha=0.1)
plt.fill_between(Egraph1, maxlistphi0d4,minlistphi0d4,facecolor='None',alpha=0.5,hatch="//",lw=0.2,edgecolor="green")# s=0.01
plt.fill_between(Egraph1, maxlistphi0d5,minlistphi0d5,facecolor='None',alpha=0.7,hatch="||",lw=0.4,edgecolor='red')# s=0.01
plt.fill_between(Egraph1, maxlistphi0d6,minlistphi0d6,facecolor='None',alpha=0.5,hatch="\\",lw=0.2,edgecolor='blue') # s
#plt.fill_between(Egraph2, min(chigraph2),min(chigraph6),facecolor='blue')#,alpha=0.3)#s0.03
#plt.fill_between(Egraph3, min(chigraph3),min(chigraph6),facecolor='green')#,alpha=0.1)
#plt.fill_between(Egraph4, min(chigraph4),min(chigraph6),facecolor='purple')#,alpha=0.3)
#plt.fill_between(Egraph5, min(chigraph5),min(chigraph6),facecolor='magenta')#,alpha=0.4)
#plt.fill_between(Egraph7, min(chigraph7),min(chigraph6),facecolor='yellow')#,alpha=0.2)
#plt.fill_between(Egraph6, min(chigraph6),min(chigraph6),facecolor='cyan')#,alpha=0.3)
#plt.fill_between(Egraph, 69,140, where=69 <= 93, facecolor='green',alpha=0.3)
#pulenergy = [300,400,600,800,1000,1200,1400,1600,1800,2000] 
#tlabels = [r'$300$',r'$400$',r'$600$',r'$800$',r'$1000$',r'$1200$',r'$1400$',r'$1600$',r'$1800$',r'$2000$']
plt.xlabel(r'$\mathdefault{E}_{\mathdefault{pwn}}$ [GeV]',fontsize =17)
plt.ylabel(r'$\chi ^2$', fontsize = 23)
#plt.text('410','82',r'$\chi ^2=92.80$ (95% CL)', fontsize = 19,color='blue') # for positron

#b=plot1chisquare(fig)

#plt.plot([], [], color='red', linewidth=10)
#plt.plot([], [], color='blue', linewidth=10)




textstr=r'$95\, \%\, $CL'
plt.text(10490, 91.7, textstr, fontsize=13,rotation='horizontal')





plt.axhline(y=93.5, linewidth=2, color='black')



plt.legend(loc='center left',bbox_to_anchor=(0.35, 0.77),prop={'size':13.7})#,frameon=False)
#plt.text
#fig.savefig(datapath+'/plotEpulchiwithsphifixrigfine.png',dpi=110)
#plt.xticks(pulenergy,tlabels,rotation='horizontal',fontsize=14)

#plt.savefig('/home/suvo/Downloads/pulcutvschiEd2TeVn_aftersubmission.eps', format='eps', dpi=1000)

plt.show()



