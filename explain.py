import web
from request_handler import RequestHandler
from movie_recommender import MovieRecommender
import util
#import urllib
class Explain(RequestHandler):
    
    def GET(self):
        if self.user:
            recsys = MovieRecommender.Instance()
            (user_id,age,gender,occupation,zip_code) = self.user
            user_data = web.input()
            reco_movie_id = user_data.r
            liked_movie_id = user_data.m
            print reco_movie_id, liked_movie_id
            #print "before url_unquote:", reco_movie_id, liked_movie_id
            #alread unquoted by web.py
            #reco_movie_id = util.url_unquote(reco_movie_id)
            #liked_movie_id = util.url_unquote(liked_movie_id)
            #print "after url_unquote:", reco_movie_id, liked_movie_id
            (common_topic_uri_list,liked_movie_rating) = recsys.explain_recommendation(user_id,reco_movie_id,liked_movie_id)

            #explanation = "explanation is here for "+reco_movie_id + " and " + liked_movie_id
            return self.render('explain.html', common_topic_uri_list=common_topic_uri_list,recommended_movie_id=reco_movie_id,liked_movie_id=liked_movie_id,liked_movie_rating=liked_movie_rating)
        else:
            web.redirect('/login')
        
