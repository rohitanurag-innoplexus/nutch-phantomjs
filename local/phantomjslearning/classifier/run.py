#!/usr/bin/env python

import os
import sys
import csv
from sklearn.externals import joblib
from sklearn.datasets import load_digits
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import RandomForestClassifier
lib_path = os.path.realpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'lib'))
if lib_path not in sys.path:
    sys.path[0:0] = [lib_path]
from itertools import izip
import utils
import clusterers
import processors
import simplejson as json
import ImageChops
import math, operator
import Image
import os
import csv
import argparse
import analyzers
import tokenizers
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn import svm, preprocessing, cross_validation
from sklearn.metrics import precision_recall_curve, auc, classification_report, precision_recall_fscore_support
import collections
import random
def main(args):

    path = utils.get_data_path(args.site[0])
    urls = utils.load_urls(path)
    #print path
    count=0
    # load data
    data = [utils.load_data(path, id) for id, url in enumerate(urls)]
    random.shuffle(data)
    for page in data:
       # print count
        #count+=1
        random.shuffle(page['texts'])

    # process data
    processor = processors.Processor(data, tokenizer=tokenizers.GenericTokenizer, analyzer=analyzers.LongestAnalyzer)
    features = processor.extract()
    #print len(features)
    # clustering
    clusterer = clusterers.DBSCAN()
    labels = clusterer.cluster(features).labels_

    # prepare features
    continuous_features, discrete_features, cluster_labels , texts1, urls , classes = processor.prepare(labels,path)

    res=[texts1,labels]
   # print len(texts1)
    lab=[]
    urlss=[]
    for k in texts1:
        lab.append(k.encode('ascii','ignore'))
    
    for l in urls:
        urlss.append(l.encode('ascii','ignore'))
    # decode the uncodes into string variable
    with open("rohit.csv","w") as fp:
	    writer = csv.writer(fp)
	    for row in zip(urls, lab, labels,classes):
		    writer.writerow(row)


    input("enter data ")
    
    classes=[]
    with open("rohit.csv","r") as fp:
	    reader = csv.reader(fp)
	    for row in reader:
		    classes += [row[3]]
    # Label the dataset and give them classes to which they belong.Classes are in 4th column
    for i in xrange(1,len(classes)):
        if classes[i] == 0:
            classes[i]= cluster_labels[i]
    vectorizer = DictVectorizer()
    discrete_features = vectorizer.fit_transform(discrete_features).toarray()
    discrete_features.resize(len(discrete_features), 10000) 
    continuous_features = np.array(continuous_features)
    labels = np.array(labels).astype(np.float32)
    #print len(discrete_features[2])
    features = np.hstack([continuous_features, discrete_features]).astype(np.float32)
    #print features
    # scale features
    features = preprocessing.scale(features)
    #preprocess the features
    rf=RandomForestClassifier(n_estimators=300)
    rf.fit(features,classes)
    #make a randomforest model and fit into them features and classes
    filename = '/home/test/nutch/runtime/local/phantomjslearning/classlibraries/ivfhaveababy.joblib.pkl'
    _ = joblib.dump(rf, filename, compress=9)
    rf = joblib.load(filename)
    #dump the model file into the particular directory
    precisions = []
    recalls = []
    f1scores = []
    supports = []

    return


    





def parse_args():
    """
    Parse commandline arguments
    """
    parser = argparse.ArgumentParser(description='Run the whole pipeline on site pages.')
    parser.add_argument('site', metavar='site', type=str, nargs=1, help='site id, for example: theverge, npr, nytimes')
    return parser.parse_args()

if __name__ == '__main__':
    main(parse_args())
