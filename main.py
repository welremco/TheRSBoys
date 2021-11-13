from load_data import load_data_movies, load_data_ratings
import os

dirname = os.path.dirname(__file__)
movies_file = os.path.join(dirname, 'MovieLens_m1/movies.dat')
ratings_file = os.path.join(dirname, 'MovieLens_m1/ratings.dat')

#a,b=load_data_movies(movies_file)
c,d=load_data_ratings(ratings_file)

# print(a)
# print(b)
print(c)
print(d)