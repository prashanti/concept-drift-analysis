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
		print word,vec1[word],vec2[word]
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
	consolidatevectors(compcontextvector["1768_1866"]["UBERON:0008258"],compcontextvector["1867_1886"]["UBERON:0008258"])
	i=0
	while i<len(groups)-1:
		previous=groups[i]
		current=groups[i+1]
		print previous,current
		for term in compcontextvector[previous]:
			if term in compcontextvector[current]:
				similarity=consolidatevectors(compcontextvector[previous][term],compcontextvector[current][term])
				print previous,current,term,similarity
		i+=1
	#print consolidatevectors({"anterior": 5, "villiform": 2, "plate": 2},{"anterior":4, "wolffish": 2})	
		



if __name__ == "__main__":
	import operator
	import nltk
	import json
	import shutil
	import sys
	import os
	import math
	main()	