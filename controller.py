import web
from datasets import MovieLens

from index import Index
from login import Login



urls = (
    '/', 'Index',
    '/login','Login'
)

ml = MovieLens.Instance()


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
