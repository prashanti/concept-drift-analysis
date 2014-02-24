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
	inp=open('./InputFiles/item_parsed.xls','r')
	for line in inp:
		if "TitleID" not in line:
			data=line.split("\t")
			itemid=data[0].strip()
			titleid=data[1].strip()
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
			if "Vertebrate" in subject:
				vertebratetitleids.add(titleid.strip())

def getVertebratePartIDs():
	global vertebratepartids
	inp=open('./InputFiles/part_parsed.xls','r')
	#PartID	ItemID	ContributorName	SequenceOrder	SegmentType	Title	ContainerTitle	PublicationDetails	Volume	Series	Issue	Date	PageRange	StartPageID	LanguageName	SegmentUrl	ExternalUrl	DownloadUrl	
	for line in inp:
		if "PartID" not in line:
			data=line.split("\t")
			partid=data[0].strip()
			title=data[2].strip()
			if "Vertebrate" in title:
				vertebratepartids.add(partid)


def getPageIDsforPartId():
	global vertebratepartids
	global partid2pageids_dict
	for partid in vertebratepartids:
		url="http://www.biodiversitylibrary.org/api2/httpquery.ashx?op=GetPartMetadata&partid="+partid+"&pages=t&ocr=t&apikey=8c118b05-3e6e-4ef2-92c5-78610a868a14&format=json"
		content = urllib2.urlopen(url).read()
		raw = nltk.clean_html(content)
		decoded_data = json.loads(raw)
		# keep a set of pageIDs for each partid
		for x in decoded_data['Result']['Pages']:
			if partid not in partid2pageids_dict:
				partid2pageids_dict[partid]=set()
			partid2pageids_dict[partid].add(x['PageID'])
			
	


def main():
	# -*- coding: utf-8 -*-
	subjectlimit=0
	partlimit=10
	global titleids
	global itemids_dict
	getTitleIDs()
	getItemIDs()
	getVertebrateTitleIDs()
	getVertebratePartIDs()
	getPageIDsforPartId()
	
	f=open('./InputFiles/BHLCorpus.txt','w')
	for titleid in vertebratetitleids:
			for item in itemids_dict[titleid]:
				if subjectlimit >0:
					f.write("TitleID:  "+str(titleid)+"\n")
					subjectlimit=subjectlimit-1
					f.write("ItemID:  "+str(item)+"\n")
					url="http://www.biodiversitylibrary.org/api2/httpquery.ashx?op=GetItemMetadata&itemid="+item.strip()+"&pages=t&ocr=t&parts=f&apikey=8c118b05-3e6e-4ef2-92c5-78610a868a14&format=json"
					content = urllib2.urlopen(url).read()
					raw = nltk.clean_html(content)
					decoded_data = json.loads(raw)
					for page in decoded_data['Result']['Pages']:
						f.write(page['OcrText'].strip().replace("."," . ").encode('utf-8')+"\n")
	
	f.write("Getting Parts which match Vertebrate in the title")
					
	for partid in partid2pageids_dict:
		if partlimit>0:
			partlimit=partlimit-1
			f.write("Part ID: "+str(partid)+"\n")
			for pageid in partid2pageids_dict[partid]:
				url ="http://www.biodiversitylibrary.org/api2/httpquery.ashx?op=GetPageOcrText&pageid="+str(pageid)+"&apikey=8c118b05-3e6e-4ef2-92c5-78610a868a14&format=json"
				content = urllib2.urlopen(url).read()
				raw = nltk.clean_html(content)
				decoded_data = json.loads(raw)
				f.write(decoded_data['Result'].replace("."," . ").encode('utf-8'))


if __name__ == "__main__":
	import json
	import urllib2
	from BeautifulSoup import BeautifulSoup
	import nltk
	titleids=set()
	itemids_dict=dict()
	vertebratetitleids=set()
	vertebratepartids=set()
	partid2pageids_dict=dict()
	main()





