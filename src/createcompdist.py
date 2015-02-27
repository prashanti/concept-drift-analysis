
def main():
	pathdir=sys.argv[1]
	comprehensivetermcount=dict()
	commontermcount=dict()
	totalfilecount=0
	peryearcount=dict()
	
	#commonfile=open(pathdir+"Commonterms.txt",'w')
	for filename in os.listdir(pathdir):
		if "Corpus" in filename:
		
			year=filename.split("Corpus_")[1].split(".txt")[0]
			
			filename=pathdir+filename
			yearcount=0
			totalfilecount+=1
			infile=open(filename,'r')
			for line in infile:
				data=line.split("\t")
				term=data[0].strip()
				if term in commontermcount:
					commontermcount[term]=commontermcount[term]+1
				else:
					commontermcount[term]=1
				count=int(data[1].strip())
				yearcount=yearcount+count
				if term in comprehensivetermcount:
					comprehensivetermcount[term]=comprehensivetermcount[term]+count
				else:
					comprehensivetermcount[term]=count
			infile.close()
			peryearcount[year]=yearcount
	

	compdistfile=open(pathdir+"ComprehensiveDistribution.txt",'w')		
	totalannotations=0

	for term in comprehensivetermcount:
		compdistfile.write(term+"\t"+str(comprehensivetermcount[term])+"\n")
		totalannotations=totalannotations+comprehensivetermcount[term]
	compdistfile.write("Total Annotations\t"+str(totalannotations))

	
	
	#for term in commontermcount:
	#	if commontermcount[term]==totalfilecount:
	#		commonfile.write(term+"\t"+str(commontermcount[term])+"\n")	
	

	peryear=open(pathdir+"PerYearCounts.txt",'w')
	peryear.write("Year\tNumber of Annotations\n")
	for year in sorted(peryearcount, key=lambda key: key):
		peryear.write(str(year)+"\t"+str(peryearcount[year])+"\n")
	
	compdistfile.close()
	#commonfile.close()
	peryear.close()


if __name__ == "__main__":
	import sys
	import os
	main()