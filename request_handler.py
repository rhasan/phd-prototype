import web
from datasets import MovieLens
import util

ml = MovieLens.Instance()


class RequestHandler:

    def login(self,user_id):
        #web.setcookie('user_id', user_id)
        self.set_secure_cookie('user_id', user_id)
    
    def set_secure_cookie(self, name, val):
        cookie_val = util.make_secure_val(val)
        web.setcookie(name, cookie_val)
        #self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/' % (name, cookie_val))
    
    def read_secure_cookie(self, name):
        cookie_val = web.cookies().get(name)
        return cookie_val and util.check_secure_val(cookie_val)
    
    def logout(self):
        web.setcookie('user_id','')
    
    def __init__(self):
        uid =  self.read_secure_cookie('user_id')
        #uid = None
        web.debug("user_id")
        web.debug(uid)
        self.user =  uid and ml.user_by_id(uid)

        #self.user = "102"

    def GET(self):
        #self.user='200'
        pass

    