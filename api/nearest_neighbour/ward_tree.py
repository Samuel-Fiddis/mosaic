from nearest_neighbour.nn import NNAlgorithm, CIFAR_DATA

from scipy.cluster import hierarchy
import numpy as np


class TreeNode:
    def __init__(self):
        self.node_id = None
        self.left = None
        self.right = None
        self.data = None
        self.data_computed = False

    def compute_data(self):
        if self.data_computed:
            return
        self.left.compute_data()
        self.right.compute_data()
        self.data = np.average([self.left.data, self.right.data], axis=0)
        self.data_computed = True

    def get_image_data(self):
        return self.data

    def find_leaf(self, img_data):
        if self.left == None:
            if self.right == None:
                return self.data
            else:
                return self.right.find_leaf(img_data)
        elif self.right == None:
            return self.left.find_leaf(img_data)
        if np.linalg.norm(self.left.data - img_data) < np.linalg.norm(
            self.right.data - img_data
        ):
            return self.left.find_leaf(img_data)
        else:
            return self.right.find_leaf(img_data)


def construct_tree_from_children(children, data):
    nodes = []
    for n in range(data.shape[0]):
        node = TreeNode()
        node.node_id = n
        node.data = np.reshape(data[n], (3, 32, 32)).transpose(1, 2, 0).astype("uint8")
        node.data_computed = True
        nodes.append(node)

    for i in range(len(children)):
        node = TreeNode()
        node.node_id = i + data.shape[0]
        node.left = children[i][0]
        node.right = children[i][1]
        nodes.append(node)

    for node in nodes:
        if node.left != None:
            node.left = nodes[node.left]
        if node.right != None:
            node.right = nodes[node.right]

    nodes[-1].compute_data()  # Should compute all nodes data

    return nodes[-1]


class WardTree(NNAlgorithm):
    def __init__(self):
        self.tree = None

    def fit(self, X):
        # Placeholder for fitting a Ward hierarchical tree
        # You can implement or import the actual logic here
        X = np.asarray(X)
        if X.ndim == 1:
            X = np.reshape(X, (-1, 1))

        X = np.require(X, requirements="W")
        linkage_matrix = hierarchy.ward(X)
        children = linkage_matrix[:, :2].astype(np.intp)

        self.tree = construct_tree_from_children(children, X)

    def query(self, x, k=1):
        # Placeholder for querying the Ward tree
        # You can implement or import the actual logic here
        return self.tree.find_leaf(x)
