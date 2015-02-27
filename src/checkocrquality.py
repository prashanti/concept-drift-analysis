def log_results(result):
	results.append(result)

def loadwords():
	from nltk.corpus import words
	wordset=set()
	#word list from http://www-01.sil.org/linguistics/wordlists/english/wordlist/wordsEn.txt
	
	for w in words.words():
		wordset.add(w)

	words=open("../data/input/english_words.txt",'r')
	for word in words:
		wordset.add(word.lower().strip())
	

	ontologyfile=open('../data/input/UBERON_Names.xls','r')
	for line in ontologyfile:
		name=line.split("\t")[1].strip()
		words=name.split(" ")
		for word in words:
			wordset.add(word.lower().strip())

	ontologyfile=open('../data/input/VSAO_Names.xls','r')
	for line in ontologyfile:
		name=line.split("\t")[1].strip()
		words=name.split(" ")
		for word in words:
			wordset.add(word.lower().strip())

	ontologyfile=open('../data/input/TAO_Names.xls','r')
	for line in ontologyfile:
		name=line.split("\t")[1].strip()
		words=name.split(" ")
		for word in words:
			wordset.add(word.lower().strip())

	for filename in os.listdir("../data/darwin-score-master/dicts/"):
		infile=open("../data/darwin-score-master/dicts/"+filename,'r')
		for word in infile:
			wordset.add(word.lower().strip())

	return wordset

def writetofile(ofile,results):
	scorehash=dict()
	for result in results:
		if "ScoredCorpus" in result[0]:
			scorehash[result[0].split("Corpus_")[1].replace("_.txt","")]=result[1]
		else:
			scorehash[result[0].replace("../data/CleanedCorpus/","")]=result[1]	
	
	if "ScoredCorpus" in result[0]: 		
		sorted_hash = sorted(scorehash.items(), key=operator.itemgetter(0))
		
	else:	
		sorted_hash = sorted(scorehash.items(), key=operator.itemgetter(1))
	
	ofile.write("Year\tOCRScore\n")
	for tupleset in sorted_hash:
		ofile.write(tupleset[0]+"\t"+str(tupleset[1])+"\n")

	#../data/ScoredCorpus/HighQualityYearlyCorpora/Corpus_1982_.txt


	

def isword(word,wordset):
	word=word.lower().strip()	
	if word in wordset:
		return True
	else:
		return False

def main():
	print cpu_count()
	outfile=sys.argv[2]
	filelist=[]
	for filename in os.listdir(sys.argv[1]):
			filelist.append(sys.argv[1]+filename)

	wordset=loadwords()
	
	pool = Pool(processes=cpu_count())
	for filename in filelist:
		pool.apply_async(worker, args = (filename,wordset,), callback = log_results)
	pool.close()
	pool.join()
	ofile=open(outfile,'w')
	writetofile(ofile,results)
	ofile.close()

def roundoff(number):
	rounded=round(number,3)
	return rounded

def worker(filename,wordset):
	try:
		outfilename='../data/WordsNotRecognized/'+filename
		outfilename=outfilename.replace("../data/CleanedCorpus/","").replace("../data/ScoredCorpus/HighQualityYearlyCorpora/","")
		outfile=open(outfilename,'w')
		totalwordcount=0
		recognizedwordcount=0
		infile=open(filename,'r')
		for line in infile:
			if "id:" not in line and line.strip() !="":
				words=line.split(" ")
				for word in words:
					if word.strip() !="":
						totalwordcount+=1
						if isword(word,wordset):
							recognizedwordcount+=1
						else:
							outfile.write(word+"\n")
	except Exception,e:
		print str(e)
					
	outfile.close()	

	qualityscore=roundoff(float(recognizedwordcount)/(totalwordcount)*100)
	return(filename,qualityscore)




if __name__ == "__main__":
	results=[]
	from multiprocessing import Process, Pool, cpu_count
	import sys
	import os
	import operator
	main()