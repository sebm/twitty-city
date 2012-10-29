from datetime import datetime

import webapp2
from AnalysesHandler import *


class AnalysisHistoryHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers["Content-Type"] = "text/plain"

        a = AnalysesHandler()

        analyses = a.getGDataForAnalyses(a.getDaysOfAnalysisForPlace('Bristol', 7)) + \
            a.getGDataForAnalyses(a.getDaysOfAnalysisForPlace('York', 7)) + \
            a.getGDataForAnalyses(a.getDaysOfAnalysisForPlace('London', 7)) + \
            a.getGDataForAnalyses(a.getDaysOfAnalysisForPlace('Margate', 7)) + \
            a.getGDataForAnalyses(a.getDaysOfAnalysisForPlace('Oxford', 7))

        gdata = AnalysisGData(created_at=datetime.now(), gdatas=analyses)
        gdata.put()

        self.response.out.write("Wrote: \n %s \n to db." % analyses)
