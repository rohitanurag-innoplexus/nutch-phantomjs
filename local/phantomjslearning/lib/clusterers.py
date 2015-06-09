from sklearn import cluster
from sklearn.preprocessing import StandardScaler
import numpy as np
#calls DBSCAN algorithm for clustering the sample points and then labels it
class DBSCAN(object):

    def cluster(self, data):
        data = StandardScaler().fit_transform(data)
        db = cluster.DBSCAN(min_samples=1).fit(data)
        return db
