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

def main():
	global titleids
	global itemids_dict
	getTitleIDs()
	getItemIDs()
	getVertebrateTitleIDs()
	f=open('BHLCorpus.txt','w')

	for titleid in vertebratetitleids:
		f.write("TitleID:  "+str(titleid)+"\n")
		for item in itemids_dict[titleid]:
			f.write("ItemID:  "+str(item)+"\n")
			url="http://www.biodiversitylibrary.org/api2/httpquery.ashx?op=GetItemMetadata&itemid="+item.strip()+"&pages=t&ocr=t&parts=f&apikey=8c118b05-3e6e-4ef2-92c5-78610a868a14&format=json"
			content = urllib2.urlopen(url).read()
			raw = nltk.clean_html(content)
			decoded_data = json.loads(raw)
			for page in decoded_data['Result']['Pages']:
				f.write(page['OcrText'].encode('utf-8').strip()+"\n")
		

	

if __name__ == "__main__":
	import json
	import urllib2
	from BeautifulSoup import BeautifulSoup
	import nltk
	titleids=set()
	itemids_dict=dict()
	vertebratetitleids=set()
	main()





