# -*- coding: utf-8 -*-
def getTitleIDs():
	global titleids
	inp=open('./NewInputs/title_parsed.txt','r')
	for line in inp:
		if "TitleID" not in line:
			data=line.split("\t")
			titleid=data[0].strip()
			titleids.add(titleid.strip())
	inp.close()

def populateyear():
	global titleid2year
	inp=open('./NewInputs/title_parsed.txt','r')
	for line in inp:
		#TitleID	FullTitle	StartYear	LanguageCode
		data=line.split("\t")
		titleid=data[0].strip()
		year=data[2].strip()
		titleid2year[titleid]=year
	inp.close()

def getItemIDs():
	global titleids
	global itemids_dict
	global itemid2year
	inp=open('./NewInputs/item_parsed.txt','r')
	for line in inp:
		if "TitleID" not in line:
			data=line.split("\t")
			itemid=data[0].strip()
			titleid=data[1].strip()
			year=data[2].strip()
			if itemid not in itemid2year:
				itemid2year[itemid]=year.split("-")[0]
			if titleid not in itemids_dict:
				itemids_dict[titleid]=set()
			itemids_dict[titleid].add(itemid)
	inp.close()


def getVertebrateTitleIDs():
	global vertebratetitleids
	inp=open('./NewInputs/subject.txt','r')
	for line in inp:
		if "TitleID" not in line:
			data=line.split("\t")
			#TitleID	Subject	CreationDate
			titleid=data[0].strip()
			subject=data[1].strip()
			subject=subject.replace("invertebrate","")
			subject=subject.replace("Invertebrate","")
			if ("Vertebrate" in subject or "vertebrate" in subject):
				vertebratetitleids.add(titleid.strip())
	inp.close()
	inp=open('./NewInputs/title_parsed.txt')
	for line in inp:
		if "TitleID" not in line:
			data=line.split("\t")
			#TitleID	FullTitle	StartYear	LanguageCode
			titleid=data[0].strip()
			title=data[1].strip()
			title=title.replace("invertebrate","")
			title=title.replace("Invertebrate","")
			if ("Vertebrate" in title or "vertebrate" in title):
				vertebratetitleids.add(titleid.strip())

	inp.close()

def getVertebratePartIDs():
	global vertebratepartids
	global itemid2year
	global partid2year
	inp=open('./NewInputs/part_parsed.txt','r')	
	for line in inp:
		if "PartID" not in line:
			data=line.split("\t")
			partid=data[0].strip()
			title=data[2].strip()
			title=title.replace("invertebrate","")
			title=title.replace("Invertebrate","")
			year=data[3].strip()
			if "/" in year:
				year="19"+year.split("/")[2]
			if "Vertebrate" in title or "vertebrate" in title:
				
				vertebratepartids.add(partid)
				partid2year[partid]=year
	inp.close()


def getPageIDsforPartId():
	global vertebratepartids
	global vertebratepartid2pageids_dict
	for partid in vertebratepartids:
		url="http://www.biodiversitylibrary.org/api2/httpquery.ashx?op=GetPartMetadata&partid="+partid+"&pages=t&ocr=t&apikey=8c118b05-3e6e-4ef2-92c5-78610a868a14&format=json"
		content = urllib2.urlopen(url).read()
		raw = nltk.clean_html(content)
		decoded_data = simplejson.loads(raw)
		# keep a set of pageIDs for each partid
		for x in decoded_data['Result']['Pages']:
			if partid not in vertebratepartid2pageids_dict:
				vertebratepartid2pageids_dict[partid]=set()
			vertebratepartid2pageids_dict[partid].add(x['PageID'])
			
	


			
def main():
	
	global titleids
	global titleid2year
	global itemids_dict
	getTitleIDs()
	getItemIDs()
	getVertebrateTitleIDs()
	getVertebratePartIDs()
	getPageIDsforPartId()
	populateyear()
	print len(vertebratetitleids)
	print vertebratetitleids-titleids
	print "Number of english vertebratetitleids",len(set.intersection(vertebratetitleids,titleids))
	for titleid in vertebratetitleids:
			if titleid in titleids:
				for item in itemids_dict[titleid]:
					year=itemid2year[item].strip()
					if year == "":
						year=titleid2year[titleid]
					if year !="":
						inputfile="./NewInputs/BHLCorpus_"+year+".txt"
						print "inputfile",inputfile
						outfile=open(inputfile,'a')
						outfile.write("TitleID:  "+str(titleid)+"\n")
						outfile.write("ItemID:  "+str(item)+"\n")
						#subjectlimit=subjectlimit-1
						
						url="http://www.biodiversitylibrary.org/api2/httpquery.ashx?op=GetItemMetadata&itemid="+item.strip()+"&pages=t&ocr=t&parts=f&apikey=8c118b05-3e6e-4ef2-92c5-78610a868a14&format=json"
						content = urllib2.urlopen(url).read()
						raw = nltk.clean_html(content)
						if raw != "":
							decoded_data = simplejson.loads(raw)
							for page in decoded_data['Result']['Pages']:
								outfile.write(page['OcrText'].strip().replace("."," . ").encode('utf-8')+"\n")
						outfile.close()
	
# need year for partID.					
	print "Number of Vertebrate PartIDs ",len(vertebratepartid2pageids_dict)
	for partid in vertebratepartid2pageids_dict:
		inputfile="./NewInputs/BHLCorpus_"+str(partid2year[partid])+".txt"
		print "file",inputfile
		outfile=open(inputfile,'a')
		outfile.write("PartID:  "+str(partid)+"\n")
		for pageid in vertebratepartid2pageids_dict[partid]:
			
			url ="http://www.biodiversitylibrary.org/api2/httpquery.ashx?op=GetPageOcrText&pageid="+str(pageid)+"&apikey=8c118b05-3e6e-4ef2-92c5-78610a868a14&format=json"
			print "2Downloading"
			content = urllib2.urlopen(url).read()
			print "Done"
			raw = nltk.clean_html(content)
			decoded_data = simplejson.loads(raw)
			outfile.write(decoded_data['Result'].replace("."," . ").encode('utf-8'))
		outfile.close()


if __name__ == "__main__":
	import simplejson
	import urllib2
	from BeautifulSoup import BeautifulSoup
	import nltk
	titleids=set()
	itemids_dict=dict()
	vertebratetitleids=set()
	vertebratepartids=set()
	vertebratepartid2pageids_dict=dict()
	itemid2year=dict()
	partid2year=dict()
	titleid2year=dict()
	main()





