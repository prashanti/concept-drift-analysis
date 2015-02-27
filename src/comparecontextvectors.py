def getDepth():
	depth=dict()
	infile=open("../data/input/UBERONDepth.txt")
	for line in infile:
		depth[line.split("\t")[0]]=line.split("\t")[1].strip()
	return depth

def getName():
	name=dict()
	infile=open("../data/input/UBERON_Names.txt")
	for line in infile:
		name[line.split("\t")[0]]=line.split("\t")[1].strip()
	return name

def consolidatevectors(vec1,vec2):
	words=set()
	len1=len(vec1)
	len2=len(vec2)
	for word in vec1:
		words.add(word)
	for word in vec2:
		words.add(word)
	for word in words:
		if word not in vec1:
			vec1[word]=0
		if word not in vec2:
			vec2[word]=0
	numerator=0
	denom1=0
	denom2=0
	
	for word in sorted(vec1, key=lambda key: key):
		numerator=numerator+(vec1[word]*vec2[word])
		denom1=denom1+(vec1[word] ** 2)
		denom2=denom2+(vec2[word] ** 2)


	denominator=math.sqrt(denom1)*math.sqrt(denom2)
	
	cosinesimilarity=float(numerator)/float(denominator)
	cosinedrift=1-cosinesimilarity
	return cosinedrift,len1,len2

def writePerDepth(perdepth_succ,perdepth_orig):
	perdepthsuccfile=open("../data/Stats_Graph/PerDepth_Successive.txt",'w')
	perdepthsuccfile.write("Depth\tDrift List\tMean drift\n")
	perdepthorigfile=open("../data/Stats_Graph/PerDepth_Original.txt",'w')
	perdepthorigfile.write("Depth\tDrift List\tMean drift\n")


	sorteddepth=sorted(perdepth_succ.items(), key=operator.itemgetter(0))
	
	for pair in sorteddepth:
		perdepthsuccfile.write(str(pair[0])+"\t"+str(pair[1]).strip('[]')+"\t"+str(np.mean(pair[1]))+"\n")

	sorteddepth=sorted(perdepth_orig.items(), key=operator.itemgetter(0))	
	for pair in sorteddepth:
		perdepthorigfile.write(str(pair[0])+"\t"+str(pair[1]).strip('[]')+"\t"+str(np.mean(pair[1]))+"\n")

	perdepthsuccfile.close()
	perdepthorigfile.close()


def roundnum(num):
	return round(num,2)

def writePerTerm(pertermscores_original,pertermscores_successive,uberondepth):
	name=getName()
	meansimperterm_succ=dict()
	meansimperterm_orig=dict()

	pertermsuccfile=open("../data/Stats_Graph/PerTerm_Successive.txt",'w')
	pertermsuccfile.write("Term\tNumber of comparisons\tDrift List\tMean drift\n")
	pertermorigfile=open("../data/Stats_Graph/PerTerm_Original.txt",'w')
	pertermorigfile.write("Term\tNumber of comparisons\tDrift List\tMean drift\n")

	top20origfile=open("../data/Stats_Graph/Top20_Original.txt",'w')
	top20succfile=open("../data/Stats_Graph/Top20_Successive.txt",'w')
	top20origfile.write("Term\tName\tDepth\tMean drift score\n")
	top20succfile.write("Term\tName\tDepth\tMean drift score\n")

	bottom20origfile=open("../data/Stats_Graph/Bottom20_Original.txt",'w')
	bottom20succfile=open("../data/Stats_Graph/Bottom20_Successive.txt",'w')
	bottom20origfile.write("Term\tName\tDepth\tMean drift score\n")
	bottom20succfile.write("Term\tName\tDepth\tMean drift score\n")	

	for term in pertermscores_original:
		pertermorigfile.write(term+"\t"+str(len(pertermscores_original[term]))+"\t"+str(pertermscores_original[term]).strip('[]'))
		pertermorigfile.write("\t"+str(np.mean(pertermscores_original[term]))+"\n")
		meansimperterm_orig[term]=np.mean(pertermscores_original[term])
	


	for term in pertermscores_successive:
		pertermsuccfile.write(term+"\t"+str(len(pertermscores_successive[term]))+"\t"+str(pertermscores_successive[term]).strip('[]'))
		pertermsuccfile.write("\t"+str(np.mean(pertermscores_successive[term]))+"\n")
		meansimperterm_succ[term]=np.mean(pertermscores_successive[term])


	# Write top files
		
	sortedsim=sorted(meansimperterm_orig.items(), key=operator.itemgetter(1),reverse=True)
	i=0
	for pair in sortedsim:
		if i<20:
			top20origfile.write(pair[0]+"\t" +name[pair[0]]+"\t" +str(uberondepth[pair[0]])+"\t" +str(roundnum(pair[1]))+"\n")
			i+=1

	sortedsim=sorted(meansimperterm_succ.items(), key=operator.itemgetter(1),reverse=True)
	i=0
	for pair in sortedsim:
		if i<20:
			top20succfile.write(pair[0]+"\t"+name[pair[0]]+ "\t"+ str(uberondepth[pair[0]])+"\t"+str(roundnum(pair[1]))+"\n")
			i+=1



	# Write bottom files

	sortedsim=sorted(meansimperterm_succ.items(), key=operator.itemgetter(1))
	i=0
	for pair in sortedsim:
		if i<20:
			bottom20succfile.write(pair[0]+"\t"+name[pair[0]]+ "\t"+str(uberondepth[pair[0]])+"\t" +str(roundnum(pair[1]))+"\n")
			i+=1

	sortedsim=sorted(meansimperterm_orig.items(), key=operator.itemgetter(1))
	i=0
	for pair in sortedsim:
		if i<20:
			bottom20origfile.write(pair[0]+"\t" +name[pair[0]]+"\t" + str(uberondepth[pair[0]])+"\t" +str(roundnum(pair[1]))+"\n")
			i+=1



	pertermsuccfile.close()
	pertermsuccfile.close()
	pertermorigfile.close()
	pertermorigfile.close()
	top20origfile.close()
	top20succfile.close()
	bottom20origfile.close()
	bottom20succfile.close()

