# -*- coding: utf-8 -*-
def stemOntologyIDs(ontology):
	global taoidname2id
	global ontologystems
	global taoids_stem
	inp=open("./InputFiles/"+ontology+"_Names.xls",'r')
	for line in inp:
		data=line.split("\t")
		name=data[1].lower().strip()
		ontid=data[0].strip()
		if name not in taoidname2id:
			taoidname2id[name]=ontid
		temp_dict=dict()
		temp_dict=getStemmedString(name)
		stemmedname=temp_dict['StemmedString']
		if stemmedname.strip() not in stem2id:
			stem2id[stemmedname]=set()
		stem2id[stemmedname].add(name)
		if name not in taoids_stem:
			taoids_stem[name]=set()
		taoids_stem[name].add(stemmedname)
		ontologystems.add(stemmedname)
		

def getStemmedString(string):
	temp_dict=dict()
	splitstring=string.split(" ")
	stemmedstring=""
	for word in splitstring:
		stemmedword=stem(word)
		temp_dict[stemmedword.strip()]=word.strip()
		stemmedstring=stemmedstring+" "+stemmedword
	temp_dict['StemmedString']=stemmedstring.strip()	
	return(temp_dict)	


 
def word_in (word, phrase):
	regex = re.compile(r'\b%s\b' % word, re.I)
	present = regex.search(phrase)
	if present:
		return True
	else:
		return False

def getOriginalTextinLine(temp_dict, line):
	#print "line",line
	#print temp_dict
	data=line.split(" ")
	origline=""
	for stem in data:
		origline=origline+" "+temp_dict[stem]
	return(origline.strip())

def joinlines():
	f=open('./InputFiles/BHLCorpus_>1900.txt','r')
	w=open('./InputFiles/BHLCorpus_Joined.txt','w')
	newline=""
	for line in f:
		words=line.split(" ")
		for word in words:
			if word.strip() is not ".":
				if word.strip() is not "":
					newline=newline+" "+word.strip()
			else:
				w.write(newline+"."+"\n")
				newline=""


def populateStopWord():
	global stopwords
	f=open('./InputFiles/stopwords.txt','r')
	for stopword in f:
		stopwords.add(stopword.strip())	


def removeStopWords(line):
	words=line.split(" ")
	stopremovedline=""
	for word in words:
		if word.lower() not in stopwords:
			stopremovedline=stopremovedline+" "+word		
	return stopremovedline



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


			

	



def main():
	# usage python MatchOntologyTerms.py /Users/pmanda/Documents/eolbhl_hackathon/InputFiles/CleanedFiles/
	#joinlines()
	#cleanfile()
	
	pathdir=sys.argv[1]
	ontology=sys.argv[2]
	stemOntologyIDs(ontology)
	tempstem2text=dict()
	count=1
	comprehensivetermcount=dict()
	compdistfile=open("./"+ontology+"Distributions/ComprehensiveDistribution.txt",'w')
	for filename in os.listdir(pathdir):
		if ".clean" in filename:
			infile=open(pathdir+filename,'r')
			localtermcount=dict()

			if not os.path.isfile("./"+ontology+"AnnotatedFiles/Annotated_"+filename):
				outfile=open("./"+ontology+"AnnotatedFiles/Annotated_"+filename,'w')
				distfile=open("./"+ontology+"Distributions/Distribution_"+filename,'w')
				print filename
				for line in infile:
					tempstem2text=getStemmedString(line)
					stemmedline=tempstem2text['StemmedString']
					matched_dict={}
					matched=0
					for stemmedterm in ontologystems:
						if word_in(stemmedterm, stemmedline):
							origontterm=stem2id[stemmedterm]
							origlineterm=getOriginalTextinLine(tempstem2text,stemmedterm)
							for term in origontterm:
								ontid=taoidname2id[term]
								matched_dict[origlineterm]=ontid
								# if origlineterm in matched_dict:
								# 	matched_dict[origlineterm].append(ontid)
								# else:
								# 	matched_dict[origlineterm]=ontid


					count+=1
					replacedline=line				
					for origlineterm in matched_dict:
						annotation=" <term> "+matched_dict[origlineterm] +" "+ origlineterm +" "+ "</term>"
						result=re.subn(r'\b%s\b' % origlineterm, annotation, replacedline)
						replacedline=result[0]
						numofmatches=result[1]

						if matched_dict[origlineterm] not in localtermcount:
							localtermcount[matched_dict[origlineterm]]=numofmatches
						else:
							localtermcount[matched_dict[origlineterm]]=localtermcount[matched_dict[origlineterm]]+numofmatches
						


						if matched_dict[origlineterm] not in comprehensivetermcount:
							comprehensivetermcount[matched_dict[origlineterm]]=numofmatches
						else:
							comprehensivetermcount[matched_dict[origlineterm]]=comprehensivetermcount[matched_dict[origlineterm]]+numofmatches
						matched=1
						#
						getContextVector(replacedline,matched_dict[origlineterm])
					if matched==1:
						outfile.write(replacedline)
					else:
						outfile.write(line)
				outfile.close()				
				infile.close()

				for term in localtermcount:
					distfile.write(term+"\t"+str(localtermcount[term])+"\n")
				distfile.close()
	print comprehensivetermcount
	for term in comprehensivetermcount:
		compdistfile.write(term+"\t"+str(comprehensivetermcount[term])+"\n")
	compdistfile.close()


				




if __name__ == "__main__":
	from stemming.porter2 import stem
	import re
	import sys
	import os
	stopwords=set()
	taoids_stem=dict()
	ontologystems=set()
	stem2id=dict()
	taoidname2id={}
	matchedontologyterms=set()
	external={}
	main()