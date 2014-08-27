def populatesufficientdataterms(directory):
	sufficientdataterms=set()

	datafile=open("./NewAnnotations/GroupedDistributions_10_UBERONDistributionsExact/SufficientDataTerms.txt",'r')
	for line in datafile:
		sufficientdataterms.add(line.strip())
	return sufficientdataterms

def getuberonnames():
	infile=open("./InputFiles/UBERON_Names.xls")
	names=dict()
	for line in infile:
		names[line.split("\t")[0]]=line.split("\t")[1].strip()
	return names
def main():
	uberonnames=getuberonnames()
	directory=sys.argv[1]
	aftercontext=dict()
	beforecontext=dict()
	windowsize=5
	contextdirectory=directory+"ContextVectors/"
	if not os.path.exists(contextdirectory):
		os.makedirs(contextdirectory)
	sufficientdataterms=populatesufficientdataterms(directory)
	for filename in os.listdir(directory):
		if "Annotations" in filename:
			print filename
			infile=open(directory+filename,'r')
			beforecontextfile=open(contextdirectory+(filename.replace("Annotations_","BeforeContextVectors_").replace(".clean","")),'w')
			aftercontextfile=open(contextdirectory+(filename.replace("Annotations_","AfterContextVectors_").replace(".clean","")),'w')		
			for line in infile:
				termsinline=set()
				line=line.replace("<term>","")
				line=line.replace("</term>","")
				tokens = nltk.word_tokenize(line)
				tokenizedtext=nltk.Text(tokens)
				c = nltk.ConcordanceIndex(tokenizedtext.tokens, key = lambda s: s.lower())
				for term in sufficientdataterms:
					if term in line:
						termsinline.add(term)
				
				for term in termsinline:
					if term not in aftercontext:
						aftercontext[term]=dict()
					if term not in beforecontext:
						beforecontext[term]=dict()
					name=uberonnames[term].strip()
					length=len(name.split())
					afterwords=set()
					beforewords=set()

					numofwordsafter=len(tokenizedtext.tokens)-max(c.offsets(term))-1-length
					numofwordsbefore=min(c.offsets(term))
					if numofwordsafter<5:
						windowsize=numofwordsafter
						print "Window Size After",term,windowsize
					
					i=1+length
					while i<=windowsize+length:
						for word in  [tokenizedtext.tokens[offset+i] for offset in c.offsets(term)]:
							if "UBERON" not in word and word.strip() != "":
								if word in aftercontext[term]:
									aftercontext[term][word]=aftercontext[term][word]+1
								else:
									aftercontext[term][word]=1
								afterwords.add(word)

						i+=1

					windowsize=5	
					if numofwordsbefore<5:
						print "Window size Before",windowsize
						windowsize=numofwordsbefore
					for i in range(1,windowsize+1):
						for word in  [tokenizedtext.tokens[offset-i] for offset in c.offsets(term)]:
							if "UBERON" not in word and word.strip() != "":
								if word in beforecontext[term]:
									beforecontext[term][word]=beforecontext[term][word]+1
								else:
									beforecontext[term][word]=1								
								beforewords.add(word)
			
			#print dictionaries to file
			
			json.dump(beforecontext, beforecontextfile)
			json.dump(aftercontext,aftercontextfile)
			infile.close()
			beforecontextfile.close()
			aftercontextfile.close()



def getContextVector(annotatedline,term):
	global external
	if term in external:
		internal=external[term]
	else:
		internal={}

	windowsize=5
	contextwords=[]
	words=annotatedline.strip().split(" ")
	stop=0
	beginning=0
	for word in words:
		word=word.lower().strip()
		if stop == 0 and word.strip()=="<term>":
			stop=1
			
		if stop==0 and word.strip() !="":
			if len(contextwords)<5 : 
				contextwords.append(word)
				if word in internal:
					internal[word]=internal[word]+1
				else:
					internal[word]=1


				
			else:
				contextwords.pop(0)
				contextwords.append(word)
				if word in internal:
					internal[word]=internal[word]+1
				else:
					internal[word]=1
				

		if word.strip() == "</term>":
			beginning=1
			prevlength=len(contextwords)
			newlength=prevlength+5
		if beginning ==1 and word.strip() != "</term>" and word.strip() !="":
			if len(contextwords)<newlength :
				contextwords.append(word)
				if word in internal:
					internal[word]=internal[word]+1
				else:
					internal[word]=1
	external[term]=internal

if __name__ == "__main__":
	import nltk
	import json
	import shutil
	import sys
	import os
	main()