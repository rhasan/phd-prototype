import web
from request_handler import RequestHandler
from web import form
from datasets import MovieLens


ml = MovieLens.Instance()

class Login(RequestHandler):

    #def __init__(self):
    #    RequestHandler.__init__(self)


    def GET(self):

        if self.user:
            web.redirect('/home')
        else:
       
            return self.render('login.html')

    def POST(self):
        
        inp = web.input()
        username =  inp.username
        password = inp.password
        
        
        if not ml.is_valid_user(username):
            return self.render('login.html', error = 'Invalid login')
        else:
            self.login(username)
            web.redirect('/home')
