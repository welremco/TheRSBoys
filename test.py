from content_based_recommender import recommend
import os

dirname = os.path.dirname(__file__)
movies_file = os.path.join(dirname, 'MovieLens_m1/movies.dat')
ratings_file = os.path.join(dirname, 'MovieLens_m1/ratings.dat')

for x in range(3):
    var = int(input("Please enter a movie id: "))
    recommend(var, 10)