def writeScores(successivecomparisonscores,originalcomparisonscores):
	successivecompfile=open("../data/Stats_Graph/Successive_Comparisons_ScoreLists.txt",'w')
	successivecompfile.write("Time period Comparison\tScoreList\n")
	originalcompfile=open("../data/Stats_Graph/Original_Comparisons_ScoreLists.txt",'w')
	originalcompfile.write("Time period Comparison\tScoreList\n")
	
	sorted_successive = sorted(successivecomparisonscores.items(), key=operator.itemgetter(0))
	for pair in sorted_successive:
		successivecompfile.write(pair[0]+"\t"+str(pair[1]).strip('[]'))
		#scores = json.dumps(pair[1],)
		#json.dump(scores, successivecompfile)
		successivecompfile.write("\n")
	successivecompfile.close()

	sorted_original = sorted(originalcomparisonscores.items(), key=operator.itemgetter(0))
	for pair in sorted_original:
		originalcompfile.write(pair[0]+"\t"+str(pair[1]).strip('[]'))
		#scores = json.dumps(pair[1],)
		#json.dump(scores, originalcompfile)
		originalcompfile.write("\n")
	originalcompfile.close()

def writeCommonGainedLostStats(termsincurrent,termsgained,termslost,termscommonwithnext):
	statsfile=open("../data/Stats_Graph/TermGainedLostStats.txt",'w')
	statsfile.write("Time Period\tTerms in Time Period\tNew Terms Introduced\tTerms Lost\n")
	commonstatsfile=open("../data/Stats_Graph/TermsCommonwithnextTPStats.txt",'w')
	commonstatsfile.write("TP1\tTP2\tNumber of common terms\n")
	
	sorted_termsincurrent = sorted(termsincurrent.items(), key=operator.itemgetter(0))
	for pair in sorted_termsincurrent:
		tp=pair[0]
		statsfile.write(tp+"\t"+ str(pair[1]) +"\t" + str(termsgained[tp]) +"\t" +str(termslost[tp])+"\n")

	sorted_termscommon = sorted(termscommonwithnext.items(), key=operator.itemgetter(0))	
	for pair in sorted_termscommon:
		tp1=pair[0]
		for tp2 in pair[1]:
			commonstatsfile.write(tp1+"\t"+tp2+"\t"+str(termscommonwithnext[tp1][tp2])+"\n")
	statsfile.close()
	statsfile.close()
	commonstatsfile.close()
	commonstatsfile.close()

