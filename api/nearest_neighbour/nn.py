import pickle
import numpy as np

CIFAR_FILES = [
    "data_batch_1",
    "data_batch_2",
    "data_batch_3",
    "data_batch_4",
    "data_batch_5",
    "test_batch",
]


def unpickle(file):
    with open(file, "rb") as fo:
        dict = pickle.load(fo, encoding="bytes")
    return dict


CIFAR_DATA = np.concatenate(
    [unpickle("./cifar-10-batches-py/" + f)[b"data"] for f in CIFAR_FILES], axis=0
)
DEFAULT_CLUSTER_SIZE = 40


class NNAlgorithm:
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
