def getTitleIDs():
	global titleids
	inp=open('./InputFiles/title_parsed.xls','r')
	for line in inp:
		if "TitleID" not in line:
			data=line.split("\t")
			titleid=data[0].strip()
			language=data[1].strip()
			titleids.add(titleid.strip())


def getItemIDs():
	global titleids
	global itemids_dict
	global itemid2year
	inp=open('./InputFiles/item_parsed.txt','r')
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


def getVertebrateTitleIDs():
	global vertebratetitleids
	inp=open('./InputFiles/subject.txt','r')
	for line in inp:
		if "TitleID" not in line:
			data=line.split("\t")
			#TitleID	Subject	CreationDate
			titleid=data[0]
			subject=data[1]
			if "Vertebrate" in subject or "vertebrate" in subject:
				vertebratetitleids.add(titleid.strip())

def getVertebratePartIDs():
	global vertebratepartids
	global itemid2year
	global partid2year
	inp=open('./InputFiles/part_parsed.xls','r')
	#PartID	ItemID	ContributorName	SequenceOrder	SegmentType	Title	ContainerTitle	PublicationDetails	Volume	Series	Issue	Date	PageRange	StartPageID	LanguageName	SegmentUrl	ExternalUrl	DownloadUrl	
	
	for line in inp:
		if "PartID" not in line:
			data=line.split("\t")
			partid=data[0].strip()
			title=data[2].strip()
			year=data[3].strip()
			if "/" in year:
				year="19"+year.split("/")[2]
			if "Vertebrate" in title or "vertebrate" in title:
				vertebratepartids.add(partid)
				partid2year[partid]=year


def getPageIDsforPartId():
	global vertebratepartids
	global vertebratepartid2pageids_dict
	for partid in vertebratepartids:
		url="http://www.biodiversitylibrary.org/api2/httpquery.ashx?op=GetPartMetadata&partid="+partid+"&pages=t&ocr=t&apikey=8c118b05-3e6e-4ef2-92c5-78610a868a14&format=json"
		content = urllib2.urlopen(url).read()
		raw = nltk.clean_html(content)
		decoded_data = json.loads(raw)
		# keep a set of pageIDs for each partid
		for x in decoded_data['Result']['Pages']:
			if partid not in vertebratepartid2pageids_dict:
				vertebratepartid2pageids_dict[partid]=set()
			vertebratepartid2pageids_dict[partid].add(x['PageID'])
			
	


			
def main():
	# -*- coding: utf-8 -*-
	subjectlimit=0
	partlimit=100
	global titleids
	global itemids_dict
	getTitleIDs()
	getItemIDs()
	getVertebrateTitleIDs()
	getVertebratePartIDs()
	getPageIDsforPartId()
	#print "Number of english vertebratetitleids",len(set.intersection(vertebratetitleids,titleids))
	for titleid in vertebratetitleids:
			if titleid in titleids:
				for item in itemids_dict[titleid]:
					if itemid2year[item].strip() !="":
						print "item,year",item,itemid2year[item]
						if subjectlimit >0:
							inputfile="./InputFiles/BHLCorpus_"+str(itemid2year[item])
							print "inputfile",inputfile
							outfile=open(inputfile,'a')
							outfile.write("TitleID:  "+str(titleid)+"\n")
							outfile.write("ItemID:  "+str(item)+"\n")
							#subjectlimit=subjectlimit-1
							
							url="http://www.biodiversitylibrary.org/api2/httpquery.ashx?op=GetItemMetadata&itemid="+item.strip()+"&pages=t&ocr=t&parts=f&apikey=8c118b05-3e6e-4ef2-92c5-78610a868a14&format=json"
							content = urllib2.urlopen(url).read()
							raw = nltk.clean_html(content)
							decoded_data = json.loads(raw)
							for page in decoded_data['Result']['Pages']:
								outfile.write(page['OcrText'].strip().replace("."," . ").encode('utf-8')+"\n")
							outfile.close()
	
# need year for partID.					
	print len(vertebratepartid2pageids_dict)
	for partid in vertebratepartid2pageids_dict:
		if partlimit>0:
			#partlimit=partlimit-1
			inputfile="./InputFiles/BHLCorpus_"+str(partid2year[partid])
			print "inputfile",inputfile
			outfile=open(inputfile,'a')
			outfile.write("PartID:  "+str(partid)+"\n")
			for pageid in vertebratepartid2pageids_dict[partid]:
				
				url ="http://www.biodiversitylibrary.org/api2/httpquery.ashx?op=GetPageOcrText&pageid="+str(pageid)+"&apikey=8c118b05-3e6e-4ef2-92c5-78610a868a14&format=json"
				content = urllib2.urlopen(url).read()
				raw = nltk.clean_html(content)
				decoded_data = json.loads(raw)
				outfile.write(decoded_data['Result'].replace("."," . ").encode('utf-8'))
			outfile.close()


if __name__ == "__main__":
	import json
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
	main()





