import pymongo
from pymongo import MongoClient
import csv
import sys
import os

client = MongoClient()
client = MongoClient('localhost', 27017)
#It drops the nutchdb database which have been created using nutch crawler
client.drop_database('nutchdb')