def main():
	contextdirectory=sys.argv[1]
	compcontextvector=dict()
	originalcontext=dict()
	originalcontexttp=dict()
	termsgained=dict()
	termslost=dict()
	termscommonwithnext=dict()
	termsincurrent=dict()
	timeperiodset=set()
	groups=[]
	termsseen=set()
	uberondepth=getDepth()
	pertermscores_successive=dict()
	pertermscores_original=dict()
	perdepth_succ=dict()
	perdepth_orig=dict()
	


	origdriftfile=open("../data/Stats_Graph/OriginalCompDriftScores.txt",'w')
	successivedriftfile=open("../data/Stats_Graph/SuccessiveCompDriftScores.txt",'w')
	origdriftfile.write("Original TP\tTP2\tTerm\tTermDepth\tDrift Score\n")
	successivedriftfile.write("TP1\tTP2\tTerm\tTermDepth\tDrift Score\n")
	difffile=open("../data/Stats_Graph/Diff-VectorSizes.txt",'w')
	successivecomparisonscores=dict()
	originalcomparisonscores=dict()





	for contextfile in os.listdir(contextdirectory):
		if "Context" in contextfile:
			infile=open(contextdirectory+contextfile,'r')
			tp=contextfile.replace("ContextVectors_","").replace(".txt","")
			groups.append(tp)
			contextdict = json.load(infile)
			for term in contextdict:
				if term not in originalcontext:
					originalcontext[term]=dict()
					originalcontext[term]=contextdict[term]
					originalcontexttp[term]=tp
			if tp not in compcontextvector:
				compcontextvector[tp]=dict()
				compcontextvector[tp]=contextdict
			infile.close()
			
	
	
	allcontextvector=dict()
	yearlastseen=dict()
	for i in range(0,len(groups)):
		termsincurrent[groups[i]]=0
		termsgained[groups[i]]=0
		termslost[groups[i]]=0
	
	groups=sorted(groups)	

	i=0
	while i<len(groups)-1:
		current=groups[i]
		next=groups[i+1]
		successive_driftscorelist=[]
		original_driftscorelist=[]
		for term in compcontextvector[current]:
				allcontextvector[term]=compcontextvector[current][term]
				yearlastseen[term]=current

		
		termsincurrent[current]=len(compcontextvector[current])
		termsincurrent[next]=len(compcontextvector[next])
		missingKeys=set(compcontextvector[current].keys())-set(compcontextvector[next].keys())
		termslost[next]=len(missingKeys)
		missingKeys=set(compcontextvector[current].keys())-termsseen
		termsgained[current] =len(missingKeys)
		

		termsseen=set.union(termsseen, set(compcontextvector[current].keys()))
		common=set.intersection(set(compcontextvector[next].keys()),set(compcontextvector[current].keys()))
		if current not in termscommonwithnext:
			termscommonwithnext[current]=dict()
		termscommonwithnext[current][next]=len(common)
		

			
		for term in allcontextvector:
			if term in compcontextvector[next]:
				
				drift,len1,len2=consolidatevectors(allcontextvector[term],compcontextvector[next][term])
				successivedriftfile.write(yearlastseen[term]+"\t"+next+"\t"+term+"\t"   + uberondepth[term]+"\t" +str(drift)+"\n")
				successivecomparison=yearlastseen[term]+"-"+next
				successive_driftscorelist.append(drift)
				if term not in pertermscores_successive:
					pertermscores_successive[term]=[]
				pertermscores_successive[term].append(drift)

				termdepth=int(uberondepth[term])
				if termdepth not in perdepth_succ:
					perdepth_succ[termdepth]=[]
				perdepth_succ[termdepth].append(drift)


				drift,len1,len2=consolidatevectors(originalcontext[term],compcontextvector[next][term])
				origdriftfile.write(originalcontexttp[term]+"\t"+next+"\t"+term+"\t"+ uberondepth[term]+"\t" +  str(drift)+"\n")
				original_driftscorelist.append(drift)
				originalcomparison=next
				if term not in pertermscores_original:
					pertermscores_original[term]=[]
				pertermscores_original[term].append(drift)

				termdepth=int(uberondepth[term])
				if termdepth not in perdepth_orig:
					perdepth_orig[termdepth]=[]
				perdepth_orig[termdepth].append(drift)
			
				difffile.write(yearlastseen[term]+"\t"+next+"\t"+term+"\t"+str(len1)+"\t"+str(len2)+"\t"+str(drift)+"\n")

		
		successivecomparisonscores[successivecomparison]=successive_driftscorelist
		originalcomparisonscores[originalcomparison]=original_driftscorelist
		i+=1
	

	
	# writing file with depth , sim score list, mean drift
	writePerDepth(perdepth_succ,perdepth_orig)


	# writing file with term, no of comparisons, sim score list, mean drift 
	writePerTerm(pertermscores_original,pertermscores_successive,uberondepth)


	writeScores(successivecomparisonscores,originalcomparisonscores)


	writeCommonGainedLostStats(termsincurrent,termsgained,termslost,termscommonwithnext)
	
	successivedriftfile.close()
	origdriftfile.close()
	difffile.close()

	


if __name__ == "__main__":
	import operator
	import nltk
	import json
	import shutil
	import sys
	import os
	import math
	import numpy as np
	main()	