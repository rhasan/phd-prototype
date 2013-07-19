import web
from request_handler import RequestHandler

class Home(RequestHandler):
    
    def GET(self):
        if self.user:
            (user_id,age,gender,occupation,zip_code) = self.user
            #return render.home(user_id)
            return self.render('home.html', username = user_id)
        else:
            web.redirect('/login')
