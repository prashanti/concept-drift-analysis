
def consolidate(infilename,countperterm):
	infile=open(infilename,'r')
	temp=dict()
	for line in infile:
		term=line.split("\t")[0].strip()
		count=int(line.split("\t")[1].strip())
		if term in temp:
			temp[term]=temp[term]+count
		else:
			temp[term]=count

		if term in countperterm:
			countperterm[term]=countperterm[term]+count
		else:
			countperterm[term]=count
	infile.close()
	outfile=open(infilename,'w')
	for term in temp:
		if temp[term] !=0:
			outfile.write(term+"\t"+str(temp[term])+"\n")
	outfile.close()
	return(countperterm)

def getuberonnames():
	infile=open("../data/input/UBERON_Names.xls")
	names=dict()
	for line in infile:
		names[line.split("\t")[0]]=line.split("\t")[1].strip()
	return names

def getcommonterms(pathdir,sufficientdataterms):
	commonterms=dict()
	commontermsset=set()
	filecount=0
	for filename in os.listdir(pathdir):
		if "Distributions_" in filename:
			filecount+=1
			infile=open(pathdir+filename,'r')
			for line in infile:
				term=line.split("\t")[0].strip()
				count=int(line.split("\t")[1].strip())
				if term in commonterms:
					commonterms[term]=commonterms[term]+1
				else:
					commonterms[term]=1
			infile.close()
	names=getuberonnames()
	outfile=open(pathdir+"Commonterms.txt",'w')
	for term in commonterms:
		if commonterms[term] ==filecount:
			commontermsset.add(term)
			outfile.write(term+"\t"+names[term]+"\n")
	#print "Number of common terms",len(set.intersection(commontermsset,sufficientdataterms))
	outfile.close()	

def gettotalnumberofannotations(peryearcountsfile):
	annotationcount=0
	percounthash=dict()
	infile=open(peryearcountsfile)
	for line in infile:
		if "Year" not in line:
			percounthash[int(line.split("\t")[0])]=int(line.split("\t")[1].strip())
			annotationcount=annotationcount+int(line.split("\t")[1].strip())
	infile.close()
	return annotationcount,percounthash


def groupannotationfiles(years,groupeddirectory,annotationdir):
	outfile=groupeddirectory+"GroupedAnnotations_"+str(min(years))+"_"+str(max(years))+".txt"
	
	for year in years:
		annotationfile=annotationdir+"Annotated_Corpus_"+str(year)+".txt"
		cmd="cat " + annotationfile+" >> "+outfile
		os.system(cmd)

def main():
	peryearcountsfile=sys.argv[1]
	annotationcount,percounthash=gettotalnumberofannotations(peryearcountsfile)
	

	annotationdir=sys.argv[2]
	interval=int(sys.argv[3])
	countperterm=dict()
	
	groupeddirectory="../data/GroupedAnnotations/"
	if os.path.exists(groupeddirectory):
		shutil.rmtree(groupeddirectory)
		os.makedirs(groupeddirectory)
	else:
		os.makedirs(groupeddirectory)

	
	groupannotationcount=0
	numberofbins=0



	orderedpercounthash= sorted(percounthash.items(), key=operator.itemgetter(0))
	groupyears=set()
	for pair in orderedpercounthash:
		year=pair[0]
		count=pair[1]
		if (float(groupannotationcount)/float(annotationcount))*100 <= interval:
			groupyears.add(year)
			groupannotationcount=groupannotationcount+count

			if (float(groupannotationcount)/float(annotationcount))*100 <= interval:
				groupyears.add(year)
			else:
				if 2001 in groupyears:
					groupyears.add(2003)
				groupannotationfiles(groupyears,groupeddirectory,annotationdir)
				groupannotationcount=0
				groupyears=set()
	#groupannotationfiles(groupyears,groupeddirectory,annotationdir)			




			

if __name__ == "__main__":
	import shutil
	import operator
	import sys
	import os
	main()