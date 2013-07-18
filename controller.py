import web
from datasets import MovieLens

from index import Index
from login import Login
from home import Home



urls = (
    '/', 'Index',
    '/login','Login',
    '/home','Home'
)

ml = MovieLens.Instance()


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
