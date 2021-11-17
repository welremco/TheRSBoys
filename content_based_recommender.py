from content_data_loader import load_data
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def recommend(id, amount):

    dirname = os.path.dirname(__file__)
    movies_file = os.path.join(dirname, 'MovieLens_m1/movies.dat')

    data = load_data(movies_file)
    #print(movie_Dict)

    # create an object for TfidfVectorizer
    tfidf_vector = TfidfVectorizer(stop_words='english')

    # apply the object to the genres
    tfidf_matrix = tfidf_vector.fit_transform(data[:, 2])
    tfidf_matrix = tfidf_matrix.todense()
    # print(tfidf_matrix.shape)
    # print(tfidf_matrix)
    # print(list(enumerate(tfidf_vector.get_feature_names())))

    ## create the cosine similarity matrix
    similarity_matrix = linear_kernel(tfidf_matrix, tfidf_matrix)
    # print(similarity_matrix.shape)
    # print(similarity_matrix)

    movie_list = list(enumerate(similarity_matrix[int(id)]))
    similar_movies = list(filter(lambda x: x[0] != int(id), sorted(movie_list, key=lambda x: x[1], reverse=True)))
    print('Here\'s the list of movies similar to ' + data[id][1] + '    (' + data[id][2] + ') :')
    for i, s in similar_movies[:amount]:
        print(data[i][1] + '    (' + data[i][2] + ')')


