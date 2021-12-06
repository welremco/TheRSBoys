from content_based_user_recommender import recommend
from load_data import load_data
import os
import numpy as np
import hybrid_kNN as hk
import hybrid_cf_cb_combinator

def ask_for_size():

    print('asking for input')
    size = int(input("Please enter a group size:  "))

    return size

def get_all_user_lists(groupsize):

    list_of_user_outputs = []

    for s in range(groupsize):
        user_id = int(input("Please enter a user id:  "))
        # content based
        cb_scores = recommend(10, user_id, train_movie_ratings)
        print('cb:   ', cb_scores)
        # collaborative
        cf_scores = hk.get_cf_results(similarity_matrix, np.transpose(train_movie_ratings), movie_names, user_id)
        print('cf:   ', cf_scores)
        # combination
        final_output = hybrid_cf_cb_combinator.combine(cf_scores, 0.5, cb_scores, 0.5)
        print('hybrid:   ', final_output)
        print('userlist length:   ', len(final_output))
        user_list_pair = (user_id, final_output)
        list_of_user_outputs.append(user_list_pair)

    return list_of_user_outputs


def remove_misery(list_users, threshold):

    for user in range(size):
        i = 0
        n = len(list_users[user][1])
        while i < n:
            if list_users[user][1][i][1] < threshold:
                del list_users[user][1][i]
                n = n - 1
            else:
                i = i + 1

    return list_users


def sum_user_scores(reduced_list, n):

    summed = []

    for iteration in range(len(reduced_list)):
        if iteration == 0:
            first_step = []
            for tuple in reduced_list[iteration][1]:
                new_triplet = (int(tuple[0]), tuple[1], 1)
                first_step.append(new_triplet)
            summed = first_step
        else:
            for tuple in reduced_list[iteration][1]:
                for triplet in range(len(summed)):
                    if int(tuple[0]) == summed[triplet][0]:
                        summed_score = tuple[1] + summed[triplet][1]
                        new_triplet = (summed[triplet][0], summed_score, summed[triplet][2] + 1)
                        summed[triplet] = new_triplet

    tuples = []
    for summed_triplet in summed:
        if summed_triplet[2] == n:
            mID = summed_triplet[0]
            value = summed_triplet[1]
            sum_tuple = (mID, value)
            tuples.append(sum_tuple)

    return tuples


def average(sums, n):

    for scoretuple in range(len(sums)):
        to_divide = sums[scoretuple][1]
        divided = to_divide / n
        divided_tuple = (sums[scoretuple][0], divided)
        sums[scoretuple] = divided_tuple

    return sums



# get filepaths
dirname = os.path.dirname(__file__)
movies_file = os.path.join(dirname, 'MovieLens_m1/movies.dat')
ratings_file = os.path.join(dirname, 'MovieLens_m1/ratings.dat')

# load_data
train_movie_genres, valid_movie_genres, train_movie_ratings, valid_movie_ratings, movie_names = load_data(movies_file,
                                                                                                          ratings_file)
# load similaritymatrix for cf
similarity_matrix = hk.load_similarity_matrix()

size = ask_for_size()

list_of_user_outputs = get_all_user_lists(size)

no_misery = remove_misery(list_of_user_outputs, 0.3)

summed_scores = sum_user_scores(no_misery, size)

averaged_scores = average(summed_scores, size)
sorted_scores = list(sorted(averaged_scores, key=lambda x: x[1], reverse=True))

print(' ')
print(sorted_scores)
print('grouplist length:   ', len(sorted_scores))

