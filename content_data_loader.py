import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


def load_data(path):

    # seed randomness for testing purposes
    np.random.seed(0)
    # loading all data
    data = np.genfromtxt(path, dtype='str', delimiter='::', usecols=(0, 1, 2))

    nmoviesid = np.unique(data[:, 0]).shape[0]  # number of movie ids
    # ngenres = np.unique(data[:, 1]).shape[0]  # number of genres
    nmovies = data.shape[0]  # number of movies

    #  change genre tags to string separated by spaces
    for i in range(len(data[:, ])):
        extract = data[i][2]
        changed = extract.replace('|', ' ')
        data[i][2] = changed
        #print(data[i][2])

    #  count the number of occurences of each genre
    genre_counts = dict()
    for i in range(len(data[:, ])):
        for g in data[i][2].split(' '):
            #print(g)
            if g not in genre_counts:
                genre_counts[g] = 1
            else:
                genre_counts[g] = genre_counts[g] + 1
    #print(len(genre_counts))

    #  remove spaces, apostrophes and hyphens
    for i in range(len(data[:, ])):
        extract = data[i][2]
        changed = extract.replace('Sci-Fi', 'SciFi')
        changed_v2 = changed.replace('Children\'s', 'Children')
        final_changed = changed_v2.replace('Film-Noir', 'Noir')
        data[i][2] = final_changed
        #print(data[i][2])

    #print(data[257][0])
    #print(data[257][1])
    #print(data[257][2])
    return data