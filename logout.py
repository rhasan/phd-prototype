import web
from request_handler import RequestHandler
from movie_recommender import MovieRecommender

class Logout(RequestHandler):
    def GET(self):
        self.logout()
        recsys = MovieRecommender.Instance()
        recsys.reinit()

        
        referer = web.ctx.env.get('HTTP_REFERER')
        print "Referer:", referer
        redirect = referer if referer else '/home'
        web.redirect(redirect)
