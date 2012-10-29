import os
from datetime import datetime, timedelta
import logging
import time
import csv
import urllib
import sys

from email.utils import parsedate_tz, mktime_tz
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from models import *
from AnalysesHandler import *


class AnalysisHistoryHandler(webapp.RequestHandler):
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
