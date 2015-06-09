#!/usr/bin/env python
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
from sklearn.datasets import load_iris
import os
import ImageChops
import math, operator
import Image
import sys
import csv
from sklearn.externals import joblib
from sklearn.datasets import load_digits
from sklearn.linear_model import SGDClassifier
lib_path = os.path.realpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'lib'))
if lib_path not in sys.path:
    sys.path[0:0] = [lib_path]
from itertools import izip
import utils
import clusterers
import processors
import simplejson as json
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
#It imports all the necessary python packages 

def combine_rfs(rf_a, rf_b):
    rf_a.estimators_ += rf_b.estimators_
    rf_a.n_estimators = len(rf_a.estimators_)
    return rf_a
# combine_rfs combines two randomforests models 
def equal(im1, im2):
    diff = ImageChops.difference(im1, im2)
    h = diff.histogram()
    sq = (value*(idx**2) for idx, value in enumerate(h))
    sum_of_squares = sum(sq)
    rms = math.sqrt(sum_of_squares/float(im1.size[0] * im1.size[1]))
    return rms

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
    #It retrieves all the dataset which gets after getting clustered and store them in various lists
    lab=[]
    urlss=[]
    for k in texts1:
        lab.append(k.encode('ascii','ignore'))
    
    #It decodes the unicode into text 
    
    vectorizer = DictVectorizer()
    discrete_features = vectorizer.fit_transform(discrete_features).toarray()
    #This is the feature extraction part which I have mentioned in my doc
    discrete_features.resize(len(discrete_features), 10000) 
    #resize the discreet_features array to a uniform size so that in further using it model and test data set have same length features array
    continuous_features = np.array(continuous_features)
    labels = np.array(labels).astype(np.float32)

    features = np.hstack([continuous_features, discrete_features]).astype(np.float32)

    features = preprocessing.scale(features)
    #This is the normalization process where features are preprocessed to a scale
    im1=Image.open("/home/test/nutch/runtime/local/phantomjslearning/data/dazedandconfused/000.png")
    im2=Image.open("/home/test/nutch/runtime/local/phantomjslearning/data/fruitsofotherhands/000.png")
    im3=Image.open("/home/test/nutch/runtime/local/phantomjslearning/data/rohitanurag/000.png")
    im4=Image.open("/home/test/nutch/runtime/local/phantomjslearning/data/thegirlwhoreadtoomuch/000.png")
    im5=Image.open("/home/test/nutch/runtime/local/phantomjslearning/data/timcotson/000.png")

    imtest=Image.open(path+"/000.png")


    result1=equal(imtest,im1)
    result2=equal(imtest,im2)
    result3=equal(imtest,im3)
    result4=equal(imtest,im4)
    result5=equal(imtest,im5)
    choose=0
    testresult=result1

    if result1 <= testresult:
        choose=1
        testresult=result1

    if result2 <= testresult:
        choose=2
        testresult=result2

    if result3 <= testresult:
        choose=3
        testresult=result3

    if result4 <= testresult:
        choose=4
        testresult=result4

    if result5 <= testresult:
        choose=5
        testresult=result5


    if choose == 1:
    	usemodel="/home/test/nutch/runtime/local/phantomjslearning/classlibraries/rfdazedandconfused.joblib.pkl"
    if choose == 2:
    	usemodel="/home/test/nutch/runtime/local/phantomjslearning/classlibraries/rffruitsofother.joblib.pkl"
    if choose == 3:
    	usemodel="/home/test/nutch/runtime/local/phantomjslearning/classlibraries/rfrohitanurag.joblib.pkl"
    if choose == 4:
    	usemodel="/home/test/nutch/runtime/local/phantomjslearning/classlibraries/rfthegirlwhoused.joblib.pkl"
    if choose == 5:
    	usemodel="/home/test/nutch/runtime/local/phantomjslearning/classlibraries/rftimscoton.joblib.pkl"
#Here we get the predicted model which we use to predict classes like title , date,paragraphs of blogs

    usemodel = "/home/test/nutch/runtime/local/phantomjslearning/classlibraries/ivfhaveababy.joblib.pkl"
    rf = joblib.load(usemodel)
    #loads the model and then use it for prediction
    predicted = rf.predict(features)
    print usemodel
    for i in xrange(1,len(predicted)):
        print lab[i]
        print  "*********"
        print predicted[i]
        print "**********"
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
