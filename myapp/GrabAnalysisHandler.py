import webapp2
from AnalysesHandler import *


class GrabAnalysisHandler(webapp2.RequestHandler):
    def get(self):
        a = AnalysesHandler()

        self.response.headers["Content-Type"] = "text/plain"
        myplace = self.request.get('place')
        a.runAnalysisForPlace(myplace, self.response)
