from datasets import MovieLens

ml = MovieLens.Instance()
print not ml.is_valid_user('123')