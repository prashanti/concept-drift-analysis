def consolidatevectors(vec1,vec2):
	words=set()
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
	return cosinesimilarity


def main():
	contextdirectory=sys.argv[1]
	compcontextvector=dict()
	groups=[]
	termsseen=set()
	simscorefile=open(contextdirectory+"SimilarityScores.txt",'w')
	
	for contextfile in os.listdir(contextdirectory):
		if "Context" in contextfile:

			infile=open(contextdirectory+contextfile,'r')
			year=contextfile.split("-")[0].split("::")[1]
			groups.append(year)
			contextdict = json.load(infile)
			if year not in compcontextvector:
				compcontextvector[year]=dict()
				compcontextvector[year]=contextdict
			infile.close()
	
	i=0
	while i<len(groups)-1:
		current=groups[i]
		future=groups[i+1]
		termsseen=set.union(termsseen, set(compcontextvector[current].keys()))
		print "Terms in ",current,len(compcontextvector[current])
		print "Terms in ",future,len(compcontextvector[future])
		missingKeys=set(compcontextvector[current].keys())-set(compcontextvector[future].keys())
		print "Terms lost in ",future,len(missingKeys)

		missingKeys=set(compcontextvector[future].keys())-termsseen
		print "Terms introduced in ",current,len(missingKeys)
		termsseen=set.union(termsseen, set(compcontextvector[future].keys()))
		common=set.intersection(set(compcontextvector[future].keys()),set(compcontextvector[current].keys()))
		print "Terms common in ",current,future,len(common)
		print "\n\n\n"
		for term in compcontextvector[current]:
			if term in compcontextvector[future]:
				similarity=consolidatevectors(compcontextvector[current][term],compcontextvector[future][term])
				simscorefile.write(current+"\t"+future+"\t"+term+"\t"+str(similarity))
		i+=1
	



if __name__ == "__main__":
	import operator
	import nltk
	import json
	import shutil
	import sys
	import os
	import math
	main()	