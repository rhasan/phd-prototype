
import util


from datasets import MovieLens
from SPARQLWrapper import SPARQLWrapper, JSON
from collections import defaultdict
from patterns import Singleton


DBPEDIA_ENDPOINT = "http://dbpedia-test.inria.fr/sparql"
#DBPEDIA_ENDPOINT = "http://dbpedia.org/sparql";
INIT_USER_K = 10
INIT_ITEM_K = 20

@Singleton
class MovieRecommender:
    def __init__(self):
        
        self.ml = MovieLens.Instance()
        self.rated_movies = list()
        self.reco_list = list()
        #self.ml.load_data()
    """
    Returns a list of similar movies based on the number of common dcterms:subject counts.
    Each entry in the list of recommendation is a tuple. Each tuple has the (movie URI, confidence score).
    Confidence score values range from 0.0 to 1.0. The value 0.0 means not similar at all and the value 1.0
    means completly similar.
    """
    def get_movie_recommendations(self,dbpedia_uri):

        sparql = SPARQLWrapper(DBPEDIA_ENDPOINT)
        queryStr = """
        SELECT ?m count(?m) AS ?num
        WHERE
        {
            <"""+dbpedia_uri+"""> dcterms:subject ?o.
            ?m dcterms:subject ?o.
            ?m a dbpedia-owl:Film.
            #FILTER (?m != <"""+dbpedia_uri+""">)

        }

        GROUP BY ?m ORDER BY DESC(?num)
        LIMIT """+str(INIT_ITEM_K)+"""
        """;
        sparql.setQuery(queryStr)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        max_score = 0.0
        movie_score = 0.0
        for result in results["results"]["bindings"]:
            res_score = float(result["num"]["value"])
            if result["m"]["value"] == dbpedia_uri:
                movie_score = res_score
            #for unusual cases to handle divide by zero
            if max_score < res_score:
                max_score = res_score

        #for unusual cases to handle divide by zero
        if movie_score == 0.0:
            normalizer = max_score
        else:
            normalizer = movie_score
        reco_list = list()
        for result in results["results"]["bindings"]:
            if result["m"]["value"] == dbpedia_uri:
                continue
            r_movie_uri = result["m"]["value"]
            r_movie_con = float(result["num"]["value"])/normalizer
            m_entry = (r_movie_uri,r_movie_con)
            reco_list.append(m_entry)
        return reco_list

    """
    Returns a list of recommended movies for a MovieLens user specified by ml_user_id.
    The recommendation is computed based on the movies the user rated. The recommendations 
    are the movies that are similar to the movies with rating greater than on equals to the 
    average rating by the user. Computes similar movies for maximum INIT_USER_K rated movies.
    The return value is a tuple of lists. The first list in the tuple are the list of movies 
    rated by the user and has the structure (DBpedia URI, rating (int), and MovieLens movie id (string)).
    The second list is the list of recommendations and has the structure (recommended movie URI, confidence score, recommended from rated movie URI)
    """

    def recommendation_for_user(self,ml_user_id):


        #print len(self.rated_movies), len(self.reco_list)
        if len(self.rated_movies)>0 and len(self.reco_list)>0:
            return (self.rated_movies, self.reco_list)

        print "user:", ml_user_id, " likes"

        rated_movies = self.ml.get_user_rating_data(ml_user_id)
        avg_rating = self.ml.get_avg_user_rating(ml_user_id)
        
        all_reco_dict = defaultdict(lambda: 0.0)
        count = 0
        for (dbp_id,rating,ml_id) in rated_movies:

            rating_f = float(rating)
            #movies that the user likes
            if rating_f >= avg_rating and rating_f>0:
                #print "finding recommendations for", util.url_unquote(dbp_id)
                print dbp_id
                m_reco_list = self.get_movie_recommendations(dbp_id)
                #all_reco_list.extend(m_reco_list)
                for m_entry in m_reco_list:
                    (r_dbp_uri,r_confidence) = m_entry
                    # to make sure that maximum confidence score recommendation is considered
                    # if a movie is recommended more than onece 
                    if all_reco_dict[r_dbp_uri] < r_confidence:
                        #all_reco_dict[r_dbp_uri] = m_entry
                        #dbp_id is included as an explanation
                        all_reco_dict[r_dbp_uri] = (r_dbp_uri,r_confidence,dbp_id)

            if count > INIT_USER_K:
                break
            count += 1
        
        all_reco_list = all_reco_dict.values()


        all_reco_list =  sorted(all_reco_list, key=lambda tup: tup[1],reverse=True)
        self.rated_movies=rated_movies
        self.reco_list=all_reco_list

        return (rated_movies,all_reco_list)
    
    """
    Explains a recommendation by querying DBpedia.
    Returns a tuple with (common topic URI list, liked movie rating from which the recommendation is generated)
    """
    def explain_recommendation(self,user_id,recommended_movie_dbp_id,liked_movie_dbp_id):
        
        liked_movie_rating = 0;
        rated_movies = self.ml.get_user_rating_data(user_id)
        for (dbp_id,rating,ml_id) in rated_movies:
            if liked_movie_dbp_id == dbp_id:
                liked_movie_rating = rating
                break;

        explanationQueryStr = """
        SELECT ?o
        WHERE
        {
            <"""+recommended_movie_dbp_id+"""> dcterms:subject ?o.
            <"""+liked_movie_dbp_id+"""> dcterms:subject ?o.

        }
        """
        sparql = SPARQLWrapper(DBPEDIA_ENDPOINT)
        sparql.setQuery(explanationQueryStr)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        common_topic_uri_list = list()
        for result in results["results"]["bindings"]:
            common_topic_uri = result["o"]["value"]
            common_topic_uri_list.append(common_topic_uri)
        return (common_topic_uri_list,liked_movie_rating)

    def reinit(self):
        self.rated_movies = []
        self.reco_list = []

def main():

    recsys = MovieRecommender().Instance()
    #print ml.get_DBpedia_mapped_movie_list()
    #print ml.get_avg_movie_rating_by_dbpedia_uri('http://dbpedia.org/resource/Roman_Holiday')
    #print ml.get_avg_movie_rating_by_dbpedia_uri('http://dbpedia.org/resource/Wag_the_Dog')
    #r_list = recsys.get_movie_recommendations('http://dbpedia.org/resource/Wag_the_Dog')

    user_id = '100'
    (rated_movies,r_list) = recsys.recommendation_for_user(user_id)
    #print r_list
    print "Recommedations for the user:", user_id
    for (movie_uri,confidence,dbp_id) in r_list:
        try:
            #print movie_uri, confidence, "|explanation:",dbp_id
        
            print util.url_unquote(movie_uri), confidence, "|explanation:",util.url_unquote(dbp_id)
        except Exception, e:
            print "----------ERROR--------"
            print movie_uri, dbp_id
            break
        



    #print ml.get_user_rating_data('122')
    #print ml.get_avg_user_rating('122')
    #print

if __name__ == "__main__":
    main()
