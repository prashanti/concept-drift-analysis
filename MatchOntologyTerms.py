
def stemOntologyIDs():
	global taoid2name
	inp=open("./InputFiles/TAO_Names.xls",'r')
	for line in inp:
		data=line.split("\t")
		name=data[1].strip()
		ontid=data[0].strip()
		if name not in taoid2name:
			taoid2name[name]=ontid
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


# 
def word_in (word, phrase):
    return word in phrase.split()

def getOriginalTextinLine(temp_dict, line):
	data=line.split(" ")
	origline=""
	for stem in data:
		origline=origline+" "+temp_dict[stem]
	return(origline.strip())

	
def clean(line):
	line=line.replace(":","")
	line=line.replace("\"","")
	line=line.replace("_","")
	line=line.replace(".","")
	line=line.replace(")","")
	line=line.replace("(","")
	return line

def main():
	inp=open("./InputFiles/BHLCorpus.txt",'r')
	out=open("./InputFiles/BHLCorpus_Annotated.txt",'w')
	stemOntologyIDs()
	tempstem2text=dict()
	for line in inp:
		clean_line=clean(line)
		tempstem2text=getStemmedString(line)
		stemmedline=tempstem2text['StemmedString']
		matched_dict={}
		matched=0
		for stemmedterm in ontologystems:
			if word_in(stemmedterm, stemmedline):
				origline=getOriginalTextinLine(tempstem2text,stemmedline)
				origontterm=stem2id[stemmedterm]
				origlineterm=getOriginalTextinLine(tempstem2text,stemmedterm)
				for x in origontterm:
					ontid=taoid2name[x]
					if origlineterm in matched_dict:
						matched_dict[origlineterm].append(ontid)
					
					else:
						matched_dict[origlineterm]=ontid
						
		for origlineterm in matched_dict:
			annotation=" <term> "+matched_dict[origlineterm]+" \""+origlineterm + "\" "+ "</term>"
			replacedline=line.replace(origlineterm,annotation)
			matched=1
			out.write(replacedline+"\n")
		if matched==0:
			out.write(line+"\n")		





				




if __name__ == "__main__":
	from stemming.porter2 import stem
	taoids_stem=dict()
	ontologystems=set()
	stem2id=dict()
	taoid2name={}
	main()