
def main():
	infile=open("../data/UBERONDistributionsExact/ComprehensiveDistribution.txt")
	sufficientdir="../data/SufficientTerms/"
	if not os.path.exists(sufficientdir):
		os.makedirs(sufficientdir)
	outfile=open(sufficientdir+ "SufficientTerms_BinSize.txt",'w')
	outfile.write("Number of Time Periods\tTerms with Sufficient Data\tPercent Terms with Sufficient Data\n")
	binsizes=[5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
	termcount=dict()
	for line in infile:
		if "Total" not in line:
			term=line.split("\t")[0].strip()
			count=int(line.split("\t")[1].strip())
			termcount[term]=count
	infile.close()
	for binsize in binsizes:
		sufffile=open(sufficientdir+str(binsize)+"_Bins_Terms.txt",'w')
		expectedcount=binsize*5
		sufficientdataterms = {term for (term,count) in termcount.items() if (count > expectedcount)}
		for term in sufficientdataterms:
			sufffile.write(term.strip()+"\n")
		sufffile.close()	
		percent=round((float(len(sufficientdataterms))/float(len(termcount)))*100,2)
		outfile.write(str(binsize)+"\t"+str(len(sufficientdataterms))+"\t"+str(percent)+"\n")
	outfile.close()


if __name__ == "__main__":
	import sys
	import os
	main()

