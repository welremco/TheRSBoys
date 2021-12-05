from content_based_user_recommender import recommend
from load_data import load_data
import os
import numpy as np
import hybrid_kNN as hk
import hybrid_cf_cb_combinator

# get filepaths
dirname = os.path.dirname(__file__)
movies_file = os.path.join(dirname, 'MovieLens_m1/movies.dat')
ratings_file = os.path.join(dirname, 'MovieLens_m1/ratings.dat')

# load_data
train_movie_genres, valid_movie_genres, train_movie_ratings, valid_movie_ratings, movie_names = load_data(movies_file,
                                                                                                          ratings_file)
# load similaritymatrix for cf
similarity_matrix = hk.load_similarity_matrix()

for x in range(3):
    # ask for user id
    print('asking for input')
    user_id = int(input("Please enter a user id: "))
    # content based
    cb_scores = recommend(10, user_id)
    print('original: ', train_movie_ratings.size)
    print('cb:   ', cb_scores)
    # collaborative
    cf_scores = hk.get_cf_results(similarity_matrix, np.transpose(train_movie_ratings), movie_names, user_id)
    print('cf:   ', cf_scores)
    # combination
    final_output = hybrid_cf_cb_combinator.combine(cf_scores, 0.5, cb_scores, 0.5)
    print(final_output)
