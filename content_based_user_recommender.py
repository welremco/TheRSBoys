from content_data_loader import load_data
from content_data_user_loader import load_data_ratings
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


def recommend(amount, user_id):

    dirname = os.path.dirname(__file__)
    movies_file = os.path.join(dirname, 'MovieLens_m1/movies.dat')
    ratings_file = os.path.join(dirname, 'MovieLens_m1/ratings.dat')

    data_movies = load_data(movies_file)
    data_ratings = load_data_ratings(ratings_file)

    # create an object for TfidfVectorizer
    tfidf_vector = TfidfVectorizer(stop_words='english')

    # apply the object to the genres
    tfidf_matrix = tfidf_vector.fit_transform(data_movies[:, 2])
    tfidf_matrix = tfidf_matrix.todense()
    # print(tfidf_matrix.shape)
    # print(tfidf_matrix)
    # print(list(enumerate(tfidf_vector.get_feature_names())))

    # create the cosine similarity matrix
    similarity_matrix = linear_kernel(tfidf_matrix, tfidf_matrix)
    # print(similarity_matrix.shape)
    # print(similarity_matrix)

    seen_list = []
    # print(data_ratings[0, :])
    # print(type(data_ratings))

    for item in data_ratings:
        # print(type(item[0]))
        if int(item[0]) == int(user_id):
            if int(item[2]) == int(5):
                # print(item)
                seen_list.append(item)

    # print(len(seen_list))

    score_list = []
    # print(len(data_movies))
    for i in range(len(data_movies)):
        score_list.append((i, 0, 0))

    for i in range(len(data_movies)):
        to_change = score_list[i]
        new_tuple = (to_change[0], to_change[1], data_movies[i][0])
        score_list[i] = new_tuple
    # print(score_list)

    for seen in seen_list:
        for index in range(len(data_movies)):
            movie = data_movies[index]
            if int(seen[1]) == int(movie[0]):
                # print(movie)
                print('seen: ', seen, '  index: ', index, ' -- ', movie)
                current_list = list(enumerate(similarity_matrix[int(index)]))
                # print(current_list)
                for score_tuple in range(len(current_list)):
                    # print(score_list.__len__())
                    to_replace = score_list[score_tuple]
                    # print(to_replace)
                    # print(current_list[index])
                    new_score_sum = to_replace[1] + current_list[score_tuple][1]
                    # print(new_score_sum)
                    new_tuple = (score_tuple, new_score_sum, data_movies[score_tuple][0])
                    # print(new_tuple)
                    score_list[score_tuple] = new_tuple

    count = len(seen_list)
    #print(count)
    for cntr in range(len(score_list)):
        to_divide = score_list[cntr][1]
        final_score = to_divide / count
        new_final_score_tuple = (cntr, final_score, score_list[cntr][2])
        score_list[cntr] = new_final_score_tuple

    # print(score_list)
    similar_movies_user = list(sorted(score_list, key=lambda x: x[1], reverse=True))
    print('Here\'s the list of movies similar to selected based on movies you rated 5 stars :')
    print(' ')

    for i, s, mid in similar_movies_user[:amount]:
        # print('i  ', i)
        # print('s  ', s)
        # print('m  ', similarity_matrix[i,id])
        print(data_movies[i][1] + ' Similarity:', s,  '   (' + data_movies[i][2] + ') - movieID: ', mid)
        # print(' ')



    #movie_list = list(enumerate(similarity_matrix[int(id)]))
    #print(movie_list[0])
    #print(type(movie_list[0]))
    #similar_movies = list(filter(lambda x: x[0] != int(id), sorted(movie_list, key=lambda x: x[1], reverse=True)))
    #print('Here\'s the list of movies similar to ' + data_movies[id][1] + '    (' + data_movies[id][2] + ') :')
    #print(' ')
    #print(similar_movies[0][1])
    #for i, s in similar_movies[:amount]:
        #print('i  ', i)
        #print('s  ', s)
        #print('m  ', similarity_matrix[i,id])
        #print(data_movies[i][1] + ' Similarity:', s ,  '   (' + data_movies[i][2] + ')')
        #print(' ')



