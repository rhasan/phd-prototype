import web
from request_handler import RequestHandler
from datasets import MovieLens

ml = MovieLens.Instance()

class Profile(RequestHandler):
    
    def GET(self):
        if self.user:
            (user_id,age,gender,occupation,zip_code) = self.user
            rated_movies = ml.get_user_rating_data(user_id)
            avg_rating = ml.get_avg_user_rating(user_id)            
            return self.render('profile.html', username = user_id, rated_movies = rated_movies, avg_rating = avg_rating)
        else:
            web.redirect('/login')
        