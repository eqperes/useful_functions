from scipy import sparse
import numpy as np
from sklearn.cluster import KMeans

#this code is an absolut mess. Please don't use it, otherwise you will blame me for it. And I don't want to be blamed.
class CoClustering(object):

    def __init__(self, n_clusters, n_components=None):
        if n_components == None:
            self.n_components = 2 + np.log2(n_clusters)
        self.n_clusters = n_clusters

    def fit_transform_adjacency(self, adjacency_list, n_itemsA, n_itemsB):
        
        # Generate the dictionary of the items, avoiding 
        #   the items that have no degree
        itemsA = []
        itemsB = []
        itemsA_dict = {}
        itemsB_dict = {}
        for edge in adjacency_list:
            itemsA.append(itemsA_dict.setdefault(edge[0], len(itemsA_dict)))
            itemsB.append(itemsB_dict.setdefault(edge[1], len(itemsB_dict)))
        itemsA_degrees = np.bincount(itemsA)
        itemsB_degrees = np.bincount(itemsB)

        # Generate the normalized data for the SVD
        data = []
        for i in range(0, len(itemsA)):
            data.append(1.0/(np.sqrt(itemsA_degrees[itemsA[i]])*np.sqrt(itemsB_degrees[itemsB[i]])))
        sparse_matrix = csc_matrix((data,(itemsA, itemsB)))

        # Execute the SVD and re-normalize the data
        Uk, __, Vk = sparse.linalg.svds(sparse_matrix, k=int(self.n_components))
        self.itemsA_SVD_ = Uk
        self.itemsB_SVD_ = Vk.T
        dA = sparse.diags([np.power(itemsA_degrees, -0.5)], [0], format="csc")
        dB = sparse.diags([np.power(itemsB_degrees, -0.5)], [0], format="csc")
        all_data = np.vstack([dA.dot(self.itemsA_SVD_), dB.dot(self.itemsB_SVD_)])
        
        # Execute the clustering on all the data
        km = KMeans(n_clusters = self.n_clusters, n_init=20, max_iter=10)
        Y = km.fit_predict(all_data)
        Ac, Bc = Y[:len(itemsA_dict)], Y[len(itemsA_dict):]

        # Use the dictionaries to retag the elements
        inv_dict_A = {v:i for i,v in itemsA_dict.iteritems()}
        inv_dict_B = {v:i for i,v in itemsB_dict.iteritems()}
        clusters_A = self.n_clusters * np.ones((n_itemsA,))
        clusters_B = self.n_clusters * np.ones((n_itemsB,))
        for i, c in enumerate(Ac):
            clusters_A[inv_dict_A[i]] = c
        for i, c in enumerate(Bc):
            clusters_B[inv_dict_B[i]] = c
            
        return clusters_A, clusters_B
