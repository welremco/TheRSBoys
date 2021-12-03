from load_data import load_data
import os
import hybrid_kNN as hk
import numpy as np

dirname = os.path.dirname(__file__)
movies_file = os.path.join(dirname, 'MovieLens_m1/movies.dat')
ratings_file = os.path.join(dirname, 'MovieLens_m1/ratings.dat')

print("Loading movie data...")
train_movie_genres, valid_movie_genres, train_movie_ratings, valid_movie_ratings, movie_names = load_data(movies_file,
                                                                                                          ratings_file)

print("Loading precomputed similarity matrix...")
similarity_matrix = hk.load_similarity_matrix()
while True:
    user_id = int(input("Enter user id: "))
    scores_list = hk.get_cf_results(similarity_matrix, np.transpose(train_movie_ratings), movie_names, user_id)
    print(scores_list)
