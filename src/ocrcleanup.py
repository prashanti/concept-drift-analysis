# -*- coding: utf-8 -*-
import re
import sys
import os
from stemming.porter2 import stem

def createstoplist():
	stoplist=set()
	for line in open('../data/input/stopwords.txt'):
		line=line.strip()
		stoplist.add(line.lower())
	stoplist=[stem(word) for word in stoplist]
	return(stoplist)



stoplist=createstoplist()
pathdir=sys.argv[1]
for filename in os.listdir(pathdir):
	if ".txt" in filename:
		infile=open(pathdir+filename,'r')
		print filename
		outfile=open("../data/CleanedCorpus/Cleaned_"+filename,'w')
		chars = [',', '!', '.', ';', '?','^','1','2','3','4','5','6','7','8','9','"',':','(',')','@','#','$','%','&','*','-','>','<','}','{',',','\]','\[','\'','■']
		for line in infile:
			if "TitleID" not in line and "ItemID" not in line and "PartID" not in line and "titleid" not in line and "itemid" not in line and "partid" not in line:
				line=re.sub('[%s]' % ''.join(chars), '', line)
				line=line.replace("OCR text unavailable for this page","")
				line=line.replace("I","i")
				line=line.strip()
				line = re.sub('[^a-zA-Z0-9\n\.]', ' ', line)
				if line !="":
					newline=line.lower().strip()
					for word in newline.split():
					
						word=word.strip()
						if stem(word) in stoplist:
							
							newline=re.sub(r'\b' + re.escape(word) + r'\b', '', newline)
					newline=' '.join(newline.split())
					outfile.write(newline+" ")
			else:
				outfile.write("\n"+line+"\n")
			
		infile.close()
		outfile.close()