from load_data import load_data
import os

dirname = os.path.dirname(__file__)
movies_file = os.path.join(dirname, 'MovieLens_m1/movies.dat')
ratings_file = os.path.join(dirname, 'MovieLens_m1/ratings.dat')

# a,b,c=load_data_movies(movies_file)
# d,e,f=load_data_ratings(ratings_file)
a,b,c,d = load_data(movies_file, ratings_file)
# print(a)
# print(b)
print(c)
print(d)