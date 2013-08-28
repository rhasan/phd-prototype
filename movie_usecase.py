import web
from datasets import MovieLens

from index import Index
from login import Login
from home import Home
from profile import Profile
from explain import Explain
from logout import Logout
from movie_recommender import MovieRecommender



urls = (
    '/', 'Index',
    '/login','Login',
    '/logout','Logout',
    '/home','Home',
    '/profile','Profile',
    '/explain','Explain'
)

ml = MovieLens.Instance()
recsys = MovieRecommender.Instance()


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
