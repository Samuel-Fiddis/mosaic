import pickle

def unpickle(file, encoding="bytes"):
    with open(file, "rb") as fo:
        dict = pickle.load(fo, encoding=encoding)
    return dict