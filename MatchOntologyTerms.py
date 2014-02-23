
def stemOntologyIDs():
	global taoid2name
	global ontologystems
	global taoids_stem
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


 
def word_in (word, phrase):
    return word in phrase.split()

def getOriginalTextinLine(temp_dict, line):
	data=line.split(" ")
	origline=""
	for stem in data:
		origline=origline+" "+temp_dict[stem]
	return(origline.strip())

def cleanfile():
	f=open('./InputFiles/BHLCorpus.txt','r')
	w=open('./InputFiles/BHLCorpus_Cleaned.txt','w')
	populateStopWord()
	for line in f:
		line=line.replace(":","")
		line=line.replace("\"","")
		line=line.replace("_","")
		line=line.replace(".","")
		line=line.replace(")","")
		line=line.replace("(","")
		cleanline=cleanOCR(line)
		stop_removed=removeStopWords(cleanline)
		w.write(cleanline+"\n")

def populateStopWord():
	global stopwords
	f=open('./InputFiles/stopwords.txt','r')
	for stopword in f:
		stopwords.add(stopword)	


def removeStopWords(line):
	words=line.split(" ")
	stopremovedline=""
	for word in words:
		if word not in stopwords:
			stopremovedline=stopremovedline+" "+word
	return stopremovedline

def get_new_line(line, flag):
    if flag == 0:
        return ""
    
    return line

def cleanOCR(line):
    line = line.strip()
    if line == "":
        print "case 0"
        return ""
    special_characters = "\*<>()\[\]{}\-_=\+^\'/"
    
    
    new_line = ""
    pattern_titleID = re.compile("^\s*TitleID:\s*\d+")
    if pattern_titleID.match(line):
        print "case 1"
        new_line = get_new_line(line, 0)
        return new_line
    
    pattern_itemID = re.compile("^\s*ItemID:\s*\d+")
    if pattern_itemID.match(line):
        print "case 2"
        new_line = get_new_line(line, 0)
        return new_line
    
    pattern_OCR_not_available = re.compile("^\s*OCR text unavailable for this page.")
    if pattern_OCR_not_available.search(line):
        print "case 3"
        new_line = get_new_line(line, 0)
        return new_line
    
    pattern_single_integer = re.compile("^\.*\d+(\s*)$")
    if pattern_single_integer.match(line):
        p = pattern_single_integer.match(line)

        
        new_line = get_new_line(line, 0)
        return new_line
    
    pattern_single_word = re.compile("^\.*[a-zA-Z0-9]+(\s*)$")
    #if len(line) > 2:
        #print line[-3]
    if pattern_single_word.match(line):
        print "case 5"
        new_line = get_new_line(line, 0)
        return new_line
    
    # eg. "3*"
    pattern_digits_and_special_characters = re.compile("^\.*[a-zA-Z0-9"+special_characters+"]+(\s*)$")
    if pattern_digits_and_special_characters.match(line):
        print "case 6"
        new_line = get_new_line(line, 0)
        return new_line
    
    # eg. EMIL BRASS
    max_len = 5
    pattern_words_and_whitespace = re.compile("^[a-zA-Z0-9\s"+special_characters+"]+$")
    pattern_words = re.compile("\w+")
    if pattern_words_and_whitespace.match(line) and pattern_words.search(line):
        words = re.split("\s+", line)
        if len(words) < max_len:
            print "case 7"
            new_line = get_new_line(line, 0)
            return new_line
        
    # If the radio of non-alphabetic characters in a line exceeds a threshold, then remove the line
    threshold = 0.5
    shorted_line = re.sub("[^a-zA-Z\s]", "", line)
    shorted_line = shorted_line.strip()

    if float(len(shorted_line)) / len(line) < threshold:
        print "case 8"

        new_line = get_new_line(line, 0)
        return new_line 
    

    return line



def getContextVector(annotatedline,ontterm,origterm):
	windowsize=5
	



def main():
	cleanfile()
	inp=open("./InputFiles/BHLCorpus_Cleaned.txt",'r')
	out=open("./InputFiles/BHLCorpus_Annotated.txt",'w')
	stemOntologyIDs()
	tempstem2text=dict()
	for line in inp:
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
			matchedontologyterms.add(matched_dict[origlineterm])
			replacedline=line.replace(origlineterm,annotation)
			matched=1
			out.write(replacedline+"\n")
			getContextVector(replacedline,matched_dict[origlineterm],origlineterm)
		if matched==0:
			out.write(line+"\n")		





				




if __name__ == "__main__":
	from stemming.porter2 import stem
	import re
	stopwords=set()
	taoids_stem=dict()
	ontologystems=set()
	stem2id=dict()
	taoid2name={}
	matchedontologyterms=set()
	main()