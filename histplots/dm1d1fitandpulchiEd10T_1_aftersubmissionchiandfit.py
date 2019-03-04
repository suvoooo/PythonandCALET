#!/usr/bin/python 

import os,math 
import numpy as np 
import sys, time, glob
import numpy as np 
#import  minuit
import time
import matplotlib.pyplot as plt
from scipy.stats import norm
import matplotlib.mlab as mlab 
from scipy import optimize
from numpy import trapz
from scipy import integrate








filepath='/home/suvo/Downloads/Analysis/DMfitDM/fitto1d1TDMwithTauEd10Ts1d0p0d5correct2/newfiles/'
pulpath='/home/suvo/Downloads/Analysis/DMfitDM/fitto1d1TDMwithTauEd10Ts1d0p0d5correct2/pulfittoDMModelA_aftersubmission/'





selectfiles = glob.glob(filepath+"brpowlaw*")



chilist = []

for sel in selectfiles :
	newfiles = open(sel, 'r')
	#headerline = newfiles.readline()
	newvals = {}
	while True :
		stringline = newfiles.readline()
		if stringline=='':
			break
		stringlist=stringline.split()
		chi = float(stringlist.pop(0))
		infoline = newfiles.readline()
		#chi   = float(stringlist.pop(0))
		#eg = float(stringlist.pop(0))
		#newvals[E] = [chi,eg]
		chilist.append(chi)



maxDM = max(chilist)
minDM = min(chilist)


j1 = [i for i in chilist if i >=101.8]

print "DM list over 95% CL: ", len(j1)


avDM =  reduce(lambda x, y: x + y, chilist) / len(chilist)

print avDM

# Equation for Gaussian DM
def f(x, a, b, c):
    return a * np.exp(-(x - b)**2.0 / (2 * c**2))








selectfiles1 = glob.glob(pulpath+"brpowlaw*")



chilistpul = []

for selpul in selectfiles1 :
	newfiles = open(selpul, 'r')
	#headerline = newfiles.readline()
	newvals = {}
	while True :
		stringline = newfiles.readline()
		if stringline=='':
			break
		stringlist=stringline.split()
		chi = float(stringlist.pop(0))
		infoline = newfiles.readline()
		#chi   = float(stringlist.pop(0))
		#eg = float(stringlist.pop(0))
		#newvals[E] = [chi,eg]
		chilistpul.append(chi+5)



maxpul = max(chilistpul)
minpul = min(chilistpul)


j2 = [k for k in chilistpul if k>101.8]
print "Pul list over 95% CL: ", len(j2)


def fpul(x, a, b, c):
    return a * np.exp(-(x - b)**2.0 / (2 * c**2))








#fig = plt.figure()
fig = plt.figure(figsize=(8.,5.))
ax = fig.add_subplot(111)
fig.patch.set_facecolor('white')
dataDM = plt.hist(chilist,bins =int(maxDM-minDM)+1,range=[minDM,maxDM],histtype='stepfilled',alpha=0.4,color='red')

# Generate data from bins as a set of points 
x1 = [0.5 * (dataDM[1][i] + dataDM[1][i+1]) for i in xrange(len(dataDM[1])-1)]
y1 = dataDM[0]

#print y1
#print x1
popt, pcov = optimize.curve_fit(f, x1, y1,p0=(60,avDM,10))



#print popt

x_fit = np.linspace(30, 110, 55)
y_fit = f(x_fit, *popt)

a = popt[0]
b= popt[1]
c=popt[2]
aDM = lambda xDM: a * np.exp(-(xDM - b)**2.0 / (2 * c**2)) 
areaDM = integrate.quad (aDM,101.8,110)
print areaDM

print "total area of DM:", a*c*(math.sqrt(2*3.141))






datapul = plt.hist(chilistpul,bins =int(maxpul-minpul)+1,range=[minpul,maxpul],histtype='stepfilled',alpha=0.4,color='green')
plt.axvline(x=101.8,ymin=0, ymax=0.71,linewidth=4,color='black')


# Generate data from bins as a set of points 
x2 = [0.5 * (datapul[1][i] + datapul[1][i+1]) for i in xrange(len(datapul[1])-1)]
y2 = datapul[0]

#print y2
#print x2
poptpul, pcovpul = optimize.curve_fit(fpul, x2, y2,p0=(36,127.,15))

apul = poptpul[0]
bpul = poptpul[1]
cpul = poptpul[2]


areapul = lambda xpul: apul * np.exp(-(xpul - bpul)**2.0 / (2 * cpul**2)) 
areapulsar = integrate.quad (areapul,101.8,141)
print areapulsar

print "total area of pulsar:", apul*cpul*(math.sqrt(2*3.141))

#print popt

x_fitpul = np.linspace(45, 145, 90)
y_fitpul = f(x_fitpul, *poptpul)




plt.plot(x_fit, y_fit, color="r", linewidth=4,alpha=0.6)

plt.plot(x_fitpul, y_fitpul, color="g", linewidth=4,alpha=0.5)





plt.ylabel('Number of Samples',fontsize=15)
plt.xlabel(r'$\chi ^2$', fontsize=19,labelpad=-13)
plt.text('33','100','DM Fit',fontsize = 17,color='hotpink')
plt.text('118','90','Pulsar Fit',fontsize = 17,color='limegreen')

plt.text('93.4','189','95% CL',fontsize = 15,color='black')

plt.ylim(0,259)
plt.xlim(29,143)

#plt.savefig('/home/suvo/Downloads/pultoDM1d1TEd10TS1d0histrefinaln_EpnfitwithTaucorrect2_aftersub.png', format='png', dpi=800)


plt.show()
