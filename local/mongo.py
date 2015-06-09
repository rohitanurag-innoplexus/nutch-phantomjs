import pymongo
from pymongo import MongoClient
import csv
import sys
import os
path = sys.argv[1]

if os.path.exists(path):
    print "file exists"
else:
    print "file does not exists"
    sys.exit()
    
    
client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['nutchdb']
collection = db.nutchdb

text = db.webpage.find({"baseUrl":{"$exists":True}})
urlsPresent = [] 
#It reads the url file as provided in the command line and then append in urlPresent lists 
with open(path,"r") as fp:
    reader=csv.reader(fp)
    for row in reader:
        urlsPresent+=row


urls = []  #It checks if the urlis already present,if it is there then it does not append in that file otherwise it appends 
for record in text:
    url = record['baseUrl']
    if url not in urlsPresent:
        urls += [[url]]
#write the new appended urls in the file
with open(path,'a') as f:
    writer  = csv.writer(f)
    writer.writerows(urls)


