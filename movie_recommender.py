import util
from datasets import MovieLens
from SPARQLWrapper import SPARQLWrapper, JSON

DBPEDIA_ENDPOINT = "http://dbpedia-test.inria.fr/sparql"


class MovieRecommender:
    def __init__(self):
        pass

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
        LIMIT 20
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


def main():
    ml = MovieLens()
    ml.load_data()
    recsys = MovieRecommender()
    #print ml.get_DBpedia_mapped_movie_list()
    #print ml.get_avg_movie_rating_by_dbpedia_uri('http://dbpedia.org/resource/Roman_Holiday')
    #print ml.get_avg_movie_rating_by_dbpedia_uri('http://dbpedia.org/resource/Wag_the_Dog')
    r_list = recsys.get_movie_recommendations('http://dbpedia.org/resource/Wag_the_Dog')

    for (movie_uri,confidence) in r_list:
        print util.url_decode(movie_uri), confidence

    #print ml.get_user_rating_data('122')
    #print

if __name__ == "__main__":
    main()
