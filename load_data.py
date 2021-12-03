# THIS CODE IS SLIGHTLY INSPIRED FROM lkasfd

import numpy as np


def load_data(path1, path2):
    np.random.seed(0)
    # path1 is movies and path2 is ratings

    data1 = np.genfromtxt(path1, dtype='str', delimiter='::', usecols=(0, 1, 2))
    data2 = np.loadtxt(path2, delimiter='::').astype('int32')

    nmoviesid = np.unique(data1[:, 0]).shape[0]  # number of movie ids
    nmovies = data1.shape[0]  # number of movies]
    movie_dict = {}
    for i in range(len(data1[:, ])):
        movie_dict[int(data1[i][0])] = data1[i, 1]

    # print(title_dict)
    genre_dict = {}
    # divide genres more
    ngenres = 0  # number of genres
    for i, m in enumerate(np.unique(data1[:, 2]).tolist()):
        m = m.split("|")
        # print(m)
        for word in m:
            if word not in genre_dict:
                genre_dict[word] = ngenres
                ngenres = ngenres + 1


    idx = np.arange(nmovies)
    # np.random.shuffle(idx)
    trainMovies = np.zeros((int(data1[nmoviesid - 1][0]) + 1, ngenres), dtype='float32')
    validMovies = np.zeros((int(data1[nmoviesid - 1][0]) + 1, ngenres), dtype='float32')

    for i in range(nmovies):
        title_id = data1[idx[i], 0]
        genre_id = data1[idx[i], 2]
        # print(genre_id)
        # print(genre_dict)
        # r = data[idx[i], 2]
        for word in genre_id.split("|"):
            if i <= 0.1 * nmovies:
                trainMovies[int(title_id), genre_dict[word]] = 1
            else:
                validMovies[int(title_id), genre_dict[word]] = 1




    nusers = np.unique(data2[:, 0]).shape[0]  # number of users
    # nmovies = np.unique(data[:, 1]).shape[0]  # number of movies
    nratings = data2.shape[0]  # number of ratings
    # these dictionaries define a mapping from user/movie id to to user/movie number (contiguous from zero)
    udict = {}
    for i, u in enumerate(np.unique(data2[:, 0]).tolist()):
        udict[u] = i
    mdict = {}
    for i, m in enumerate(np.unique(data2[:, 1]).tolist()):
        mdict[m] = i
    revmdict = {v: k for k, v in mdict.items()}

    # shuffle index around
    idx = np.arange(nratings)
    # np.random.shuffle(idx)

    trainRatings = np.zeros((nusers, int(data1[nmoviesid - 1][0]) + 1), dtype='float32')
    validRatings = np.zeros((nusers, int(data1[nmoviesid - 1][0]) + 1), dtype='float32')

    for i in range(nratings):
        u_id = data2[idx[i], 0]
        m_id = data2[idx[i], 1]
        r = data2[idx[i], 2]

        # Validation
        if i <= 0.1 * nratings:
            validRatings[udict[u_id], m_id] = int(r)
        else:
            trainRatings[udict[u_id], m_id] = int(r)

    # get average rating in every column of trainRatings excluding zero ratings
    average = np.zeros((nusers, 1), dtype='float32')
    for i in range(nusers):
        if np.count_nonzero(trainRatings[i, :]) > 0:
            average[i] = np.mean(trainRatings[i, trainRatings[i, :] != 0])
        else:
            average[i] = 0
    # subtract average from every column of trainRatings except zero ratings
    for i in range(nusers):
        trainRatings[i, trainRatings[i, :] != 0] = trainRatings[i, trainRatings[i, :] != 0] - average[i]

    return trainMovies, validMovies, trainRatings, validRatings, movie_dict
