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
	return cosinesimilarity,len1,len2


def main():
	contextdirectory=sys.argv[1]
	compcontextvector=dict()
	originalcontext=dict()
	originalcontextyear=dict()
	groups=[]
	termsseen=set()
	origdriftfile=open(contextdirectory+"OriginalDriftSimilarityScores.txt",'w')
	#simscorefile=open(contextdirectory+"SimilarityScores.txt",'w')
	difffile=open(contextdirectory+"Diff-VectorSizes.txt",'w')
	#statsfile=open(contextdirectory+"TermGainedLostStats.txt",'w')
	for contextfile in os.listdir(contextdirectory):
		if "Context" in contextfile:

			infile=open(contextdirectory+contextfile,'r')
			year=contextfile.split("-")[0].split("::")[1]
			groups.append(year)
			contextdict = json.load(infile)
			for term in contextdict:
				if term not in originalcontext:
					originalcontext[term]=dict()
					originalcontext[term]=contextdict[term]
					originalcontextyear[term]=year
			if year not in compcontextvector:
				compcontextvector[year]=dict()
				compcontextvector[year]=contextdict
			infile.close()
			
	
	i=0
	allcontextvector=dict()
	yearlastseen=dict()
	while i<len(groups)-1:
		current=groups[i]
		next=groups[i+1]
		for term in compcontextvector[current]:
				allcontextvector[term]=compcontextvector[current][term]
				yearlastseen[term]=current

		
		# statsfile.write("Terms in\t"+current+"\t"+str(len(compcontextvector[current]))+"\n")
		# statsfile.write("Terms in\t"+next+"\t"+str(len(compcontextvector[next]))+"\n")
		missingKeys=set(compcontextvector[current].keys())-set(compcontextvector[next].keys())
		#statsfile.write("Terms lost in \t"+next+"\t"+str(len(missingKeys))+"\n")

		missingKeys=set(compcontextvector[current].keys())-termsseen
		#statsfile.write("Terms introduced in\t"+current+"\t"+str(len(missingKeys))+"\n")
		

		termsseen=set.union(termsseen, set(compcontextvector[current].keys()))
		common=set.intersection(set(compcontextvector[next].keys()),set(compcontextvector[current].keys()))
		#statsfile.write("Terms common between\t"+current+"\t"+next+"\t"+str(len(common))+"\n\n\n")
		


		for term in allcontextvector:
			if term in compcontextvector[next]:
				
				#similarity,len1,len2=consolidatevectors(allcontextvector[term],compcontextvector[next][term])
				#simscorefile.write(yearlastseen[term]+"\t"+next+"\t"+term+"\t"+str(similarity)+"\n")
				similarity,len1,len2=consolidatevectors(originalcontext[term],compcontextvector[next][term])
				origdriftfile.write(originalcontextyear[term]+"\t"+next+"\t"+term+"\t"+str(similarity)+"\n")
				difffile.write(yearlastseen[term]+"\t"+next+"\t"+term+"\t"+str(len1)+"\t"+str(len2)+"\t"+str(similarity)+"\n")
		i+=1
	
	#simscorefile.close()
	#statsfile.close()
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
	main()	