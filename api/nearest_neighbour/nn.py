import pickle

import numpy as np
from nearest_neighbour.utils import unpickle

CIFAR_FILES = [
    "data_batch_1",
    "data_batch_2",
    "data_batch_3",
    "data_batch_4",
    "data_batch_5",
    "test_batch",
]

CIFAR_DATA = np.concatenate(
    [unpickle("/app/cifar-10-batches-py/" + f)[b"data"] for f in CIFAR_FILES], axis=0
)

DEFAULT_CLUSTER_SIZE = 40


class NNAlgorithm:
    """Base class for nearest neighbour algorithms used to fit and query an image dataset."""
    def fit(self, X, cluster_size=DEFAULT_CLUSTER_SIZE):
        """Fit the model to the data X."""
        raise NotImplementedError("fit method not implemented.")

    def query(self, x, k=1):
        """Query the k nearest neighbors of x."""
        raise NotImplementedError("query method not implemented.")

    def pickle(self, filename):
        """Save the model to a file."""
        with open(filename, "wb") as f:
            pickle.dump(self, f)
