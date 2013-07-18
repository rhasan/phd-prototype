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
			FILTER (?m != <http://dbpedia.org/resource/Catch_Me_If_You_Can>)

		}

		GROUP BY ?m ORDER BY DESC(?num)
		LIMIT 50
		""";
		sparql.setQuery(queryStr)
		sparql.setReturnFormat(JSON)
		results = sparql.query().convert()

		for result in results["results"]["bindings"]:
		    print util.url_decode(result["m"]["value"]), result["num"]["value"]
		    #print result["m"]["value"], result["num"]["value"]




def main():
	ml = MovieLens()
	ml.load_data()
	#print ml.get_DBpedia_mapped_movie_list()
	print ml.get_avg_movie_rating_by_dbpedia_uri('http://dbpedia.org/resource/Roman_Holiday')
	print ml.get_avg_movie_rating_by_dbpedia_uri('http://dbpedia.org/resource/Wag_the_Dog')

	print ml.get_user_rating_data('122')
	#print

if __name__ == "__main__":
	main()
