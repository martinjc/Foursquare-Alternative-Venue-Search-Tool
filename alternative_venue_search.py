import urllib2

from _credentials import *
from api import APIGateway, APIWrapper

class AlternativeSearcher:

    def __init__(self):
        
        self.gateway = APIGateway(access_token, 500, [client_id, client_secret], 5000)
        self.wrapper = APIWrapper(self.gateway)

        self.params = {
            'v' : 20140713
        }

    def search_for_venue(self, venue_id):
        try:
            response = self.wrapper.query_resource("venues", venueid, get_params=self.params, userless=True)
            return response['response']['venue']
        except urllib2.HTTPError, e:
            pass
        except urllib2.URLError, e:
            pass

    def search_for_alternates(self, venue, range):

        lat = venue['location']['lat']
        lng = venue['location']['lng']



if __name__ == "__main__":

    venueid = "4b978a27f964a520f20735e3"
    alt_searcher = AlternativeSearcher()
    venue_data = alt_searcher.search_for_venue(venueid)



