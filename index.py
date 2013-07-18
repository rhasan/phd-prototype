from request_handler import RequestHandler

class Index(RequestHandler):
    
    def GET(self):
        if self.user:
            (user_id,age,gender,occupation,zip_code) = self.user
        else:
            user_id = "no user found"
        return "Hello, world! " + user_id
