import web
from request_handler import RequestHandler
from movie_recommender import MovieRecommender
import navigation

class Home(RequestHandler):
    
    def GET(self):
        if self.user:
            recsys = MovieRecommender.Instance()
            (user_id,age,gender,occupation,zip_code) = self.user
            #return render.home(user_id)
            (rated_movies,r_list) = recsys.recommendation_for_user(user_id)
            navigation_links = navigation.get_login_navigation(self.user)
            return self.render('home.html',login_area_links=navigation_links, username = user_id,recommendations=r_list)
        else:
            web.redirect('/login')
    
