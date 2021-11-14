import load_data
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def cosine_similarity_array(movie_ratings, index):
    """
    Calculate cosine similarity between movie at index and all other movies in movie_ratings array
    :param movie_ratings: 2d array of size (num_movies, num_users)
    :param index: index of movie to compare against all other movies
    :return: 1d array with cosine similarities of each movie with the movie at index (including with itself)
    """
    similarity = np.zeros(len(movie_ratings))
    movie_i_ratings = movie_ratings[index]
    ri = np.nonzero(movie_i_ratings)
    for j in range(len(movie_ratings)):
        movie_j_ratings = movie_ratings[j]
        rj = np.nonzero(movie_j_ratings)
        ids = np.intersect1d(ri, rj)
        movie_i_nonzero_ratings = np.take(movie_i_ratings, ids)
        movie_j_nonzero_ratings = np.take(movie_j_ratings, ids)
        if len(movie_j_nonzero_ratings) > 0:
            similarity[j] = cosine_similarity(np.expand_dims(movie_i_nonzero_ratings, 0),
                                              np.expand_dims(movie_j_nonzero_ratings, 0))[0][0]
        else:
            similarity[j] = 0
    return similarity

print("loading movie data...")
train_movie_genres, val_movie_genres, train_ratings, val_ratings, movie_names = load_data.load_data("MovieLens_m1/movies.dat", "MovieLens_m1/ratings.dat")

# take out movies with fewer than 10 ratings
# TODO tune amount of ratings
train_ratings = np.where(np.sum(train_ratings != 0, axis=0) >= 1000, train_ratings, 0)

while True:
    id = int(input("movie id: "))
    print(movie_names[id])

    similarity_array = cosine_similarity_array(np.transpose(train_ratings), id)
    similar_movie_ids = np.argpartition(similarity_array, -5)[-5:]
    similar_movie_ids_score = similarity_array[similar_movie_ids]

    for i in range(len(similar_movie_ids)):
        similar_id = similar_movie_ids[i]
        print(movie_names[similar_id], similar_movie_ids_score[i])
