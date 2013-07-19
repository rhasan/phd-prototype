import web
from request_handler import RequestHandler

class Profile(RequestHandler):
    
    def GET(self):
        if self.user:
            (user_id,age,gender,occupation,zip_code) = self.user
            return self.render('profile.html', username = user_id)
        else:
            web.redirect('/login')
        