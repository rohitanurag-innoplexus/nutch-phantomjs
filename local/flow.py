import subprocess
import os
import sys
arr=sys.argv
filename=arr[1]
url=arr[2]
print arr[1]
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-7-openjdk-amd64/jre/"

subprocess.call(["mkdir","./urls/"+filename])
f = open('./urls/'+filename+'/seed.txt','w')
f.write(url) 
f.close()
subprocess.call(["mkdir","./phantomjslearning/data/"+filename])
f = open('./phantomjslearning/data/'+filename+'/urls','w')
f.write(url) 
f.close()
subprocess.call(["python","dropdatabase.py"])
subprocess.call(["bin/nutch","inject","urls/"+filename])
for i in xrange(1,3):
    subprocess.call(["make","generate"])
subprocess.call(["python","mongo.py","./phantomjslearning/data/"+filename+"/urls"])
input("enter")
subprocess.call(["python","./phantomjslearning/extractor/run.py","../data/"+filename])
subprocess.call(["python","./phantomjslearning/ensemblerf/checkclassifier.py","../data/"+filename])
