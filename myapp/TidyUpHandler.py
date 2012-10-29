from datetime import datetime, timedelta
import webapp2
from models import Tweet, Analysis, AnalysisGData


class TidyUpHandler(webapp2.RequestHandler):
    def get(self):
        datatype = self.request.get('datatype')
        fortnight_ago = datetime.now() + timedelta(days=-14)
        counter = 0
        self.response.out.write(
            "Looking to delete stuff from before " + str(fortnight_ago) + "<br>"
        )

        if datatype == "tweet":
            old_tweets = Tweet.gql(
                'WHERE created_at < :before LIMIT 1000', before=fortnight_ago)
            for t in old_tweets:
                t.delete()
                counter += 1

        elif datatype == "analysis":
            old_analyses = Analysis.gql(
                'WHERE created_at < :before LIMIT 1000', before=fortnight_ago)
            for a in old_analyses:
                a.delete()
                counter += 1

        elif datatype == "gdata":
            old_gdatas = AnalysisGData.gql(
                'WHERE created_at < :before LIMIT 50', before=fortnight_ago)
            for g in old_gdatas:
                g.delete()
                counter += 1

        else:
            self.response.out.write("Please say what datatype you'd like to tidy up. ")

        self.response.out.write(str(counter) + " items deleted")
