import sys
from nearest_neighbour.faiss_index import FAISS
from nearest_neighbour.nn import CIFAR_DATA
from nearest_neighbour.ward_tree import WardTree


if __name__ == "__main__":

    if len(sys.argv) > 1:
        num_points = int(sys.argv[1])
    else:
        num_points = 10000

    ward_tree = WardTree()
    print("Fitting Ward tree with CIFAR data...")
    ward_tree.fit(CIFAR_DATA[:num_points])
    print("Ward tree fitted successfully.")
    ward_tree.pickle("ward_tree.pkl")

    faiss_index = FAISS()
    print("Fitting FAISS index with CIFAR data...")
    faiss_index.fit(CIFAR_DATA[:num_points])
    print("FAISS index fitted successfully.")
    faiss_index.pickle("faiss_index.pkl")
