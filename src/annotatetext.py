# -*- coding: utf-8 -*-
def log_results(result):
	results.append(result)

def stemOntologyIDs(ontology):
	name2id={}
	ids_stem=dict()
	ontologystems=set()
	stem2id=dict()
	inp=open("../data/input/"+ontology+"_Names.xls",'r')
	for line in inp:
		data=line.split("\t")
		name=data[1].lower().strip()
		ontid=data[0].strip()
		if name not in name2id:
			name2id[name]=ontid
		temp_dict=dict()
		temp_dict=getStemmedString(name)
		stemmedname=temp_dict['StemmedString']
		if stemmedname.strip() not in stem2id:
			stem2id[stemmedname]=set()
		stem2id[stemmedname].add(name)
		if name not in ids_stem:
			ids_stem[name]=set()
		ids_stem[name].add(stemmedname)
		ontologystems.add(stemmedname)
	return ontologystems,name2id,ids_stem,stem2id

def getStemmedString(string):
	temp_dict=dict()
	splitstring=string.split(" ")
	stemmedstring=""
	for word in splitstring:
		stemmedword=word
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
	data=line.split(" ")
	origline=""
	for stem in data:
		origline=origline+" "+temp_dict[stem]
	return(origline.strip())



def worker(filename,ontologystems,name2id,ids_stem,stem2id,annotationdir,distributiondir):
	try:
		print filename
		infile=open(filename)
		filename=filename.replace("../data/ScoredCorpus/HighQualityYearlyCorpora/","")
		localtermcount=dict()
		outfile=open(annotationdir+"Annotated_"+filename,'w')
		distfile=open(distributiondir+"Distribution_"+filename,'w')
		for line in infile:
			if line.strip()!="":
				tempstem2text=getStemmedString(line)
				stemmedline=tempstem2text['StemmedString']
				matched_dict={}
				matched=0
				for stemmedterm in ontologystems:
					if word_in(stemmedterm, stemmedline):
						origontterm=stem2id[stemmedterm]
						origlineterm=getOriginalTextinLine(tempstem2text,stemmedterm)
						for term in origontterm:
							ontid=name2id[term]
							matched_dict[origlineterm]=ontid
							
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
					


					matched=1
					#
					
				if matched==1:
					outfile.write(replacedline)
				else:
					outfile.write(line)
		outfile.close()				
		infile.close()

		for term in localtermcount:
			distfile.write(term+"\t"+str(localtermcount[term])+"\n")
		distfile.close()
	except Exception,e: print str(e)	


def main():	
	pathdir=sys.argv[1]
	ontology=sys.argv[2]
	ontologystems,name2id,ids_stem,stem2id=stemOntologyIDs(ontology)
	tempstem2text=dict()
	comprehensivetermcount=dict()
	distributiondir="../data/"+ontology+"NewDistributionsExact/"
	annotationdir="../data/"+ontology+"NewAnnotatedFilesExact/"
	if not os.path.exists(distributiondir):
		os.makedirs(distributiondir)
	if not os.path.exists(annotationdir):
		os.makedirs(annotationdir)	
	
	filelist=[]
	for filename in os.listdir(pathdir):
			if "Corpus" in filename:
				filelist.append(sys.argv[1]+filename)
	
	pool = Pool(processes=cpu_count())
	for filename in filelist:
		pool.apply_async(worker, args = (filename,ontologystems,name2id,ids_stem,stem2id,annotationdir,distributiondir), callback = log_results)
	pool.close()
	pool.join()
		

				




if __name__ == "__main__":
	results=[]
	from multiprocessing import Process, Pool, cpu_count
	import re
	import sys
	import os

	main()