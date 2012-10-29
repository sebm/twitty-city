import sys

from email.utils import parsedate_tz, mktime_tz
from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from models import *
from jinja2 import Environment, FileSystemLoader

from AnalysesHandler import *


class IndexHandler(webapp.RequestHandler):
    def get(self):
        a = AnalysesHandler()

        analyses_gdata = AnalysisGData.gql("ORDER BY created_at DESC LIMIT 0,1")

        template_values = {
            'gdata': analyses_gdata[0].gdatas,
            'BristolSentiment': "%.2f" % a.getAnalysisForPlace('Bristol'),
            'OxfordSentiment': "%.2f" % a.getAnalysisForPlace('Oxford'),
            'LondonSentiment': "%.2f" % a.getAnalysisForPlace('London'),
            'YorkSentiment': "%.2f" % a.getAnalysisForPlace('York'),
            'MargateSentiment': "%.2f" % a.getAnalysisForPlace('Margate'),
            'BristolImg': a.getImageForScore(a.getAnalysisForPlace('Bristol')),
            'OxfordImg': a.getImageForScore(a.getAnalysisForPlace('Oxford')),
            'LondonImg': a.getImageForScore(a.getAnalysisForPlace('London')),
            'YorkImg': a.getImageForScore(a.getAnalysisForPlace('York')),
            'MargateImg': a.getImageForScore(a.getAnalysisForPlace('Margate')),
            'sitename': "Twitty City"
        }
        loader = FileSystemLoader(os.path.dirname(__file__) + '/../templates/')
        env = Environment(loader=loader)

        template = env.get_template('index.html')

        self.response.out.write(template.render(template_values))
