#!/usr/bin/python

import matplotlib.pyplot as plt


saveDMpath = '/home/suvo/Downloads/Analysis/DMfitDM/fitto1d1TDMwithTauEd10Ts1d0p0d5correct2/newfiles/'
saveDMfilename = saveDMpath+"info1d1TDMs1d0Ed10Tfitallchi_check.d"



savepulpath = '/home/suvo/Downloads/Analysis/DMfitDM/fitto1d1TDMwithTauEd10Ts1d0p0d5correct2/pulfittoDMModelA_aftersubmission/'
savepulfilename = savepulpath+"infopulfittoDMModelA_check.d"






chilistpul = []


#pulfile = open(pulpath+'pulchivals.d', 'r')
#headerline = newfiles.readline()
#newvals = {}


pulfile = open(savepulpath+'infopulfittoDMModelA_check.d', 'r')
while True :
	stringline = pulfile.readline()
	if stringline=='':
		break
	stringlist=stringline.split()
	chipul = float(stringlist.pop(0))
	#infoline = newfiles.readline()
	#chi   = float(stringlist.pop(0))
	#eg = float(stringlist.pop(0))
	#newvals[E] = [chi,eg]
	chilistpul.append(chipul)





chilistDM=[]

DMfile = open(saveDMfilename,'r')
while True:
	stringline=DMfile.readline()
	if stringline=='':
		break
	stringlist=stringline.split()
	chiDM=float(stringlist.pop(0))
	chilistDM.append(chiDM)





chidiff=[]

for a,b in zip(chilistpul,chilistDM):
	diff = a -b
	chidiff.append(diff)





avg = sum(chidiff)/len(chidiff)
print "average chi diff: %3.2f"%(avg)






nsamp=[d for d in chidiff if d>0]

print "samples with positive chi square difference: %d"%(len(nsamp))





critchi = [cc for cc in chidiff if cc<-7.81473 ]
print "samples with chi square difference less than cc: %d"%(len(critchi))


critchiDM = [cc for cc in chidiff if cc>7.81473 ]
print "samples with chi square difference less than cc DM: %d"%(len(critchiDM))


ratio = (len(critchi) + len(critchiDM))/(len(critchi))
print "ratio: %3.2f"%(ratio)

maxdiff = max(chidiff)
mindiff = min(chidiff)-5
#for point in sorted(newvals.keys()):
#	d_file.write('{0:2}' .format(point, newvals[point][0], newvals[point][1]) + "\n")


fig = plt.figure(figsize=(8.,5.))

fig.patch.set_facecolor('white')


plt.ylabel('Number of Samples',fontsize=13)
plt.xlabel(r'$\chi ^2 _{\mathdefault{pulsar}}\, -\, \chi ^2 _{\mathdefault{DM}}$', fontsize=15,labelpad=-13)

plt.xlim(-57,104)

xticks=[-45,0,45,90]
xticklabel=[r'$-45$',r'$0$',r'$45$',r'$90$']
plt.xticks(xticks,xticklabel,fontsize=13)

plt.hist(chidiff,bins=int(maxdiff-mindiff)+1,range=[mindiff,maxdiff],histtype='stepfilled')
plt.axvline(x=-7.81473,ymin=0, ymax=0.65,linewidth=4,color='black')
plt.text(-16, 114, r'$\chi ^2 _{\mathdefault{critical}}$',fontsize=17)



plt.savefig('/home/suvo/Downloads/chidiffDMModelA_withTaucorrect2_aftersub_nonnested.png', format='png', dpi=800)




plt.show()
