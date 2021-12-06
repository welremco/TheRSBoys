from content_based_user_recommender import recommend
from load_data import load_data
import os

dirname = os.path.dirname(__file__)
movies_file = os.path.join(dirname, 'MovieLens_m1/movies.dat')
ratings_file = os.path.join(dirname, 'MovieLens_m1/ratings.dat')

# load_data
train_movie_genres, valid_movie_genres, train_movie_ratings, valid_movie_ratings, movie_names = load_data(movies_file,
                                                                                                          ratings_file)

for x in range(3):
    user = int(input("Please enter a user id: "))
    recommend(10, user, train_movie_ratings)
