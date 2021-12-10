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
    if len(ri) > 300:
        for j in range(len(movie_ratings)):
            movie_j_ratings = movie_ratings[j]
            rj = movie_ratings_nonzero[j]
            # TODO tune amount of users that need to have rated a movie
            if len(rj) > 300:
                ids = np.intersect1d(ri, rj, assume_unique=True)
                # TODO tune amount of users that need to have rated both movies
                if len(ids) > 300:
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
            if i % 100 == 0:
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
    biggest_contributor = [('no movie', 0) for i in range(len(similarity_matrix))]
    watched_movies = np.array([1])
    # watched_movies = np.nonzero(ratings[:, user_id])[0]
    for movie_id in range(len(ratings[:, user_id])):
        rating = ratings[movie_id, user_id]
        if rating != 0 and movie_id in movie_names:
            similarity_array = similarity_matrix[movie_id]
            for i in range(len(similarity_array)):
                if similarity_array[i] != 0 and i not in watched_movies:
                    if i not in recommendations:
                        score = similarity_array[i] * rating
                        recommendations[i] = score
                        if score > biggest_contributor[i][1]:
                            biggest_contributor[i] = (movie_names[movie_id], score)
                    else:
                        score = similarity_array[i] * rating
                        recommendations[i] += score
                        if score > biggest_contributor[i][1]:
                            biggest_contributor[i] = (movie_names[movie_id], score)
    # divide all values by largest absolute value in recommendations
    max_abs = 0
    for movie_id in recommendations:
        if abs(recommendations[movie_id]) > max_abs:
            max_abs = abs(recommendations[movie_id])
    for movie_id in recommendations:
        recommendations[movie_id] /= max_abs

    # [(k, v) for k, v in sorted(recommendations.items(), key=lambda item: item[1], reverse=True)]
    return recommendations, biggest_contributor


def AP(actual, predicted, n=10, min_rating=0):
    """
    Calculate average precision
    :param actual: list of tuples of form (movie_id, rating) sorted by highest rating
    :param predicted: list of tuples of form (movie_id, rating) sorted by highest rating
    :param n: number of top recommendations to consider
    :param min_rating: minimum rating to consider
    :return: average precision
    """
    adjusted_n = min(n, len(actual))
    predicted_list = [p[0] for p in predicted[:n]]
    actual_list = [a[0] for a in actual if a[1] >= min_rating]
    average_precision = 0
    correct = 0
    for k in range(n):
        if predicted_list[k] in actual_list:
            correct += 1
            average_precision += correct/min((k+1), adjusted_n)
            # print(correct/min((k+1), adjusted_n))
    if correct == 0:
        return 0.0
    return average_precision/correct


def get_top_rated_movies(ratings, movie_names, user_id):
    """
    return top rated movies that user has not watched
    :param ratings: 2d array of size (num_movies, num_users)
    :param movie_names: list of movie names
    :param user_id: user id to get recommendations for
    :return: list of tuples of form (movie_id, rating)
    """
    top_rated_movies = []
    for i in range(len(ratings[:, user_id])):
        if ratings[i, user_id] == 0 and i in movie_names:
            # get average rating for movie i from ratings array not counting 0 ratings
            nonzero_ratings = np.nonzero(ratings[i])[0]
            if len(nonzero_ratings) >= 200:
                average_rating = np.mean(ratings[i, nonzero_ratings])
                top_rated_movies.append((i, average_rating))
    top_rated_movies = sorted(top_rated_movies, key=lambda x: x[1], reverse=True)
    # print(len(top_rated_movies))
    return top_rated_movies






