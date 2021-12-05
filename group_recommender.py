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
    size = int(input("Please enter a group size:  "))
    group_scores = []
    for s in range(size):
        print('group - ', len(group_scores))
        user_id =int(input("Please enter a user id:  "))
        # content based
        cb_scores = recommend(10, user_id)
        print('cb:   ', cb_scores)
        # collaborative
        cf_scores = hk.get_cf_results(similarity_matrix, np.transpose(train_movie_ratings), movie_names, user_id)
        print('cf:   ', cf_scores)
        # combination
        final_output = hybrid_cf_cb_combinator.combine(cf_scores, 0.5, cb_scores, 0.5)
        print('im here')
        print('user - ', final_output.__len__())
        if(s == 0):
            group_scores = final_output
        else:
            for group in range(len(group_scores)):
                #print(group, '   ', len(group_scores))
                group_score = group_scores[group][1]
                # print(cf_score)
                for index in range(len(final_output)):
                    if int(group_scores[group][0]) == int(final_output[index][0]):
                        user_score = final_output[index][1]
                        # print(cb_score)
                        #print(group_score, '  -- ', user_score)
                        final_score = group_score + user_score
                        # print(final_score)
                        final_score_tuple = (group_scores[group][0], final_score)
                        # print(final_score_tuple)
                        group_scores[group] = final_score_tuple
    for cntr in range(len(group_scores)):
        element = group_scores[cntr]
        to_divide = element[1]
        final_score = to_divide / size
        new_final_score_tuple = (element[0], final_score)
        group_scores[cntr] = new_final_score_tuple


    print(group_scores)