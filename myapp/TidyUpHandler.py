import os
from datetime import datetime, timedelta
import logging
import time
import csv 
import urllib

from email.utils import parsedate_tz, mktime_tz
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from django.utils import simplejson as json
from models import *

class TidyUpHandler(webapp.RequestHandler):
  def get(self):
    one_month_ago = datetime.now() + timedelta(days=-30)

    old_tweets = Tweet.gql('WHERE created_at < :before LIMIT 100', before=one_month_ago )
    for t in old_tweets:
      t.delete()

    old_analyses = Analysis.gql('WHERE created_at < :before LIMIT 100', before=one_month_ago )
    for a in old_analyses:
      a.delete()

    old_gdatas = AnalysisGData.gql('WHERE created_at < :before LIMIT 100', before=one_month_ago )
    for g in old_gdatas:
      g.delete()
      