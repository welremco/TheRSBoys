from content_based_user_recommender import recommend
import os

dirname = os.path.dirname(__file__)
movies_file = os.path.join(dirname, 'MovieLens_m1/movies.dat')
ratings_file = os.path.join(dirname, 'MovieLens_m1/ratings.dat')

for x in range(3):
    user = int(input("Please enter a user id: "))
    recommend(10, user)
