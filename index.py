import web
from request_handler import RequestHandler

class Index(RequestHandler):
    
    def GET(self):
        if self.user:
            (user_id,age,gender,occupation,zip_code) = self.user
            web.redirect('/home')
        else:
            web.redirect('/login')
        
