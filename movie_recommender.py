from datasets import MovieLens

DBP_ML_MAPPING = "data/mapping-movielens-dbpedia.csv"

def main():
	ml = MovieLens()
	ml.load_dbpedia_mapping(DBP_ML_MAPPING)

if __name__ == "__main__":
	main()
