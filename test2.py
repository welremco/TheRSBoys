import hybrid_kNN
from content_based_user_recommender import recommend, load, create_similarity_matrix, print_explanation
from load_data import load_data
import os
import numpy as np
import hybrid_kNN as hk
import hybrid_cf_cb_combinator
# from line_profiler_pycharm import profile

NUM_PREDICTIONS = 20

print("preprocessing...")

# get filepaths
dirname = os.path.dirname(__file__)
movies_file = os.path.join(dirname, 'MovieLens_m1/movies.dat')
ratings_file = os.path.join(dirname, 'MovieLens_m1/ratings.dat')

# load_data
train_movie_genres, valid_movie_genres, train_movie_ratings, valid_movie_ratings, movie_names = load_data(movies_file,
                                                                                                          ratings_file)
# load similarity matrix for cf
# True, train_movie_ratings)
similarity_matrix = hk.load_similarity_matrix(False, train_movie_ratings)

movies, ratings = load(train_movie_ratings)
similarity_matrix_cb = create_similarity_matrix(movies)


# @profile
def hybrid_recommend(user_id, num_predictions=NUM_PREDICTIONS):
    for x in range(1):
        # ask for user id
        print('asking for input')
        # user_id = int(input("Please enter a user id: "))
        # content based
        # cb_scores = recommend(10, user_id, train_movie_ratings)
        # print('original: ', train_movie_ratings.size)
        # print('cb:   ', cb_scores)
        # collaborative
        # cf_scores = hk.get_cf_results(similarity_matrix, np.transpose(train_movie_ratings), movie_names, user_id)
        # print('cf:   ', cf_scores)
        # combination
        # final_output = hybrid_cf_cb_combinator.combine(cf_scores, 0.9, cb_scores, 0.1)
        # print(final_output[:10])

        mAP = 0
        num = 0
        total = 0
        total_baseline = 0
        for u in range(100, 200):
            user_id = u
            if u % 1 == 0 and u - 100 != 0:
                print('iteration: ', u - 100)
                # print('mAP:', mAP/num)
            # get list of tuples [(movie_id, rating), (movie_id, rating), ...] for valid_movie_ratings for user_id
            valid_movie_list = []
            counter = 0
            for i in range(len(valid_movie_ratings[user_id])):
                valid_movie_list.append((i, valid_movie_ratings[user_id][i]))
                if valid_movie_ratings[user_id][i] != 0:
                    counter += 1
            if counter > 20:
                # sort list by rating
                valid_movie_list.sort(key=lambda tup: tup[1], reverse=True)
                # print('valid: ', valid_movie_list[:NUM_PREDICTIONS])

                baseline = hybrid_kNN.get_top_rated_movies(np.transpose(train_movie_ratings), movie_names, user_id)

                cb_scores = recommend(10, user_id, movies, ratings, similarity_matrix_cb)
                # print('original: ', train_movie_ratings.size)
                # print('cb:   ', cb_scores)
                # collaborative
                cf_scores = hk.get_cf_results(similarity_matrix, np.transpose(train_movie_ratings), movie_names, user_id)
                # print('cf:   ', cf_scores)
                # combination
                final_output = hybrid_cf_cb_combinator.combine(dict(baseline), 1, cf_scores, 1, cb_scores, 1)
                print('recommendations : ', final_output)
                if int(final_output[0][1][1]) == 1:
                    print('This movie is recommended to you because it is very popular')
                if int(final_output[0][1][1]) == 2:
                    print('this is where the colaborative filtering explanation call must be')
                if int(final_output[0][1][1]) == 3:
                    print_explanation(final_output[0][0], user_id, movies, ratings, similarity_matrix_cb)
                Ap = hybrid_kNN.AP(valid_movie_list, final_output, NUM_PREDICTIONS, 4)
                Ap_baseline = hybrid_kNN.AP(valid_movie_list, baseline, NUM_PREDICTIONS, 4)
                total += Ap
                total_baseline += Ap_baseline
                num += 1
                print('mAP: ', Ap, total/num)
                print('mAP_baseline: ', Ap_baseline, total_baseline/num)
                mAP += Ap
        mAP /= num
        print(mAP)

# baseline: 0.156 mAP


print("starting...")
hybrid_recommend(1, NUM_PREDICTIONS)

