#import web
from datasets import MovieLens

class RequestHandler:
    def __init__(self):
        movielens_dataset = MovieLens.Instance()
        uid = '122' #get this from cookies
        #uid = None
        self.user =  uid and movielens_dataset.user_by_id(uid)
        #self.user = "102"

    def GET(self):
        #self.user='200'
        pass

    