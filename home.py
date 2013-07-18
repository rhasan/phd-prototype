import web
from request_handler import RequestHandler

render = web.template.render('templates/')

class Home(RequestHandler):
    
    def GET(self):
        if self.user:
            (user_id,age,gender,occupation,zip_code) = self.user
            return render.home(user_id)
        else:
            web.redirect('/login')
