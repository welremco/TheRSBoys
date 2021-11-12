#THIS CODE IS SLIGHTLY INSPIRED FROM lkasfd

import numpy as np


def load_data_ratings(path):
    # seed randomness for testing purposes
    np.random.seed(0)
    # loading all data
    data = np.loadtxt(path,delimiter='::').astype('int32')

    n_u = np.unique(data[:, 0]).shape[0]  # number of users
    n_m = np.unique(data[:, 1]).shape[0]  # number of movies
    n_r = data.shape[0]  # number of ratings

    # these dictionaries define a mapping from user/movie id to to user/movie number (contiguous from zero)
    udict = {}
    for i, u in enumerate(np.unique(data[:, 0]).tolist()):
        udict[u] = i
    mdict = {}
    for i, m in enumerate(np.unique(data[:, 1]).tolist()):
        mdict[m] = i

    # shuffle indices
    idx = np.arange(n_r)
    np.random.shuffle(idx)

    trainRatings = np.zeros((n_u, n_m), dtype='float32')
    validRatings = np.zeros((n_u, n_m), dtype='float32')

    for i in range(n_r):
        u_id = data[idx[i], 0]
        m_id = data[idx[i], 1]
        r = data[idx[i], 2]

        # the first few ratings of the shuffled data array are validation data
        if i <= 0.1 * n_r:
            validRatings[udict[u_id], mdict[m_id]] = int(r)
        # the rest are training data
        else:
            trainRatings[udict[u_id], mdict[m_id]] = int(r)

    # if transpose:
    #     trainRatings = trainRatings.T
    #     validRatings = validRatings.T

    return trainRatings, validRatings

def load_data_movies(path):
    # seed randomness for testing purposes
    np.random.seed(0)
    # loading all data
    data = np.loadtxt(path, dtype='string', delimiter='::')

    n_u = np.unique(data[:, 0]).shape[0]  # number of users
    n_m = np.unique(data[:, 1]).shape[0]  # number of movies
    n_r = data.shape[0]  # number of ratings

    # these dictionaries define a mapping from user/movie id to to user/movie number (contiguous from zero)
    title_dict = {}
    for i, u in enumerate(np.unique(data[:, 0]).tolist()):
        title_dict[u] = i
    genre_dict = {}
    for i, m in enumerate(np.unique(data[:, 1]).tolist()):
        genre_dict[m] = i

    print(title_dict)
    exit(0)
    # shuffle indices
    idx = np.arange(n_r)
    np.random.shuffle(idx)

    trainRatings = np.zeros((n_u, n_m), dtype='float32')
    validRatings = np.zeros((n_u, n_m), dtype='float32')

    for i in range(n_r):
        title_dict = data[idx[i], 0]
        genre_dict = data[idx[i], 1]
        r = data[idx[i], 2]

        # the first few ratings of the shuffled data array are validation data
        if i <= 0.1 * n_r:
            validRatings[title_dict[title_id], genre_dict[genre_id]] = int(r)
        # the rest are training data
        else:
            trainRatings[title_dict[title_id], genre_dict[genre_id]] = int(r)

    # if transpose:
    #     trainRatings = trainRatings.T
    #     validRatings = validRatings.T

    return trainRatings, validRatings

