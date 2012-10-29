import webapp2
from google.appengine.api import urlfetch
import json
from models import Tweet
from email.utils import parsedate_tz, mktime_tz
from datetime import datetime


class GrabTweetsHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers["Content-Type"] = "text/plain"

        myplace = self.request.get('place')

        urlbase = 'http://search.twitter.com/search.json'
        if myplace == 'Oxford':
            search_url = urlbase + '?geocode=51.751944%2C-1.257778%2C10km'
        elif myplace == 'London':
            search_url = urlbase + '?geocode=51.511676%2C-0.133209%2C10km'
        elif myplace == 'York':
            search_url = urlbase + '?geocode=53.958333%2C-1.080278%2C10km'
        elif myplace == 'Margate':
            search_url = urlbase + '?geocode=51.382681%2C1.3664245%2C10km'
        elif myplace == 'Bristol':
            search_url = urlbase + '?geocode=51.45%2C-2.583333%2C10km'
        else:
            self.response.out.write(("Please provide a 'place' parameter:"
                                     "Oxford, London, York, Bristol or Margate."))

        self.response.out.write('About to access: %s\n\n' % search_url)
        f = urlfetch.fetch(url=search_url)

        if f.status_code == 200:
            j = json.loads(f.content)
            for result in j['results']:
                self.response.out.write(result)
                self.response.out.write('\n')
                if (result['id']):
                    same_id = Tweet.gql('WHERE tweet_id = :1', result['id'])

                    if (same_id.count() > 0):
                        self.response.out.write('Tweet id #%s exists in the datastore\n'
                                                % result['id'])
                    else:
                        self.response.out.write('Adding tweet id #%s to datastore\n'
                                                % result['id'])
                        created_at = datetime.fromtimestamp(
                            mktime_tz(parsedate_tz(result['created_at'])))
                        tweet = Tweet(
                            tweet_id=result['id'],
                            tweet_content=result['text'],
                            place=myplace,
                            created_at=created_at
                        )

                        tweet.put()

        elif f.status_code == 400:
            self.response.out.write('UHOH! You have hit the rate limit...')
