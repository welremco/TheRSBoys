from content_data_loader import load_data
from content_data_user_loader import load_data_ratings
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def load():

    # generate filepaths
    dirname = os.path.dirname(__file__)
    movies_file = os.path.join(dirname, 'MovieLens_m1/movies.dat')
    ratings_file = os.path.join(dirname, 'MovieLens_m1/ratings.dat')

    # load moviedata (movieID, title, genres)
    movies = load_data(movies_file)
    # load ratings (userID, movieID, rating)
    ratings = load_data_ratings(ratings_file)

    return movies, ratings


def create_similarity_matrix(data_m):

    # create an object for TfidfVectorizer
    tfidf_vector = TfidfVectorizer(stop_words='english')

    # apply the object to the genres
    tfidf_matrix = tfidf_vector.fit_transform(data_m[:, 2])
    tfidf_matrix = tfidf_matrix.todense()

    # create the cosine similarity matrix
    similarity_matrix = linear_kernel(tfidf_matrix, tfidf_matrix)

    return similarity_matrix


def get_seen_movies(data_r, u_id):

    # create empty list to append seen movies into
    seen_list = []

    # for each rating
    for item in data_r:
        # if rating was performed by user
        if int(item[0]) == int(u_id):
            if(int(item[2]) == 5):
                # append rating (uID, mID, rating) to list of seen movies
                seen_list.append(item)

    return seen_list


def create_empty_scores_list(data_m):

    # create empty list to append tuples
    score_list = []
    # for each movie create a tuple with index
    for i in range(len(data_m)):
        score_list.append((i, 0, 0))

    # add movie ID's to empty tuples so that they do not only
    # hold line list index for later output (index, score (0 for now), movieID)
    for i in range(len(data_m)):
        to_change = score_list[i]
        new_tuple = (to_change[0], to_change[1], data_m[i][0])
        score_list[i] = new_tuple

    return score_list


def compute_recommendations(list_seen, data_m, similarity_matrix, scores):
    # for each seen movie
    for seen in list_seen:
        # decide weight based on score
        # NOT DONE HERE, ONLY 5stars considered
        # for each movie in the dataset
        for index in range(len(data_m)):
            movie = data_m[index]
            # if they are the same
            if int(seen[1]) == int(movie[0]):
                print('seen: ', seen, '  index: ', index, ' -- ', movie)
                # get the similarity scores for this movie with all other movies
                current_list = list(enumerate(similarity_matrix[int(index)]))
                # for each scores_tuple in the list of all moviescores add weighted score to scoresum
                for score_tuple in range(len(current_list)):
                    # get the tuple to edit
                    to_replace = scores[score_tuple]
                    # compute score to add by looking at similarity matrix and multiplying by weight
                    score_to_add = current_list[score_tuple][1]
                    # computed score to already present sum of scores
                    new_score_sum = to_replace[1] + score_to_add
                    # create new tuple with new sum
                    new_tuple = (score_tuple, new_score_sum, data_m[score_tuple][0])
                    # replace old tuple by new tuple
                    scores[score_tuple] = new_tuple

    return scores


def average_scores(list_seen, list_scores):

    # count the amount of seen movies
    count = len(list_seen)

    # for each tuple in the scoreslist divide the score by the count of seen movies to get a score between 0-1
    for cntr in range(len(list_scores)):
        to_divide = list_scores[cntr][1]
        final_score = to_divide / count
        new_final_score_tuple = (cntr, final_score, list_scores[cntr][2])
        list_scores[cntr] = new_final_score_tuple

    return list_scores

def remove_seen(seen_list, sorted_list):

    # for each seen movie
    for seen in seen_list:
        # search for it in the sorted list of scores
        for remove in sorted_list:
            # if (when) found remove from sorted scorelist
            if int(remove[2]) == int(seen[1]):
                sorted_list.remove(remove)

    return sorted_list

def convert_output(sorted_scores_list):

    # create empty output list
    output = []

    # for each tuple (index, score, id) create tuple (id, score) to add to output list
    for t in sorted_scores_list:
        output_tuple = (t[2], t[1])
        output.append(output_tuple)

    return output


def recommend(amount, user_id):

    # load data from files
    data_movies, data_ratings = load()

    # create the similarity matrix
    similarity_matrix = create_similarity_matrix(data_movies)

    # create list of seen movies aka movies a user has rated (5stars for now)
    seen_list = get_seen_movies(data_ratings, user_id)

    # create list to hold scores and fill with empty tuples
    score_list = create_empty_scores_list(data_movies)

    # for each seen movie add the similarity scores up to a sum per movie tuple in the scoreslist
    score_list = compute_recommendations(seen_list, data_movies, similarity_matrix, score_list)

    # average scores to be back between 0-1 by dividing through amount of seen movies
    score_list = average_scores(seen_list, score_list)

    # sort scorelist list by scores and store as similar movies list
    similar_movies_user = list(sorted(score_list, key=lambda x: x[1], reverse=True))

    # remove seen movies from sorted similar movies list
    remove_seen(seen_list, similar_movies_user)

    # some printstatements for testing
    print(' ')
    print('Here\'s the list of movies similar to selected based on movies you rated in the past :')
    print(' ')
    for i, s, mid in similar_movies_user[:amount]:
        # print('i  ', i)
        # print('s  ', s)
        # print('m  ', similarity_matrix[i,id])
        print(data_movies[i][1] + ' Similarity:', s,  '   (' + data_movies[i][2] + ') - movieID: ', mid)
        print(i, ' ', s, ' ', mid)
        # print(' ')


    # create output list in agreed format [(id, score), (id, score), ...] (so without original dataindex
    output = convert_output(similar_movies_user)

    print(output)

