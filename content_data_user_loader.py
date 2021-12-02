import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def load_data_ratings(path):
    # seed randomness for testing purposes
    np.random.seed(0)
    # loading all data
    data = np.genfromtxt(path, dtype='str', delimiter='::', usecols=(0, 1, 2))

    #print(data[0][1])

    return data


