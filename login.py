import web
from request_handler import RequestHandler
from web import form
from datasets import MovieLens



ml = MovieLens.Instance()

class Login(RequestHandler):

    #def __init__(self):
    #    RequestHandler.__init__(self)


    def GET(self):
        referer = web.ctx.env.get('HTTP_REFERER','')
        redirect = referer if referer else '/home'
        self.set_secure_cookie('lr-url', str(redirect))
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
            lr_url = self.read_secure_cookie('lr-url')
            redirect_url = str(lr_url) if lr_url else '/home'             
            self.login(username)
            web.redirect(redirect_url)
