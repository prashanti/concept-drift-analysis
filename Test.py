def getTitleIDs():
	global titleids
	inp=open('title_parsed.xls','r')
	for line in inp:
		if "TitleID" not in line:
			data=line.split("\t")
			titleid=data[0].strip()
			language=data[1].strip()
			titleids.add(titleid.strip())


def getItemIDs():
	global titleids
	global itemids_dict
	inp=open('item_parsed.xls','r')
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
	inp=open('subject.txt','r')
	for line in inp:
		if "TitleID" not in line:
			data=line.split("\t")
			#TitleID	Subject	CreationDate
			titleid=data[0]
			subject=data[1]
			if "Vertebrate" in subject:
				print "yes"
				vertebratetitleids.add(titleid.strip())

def getVertebratePartIDs():
	global vertebratepartids
	inp=open('part_parsed.xls','r')
	#PartID	ItemID	ContributorName	SequenceOrder	SegmentType	Title	ContainerTitle	PublicationDetails	Volume	Series	Issue	Date	PageRange	StartPageID	LanguageName	SegmentUrl	ExternalUrl	DownloadUrl	
	for line in inp:
		if "PartID" not in line:
			data=line.split("\t")
			partid=data[0].strip()
			title=data[2].strip()
			if "Vertebrate" in title:
				vertebratepartids.add(partid)


def main():
	getItemIDs()
	getTitleIDs()
	getVertebratePartIDs()
	getVertebrateTitleIDs()
	
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