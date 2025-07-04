import faiss
import numpy as np
from nearest_neighbour.nn import CIFAR_DATA, DEFAULT_CLUSTER_SIZE, NNAlgorithm


class FAISS(NNAlgorithm):
    def __init__(self, index=None):
        self.index = index

    def fit(self, X, cluster_size=DEFAULT_CLUSTER_SIZE):
        dimension = X.shape[1]
        num_clusters = int(X.shape[0] / cluster_size)
        quantizer = faiss.IndexFlatL2(dimension)
        self.index = faiss.IndexIVFFlat(quantizer, dimension, num_clusters)
        self.index.train(X.astype("float32"))
        self.index.add(X.astype("float32"))

    def query(self, x, k=1):
        # Placeholder for querying the FAISS index
        # You can implement or import the actual logic here
        D, I = self.index.search(x, k)
        I = np.random.choice(I[0], 1)
        return CIFAR_DATA[I[0]].reshape(3, 32, 32).transpose(1, 2, 0).astype("uint8")
