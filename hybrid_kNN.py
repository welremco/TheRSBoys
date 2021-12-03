import load_data
import numpy as np


def cosine_similarity_array(movie_ratings, index, movie_ratings_nonzero):
    """
    Calculate cosine similarity between movie at index and all other movies in movie_ratings array
    :param movie_ratings: 2d array of size (num_movies, num_users)
    :param index: index of movie to compare against all other movies
    :param movie_ratings_nonzero: list of indices of nonzero movies in movie_ratings
    :return: 1d array with cosine similarities of each movie with the movie at index (including with itself)
    """
    similarity = np.zeros(len(movie_ratings))
    movie_i_ratings = movie_ratings[index]
    ri = movie_ratings_nonzero[index]
    # TODO tune amount of users that need to have rated a movie
    if len(ri) > 100:
        for j in range(len(movie_ratings)):
            movie_j_ratings = movie_ratings[j]
            rj = movie_ratings_nonzero[j]
            # TODO tune amount of users that need to have rated a movie
            if len(rj) > 100:
                ids = np.intersect1d(ri, rj, assume_unique=True)
                # TODO tune amount of users that need to have rated both movies
                if len(ids) > 10:
                    movie_i_nonzero_ratings = movie_i_ratings[ids]
                    movie_j_nonzero_ratings = movie_j_ratings[ids]
                    similarity[j] = faster_cosine_similarity(movie_i_nonzero_ratings, movie_j_nonzero_ratings)

    return similarity


def faster_cosine_similarity(a, b):
    return np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))


def load_movie_data():
    print("loading movie data...")
    return load_data.load_data("MovieLens_m1/movies.dat", "MovieLens_m1/ratings.dat")


def load_similarity_matrix(calculate=False, train_ratings=None):
    """
    Load similarity matrix from file or calculate it
    :param calculate: whether to calculate the data
    :param train_ratings: 2d array of size (num_movies, num_users), only used if calculate is True
    :return: similarity matrix
    """
    if calculate:
        print("preprocessing...")
        movie_ratings_nonzero = []
        train_ratings_t = np.transpose(train_ratings)
        for i in range(len(train_ratings_t)):
            movie_ratings_nonzero.append(np.nonzero(train_ratings_t[i])[0])

        print("preprocessing matrix...")
        similarity_matrix = np.zeros((len(train_ratings_t), len(train_ratings_t)), dtype=np.float16)
        for i in range(len(train_ratings_t)):
            print(i)
            similarity_matrix[i] = cosine_similarity_array(train_ratings_t, i, movie_ratings_nonzero)

        np.save("similarity_matrix.npy", similarity_matrix)
    else:
        similarity_matrix = np.load("similarity_matrix.npy")
    return similarity_matrix


def get_cf_results(similarity_matrix, ratings, movie_names, user_id):
    """
    Get the cosine similarity scores for a user based on their watched movies
    :param similarity_matrix: precomputed matrix of cosine similarities between movies
    :param ratings: 2d array of size (num_movies, num_users)
    :param movie_names: list of movie names
    :param user_id: user id to get recommendations for
    :return: sorted list of tuples of form (movie_name, predicted_rating)
    """
    recommendations = {}
    watched_movies = np.nonzero(ratings[:, user_id])[0]
    for movie_id in range(len(ratings[:, user_id])):
        rating = ratings[movie_id, user_id]
        if rating != 0 and movie_id in movie_names:
            similarity_array = similarity_matrix[movie_id]
            for i in range(len(similarity_array)):
                if similarity_array[i] != 0 and i not in watched_movies:
                    if i not in recommendations:
                        recommendations[i] = similarity_array[i]*rating  # *((rating-3)/2)
                    else:
                        recommendations[i] += similarity_array[i]*rating  # *((rating-3)/2)
    # divide all values by largest absolute value in recommendations
    max_abs = 0
    for movie_id in recommendations:
        if abs(recommendations[movie_id]) > max_abs:
            max_abs = abs(recommendations[movie_id])
    for movie_id in recommendations:
        recommendations[movie_id] /= max_abs

    return [(k, v) for k, v in sorted(recommendations.items(), key=lambda item: item[1], reverse=True)]
