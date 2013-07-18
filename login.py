import web
from request_handler import RequestHandler
from web import form
from datasets import MovieLens

render = web.template.render('templates/')
ml = MovieLens.Instance()

login_form = form.Form(
            form.Textbox('username',
                form.notnull,
                form.Validator('Must be more than 3', lambda x:int(x)>3)),
            form.Password('password'),
        )

class Login(RequestHandler):

    #def __init__(self):
    #    RequestHandler.__init__(self)


    def GET(self):

        if self.user:
            web.redirect('/home')
            return

        f = login_form()
       
        return render.login(f)

    def POST(self):
        f = login_form()

        if not f.validates():
            return render.login(f)

        username = f['username'].value
        password = f['password'].value
        
        #web.debug(type(username))
        #web.debug(username)
        
        if not ml.is_valid_user(username):
            return render.login(f)
        else:
            user = ml.user_by_id(username)
            self.login(username)
            web.redirect('/home')
