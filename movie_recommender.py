from datasets import MovieLens


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
