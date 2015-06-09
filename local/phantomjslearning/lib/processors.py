from sklearn.feature_extraction import DictVectorizer
import numpy as np
import tokenizers
import analyzers
import collections
import pymongo
from pymongo import MongoClient
import csv
import sys
import os
import itertools
from sklearn.feature_extraction import DictVectorizer
import utils
import re
from sklearn import preprocessing
    
client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['nutchdb']
collection = db.nutchdb
# Connect to the mongo db server and the use nutchdb database
class Processor(object):

    CONTINUOUS_FEATURES = {
        'width': lambda page, datapoint: float(datapoint['bound']['width']),
    }

    def __init__(
        self,
        data,
        tokenizer=tokenizers.EnglishTokenizer,
        analyzer=analyzers.TermFrequencyAnalyzer
    ):
        self.data = data
        self.tokenizer = tokenizer()

        # tokenize data fields in each page and store them
        pages = []
        for page in self.data:
            page['titles'] = self.tokenizer.tokenize(*page['titles'])
            page['descriptions'] = self.tokenizer.tokenize(*page['descriptions'])
            tokens = page['titles'] + page['descriptions']
            for text in page['texts']:
                text['label'] = 0
                text['there'] = 0
                text['tokens'] = self.tokenizer.tokenize(*text['text'])
                text['url']=page['url']
                tokens += text['tokens']
            pages.append(tokens)

        self.analyzer = analyzer(*pages)

        self.pages = []
        self.texts = []

        for page in self.data:
            for text in page['texts']:

                # keep track of corresponding page and text for each datapoint
                self.pages.append(page)
                self.texts.append(text)

    def extract(self):
        """
        Extract features for clustering
        """
     #This method extract the features from the data.Two types of features are being extracted
     #One is of continuos_features and other of discrete_features
        continuous_features = []
        discrete_features = []

        for page, text in zip(self.pages, self.texts):
        
            # continuous features
            continuous_features.append([
                process(page, text)
                for key, process in self.CONTINUOUS_FEATURES.iteritems()
            ])

            # discrete features
            discrete_feature = dict(text['computed'].items())
            discrete_feature['path'] = ' > '.join(text['path'])
            discrete_features.append(discrete_feature)

        # build numpy array
        continuous_features = preprocessing.scale(np.array(continuous_features))

        # vectorize discrete features
        vectorizer = DictVectorizer()
        discrete_features = vectorizer.fit_transform(discrete_features).toarray()

        return np.hstack([continuous_features, discrete_features]).astype(np.float32)

    def prepare(self, labels,path):
       # It helps in preparing Random Forest data
        clusters = collections.defaultdict(lambda: dict(
            label=0,
            score=0.0,
            pages=collections.defaultdict(lambda: dict(
                texts=[],
            )),
        ))

        # iterate over each block
        for page, text, label in zip(self.pages, self.texts, labels):

            # first find out this text block's relevence score
            hints = page['titles'] + page['descriptions']
            score = self.analyzer.get_similarity(text['tokens'], hints) if hints else 0.0
            # It finds the similarity between text tokens and then give a score based on the similarity between text and hints we get from description and titles 
            # find the cluster
            cluster = clusters[int(label)]
           # print cluster
            cluster['score'] += score

            cluster['pages'][page['url']]['texts'].append(text)


            text['label'] = int(label)


        # build features
        continuous_features = []
        discrete_features = []
        labels = []
        texts1 = []
        urls = []
        yesno=[]
        # Create 6 features python lists

        for text in self.texts:
            text_length = len(text['tokens'])
            #finds the text length of the token
            area = text['bound']['height'] * text['bound']['width']
            # Calculates the area of the text block
            text_density = float(text_length) / float(area)

            #appends all the above calculated features to the continuous_feature array
            continuous_feature = [text_length, text_density, float(text_length) / float(len(text['text'])), area]


            #It creates a dict() and then add the corresponding 
            discrete_feature = dict()

            discrete_feature['class'] = ' > '.join([
                '%s%s' % (
                    selector['name'],
                    '.' + '.'.join(selector['classes']) if selector['classes'] else '',
                )
                for selector in text['selector']
            ])
            #appends the tag_path data in discrete features
            discrete_features.append(discrete_feature)
            labels.append(text['label'])
            continuous_features.append(continuous_feature)
            texts1.append(text['tokens'])
            urls.append(text['url'])
            yesno.append(text['there'])
            #appends all the required datasets into arrays .We will be using this to train
        return continuous_features, discrete_features, labels, texts1, urls, yesno

