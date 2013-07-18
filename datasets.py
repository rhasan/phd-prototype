import csv
import util
import numpy as np

from collections import defaultdict
from patterns import Singleton

DBP_ML_MAPPING = "data/mapping-movielens-dbpedia.csv"
ML_ITEM_RATING = "data/ml-100k/u.data"
ML_USER_DEMO = "data/ml-100k/u.user"

MAX_RATING = 5

#work on making a singletone

@Singleton
class MovieLens:
    def __init__(self):
        self.ml_to_dbp = dict()
        self.dbp_to_ml = dict()
        self.user_rating_data = defaultdict(lambda: list())
        self.item_rating_data = defaultdict(lambda: np.zeros(MAX_RATING+1))
        self.user_demographic = dict()

        self.load_data()
    

    """
    loads DBpedia movie URI and MovieLens movie id mapping
    """ 
    def load_dbpedia_mapping(self,file_path):
        
        try:
            f = open(file_path,'rb')
            reader = csv.reader(f)
            rownum = 0
            for row in reader:
                if rownum == 0:
                    header = row
                else:
                    # colnum = 0
                    # for col in row:
                    #   print '%s: %s' % (header[colnum], col)
                    #   colnum += 1
                    #print "row:",row[0], util.url_decode(row[1])
                    ml_id = row[0]
                    #dbp_uri = util.url_decode(row[1])
                    dbp_uri = row[1]
                    self.ml_to_dbp[ml_id] = dbp_uri
                    self.dbp_to_ml[dbp_uri] = ml_id
                rownum += 1
        finally:
            f.close()

    """
    loads movie lens movie rating data
    """
    def load_movielens_rating_data(self,file_path):
        
        try:
            f = open(file_path,'rb')
            #reader = csv.reader(f)
            for line in f:
                row = line.split()
                #print row
                user_id = row[0]
                movie_id = row[1]
                #work with only the movies that have dbpedia mapping
                if self.has_DBpedia_mapping(movie_id) == False:
                    continue

                rating = int(row[2])

                #rating_data = dict()
                #rating_data['movie_id'] = movie_id
                #rating_data['rating'] = rating
                dbp_uri = self.get_DBpedia_movie_URI(movie_id)
                rating_data = (dbp_uri,rating,movie_id)
                
                self.user_rating_data[user_id].append(rating_data)

                rating_vector = np.zeros(MAX_RATING+1)
                rating_vector[rating] = 1;

                self.item_rating_data[movie_id] += rating_vector

        finally:
            f.close()

    """
    loads movie lens user demographic
    """
    def load_movielens_user_demographics(self,file_path):
        try:
            f = open(file_path,'rb')
            for line in f:
                row = line.split('|')
                #print row
                user_id = row[0]
                age = row[1]
                gender = row[2]
                occupation = row[3]
                zip_code = row[4]

                self.user_demographic[user_id]=(user_id,age,gender,occupation,zip_code)
        finally:
            f.close()
    """
    get a user by user id
    """
    def user_by_id(self,user_id):
        if self.user_demographic.has_key(user_id):
            return self.user_demographic[user_id]
        return None

    """
    checks if the given user is a valid user
    """
    def is_valid_user(self,user_id):
        return self.user_demographic.has_key(user_id)

    """
    Takes a DBpedia movie URI as parameter
    returns a tuple of average rating and the number of people rated the movie
    """
    def get_avg_movie_rating_by_dbpedia_uri(self, dbp_uri):
        movie_id = self.dbp_to_ml[dbp_uri]
        return self.get_avg_item_rating(movie_id)

    """
    Takes a MovieLens movie id as parameter
    returns a tuple of average rating, the number of people rated the movie, 
    and a rating vector with rating counts
    """
    def get_avg_item_rating(self,movie_id):
        rating_vector = self.item_rating_data[movie_id]
        
        rating_sum = 0
        count = 0
        rating = 0
        for r_count in rating_vector:
            rating_sum += (r_count*rating)
            count += r_count
            rating += 1

        avg_rating = rating_sum/count
        return (avg_rating,count,rating_vector.tolist())


    """
    Get the list DBpedia URIs that were mapped to MovieLens movie ids
    """
    def get_DBpedia_mapped_movie_list(self):
        return self.ml_to_dbp.values()

    """
    Returns the list of movies that a give user has rated.
    Each element in the list is a tuple with DBpedia URI, rating (int), and MovieLens movie id (string).
    The parameter user_id must be string
    """
    def get_user_rating_data(self,user_id):

        data = self.user_rating_data[user_id]
        return sorted(data, key=lambda tup: tup[1],reverse=True)

    def get_avg_user_rating(self,user_id):
        data = self.get_user_rating_data(user_id)
        rating_sum = 0.0
        for (dbp_m_id,r,ml_m_id) in data:
            rating_sum += r
        return rating_sum/len(data)


    """
    Returns the DBpedia URI for a MovieLens movie id
    """
    def  get_DBpedia_movie_URI(self,movie_id):
        return self.ml_to_dbp[movie_id]
    """
    Returns the MovieLens movie id for a DBpedia URI
    """
    def get_MovieLens_movie_id(self,DBpedia_uri):
        return self.dbp_to_ml[DBpedia_uri]


    def has_DBpedia_mapping(self,movie_id):
        return self.ml_to_dbp.has_key(movie_id)

    """
    Loads all the data files
    """
    def load_data(self):
        #DBpedia mapping must be loaded first
        self.load_dbpedia_mapping(DBP_ML_MAPPING)
        self.load_movielens_rating_data(ML_ITEM_RATING)
        self.load_movielens_user_demographics(ML_USER_DEMO)
        

