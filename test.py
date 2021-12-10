import hybrid_kNN
from content_based_user_recommender import recommend, load, create_similarity_matrix
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
# load similarity matrix for cf
# True, train_movie_ratings)
# similarity_matrix = hk.load_similarity_matrix(True, train_movie_ratings)

movies, ratings = load(train_movie_ratings)
similarity_matrix_cb = create_similarity_matrix(movies)

for x in range(100):
    # ask for user id
    print('asking for input')
    user_id = int(input("Please enter a user id: "))
    # content based
    cb_scores = recommend(10, user_id, movies, ratings, similarity_matrix_cb)
    # print('original: ', train_movie_ratings.size)
    # print('cb:   ', cb_scores)
    # collaborative
    # cf_scores = hk.get_cf_results(similarity_matrix, np.transpose(train_movie_ratings), movie_names, user_id)
    # print('cf:   ', cf_scores)
    # combination
    # final_output = hybrid_cf_cb_combinator.combine(cf_scores, 0.7, cb_scores, 0.3)
    print(cb_scores)

    # get list of tuples [(movie_id, rating), (movie_id, rating), ...] for valid_movie_ratings for user_id
    valid_movie_list = []
    for i in range(len(valid_movie_ratings[user_id])):
        valid_movie_list.append((i, valid_movie_ratings[user_id][i]))

    # sort list by rating
    valid_movie_list.sort(key=lambda tup: tup[1], reverse=True)
    # print('valid: ', valid_movie_list[:10])
    Ap = hybrid_kNN.AP(valid_movie_list, cb_scores, 20, 3)
    print('AP: ', Ap)



