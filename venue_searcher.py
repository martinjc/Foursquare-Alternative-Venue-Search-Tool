#!/usr/bin/env python
#
# Copyright 2014 Martin J Chorley
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import urllib2

from _credentials import *
from api import APIGateway, APIWrapper

class VenueSearcher:

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

    def search_for_alternates(self, venue, radius=500):

        lat = venue['location']['lat']
        lng = venue['location']['lng']

        categories = ','.join(str(category['id']) for category in venue['categories'])

        params = {}
        params['v'] = self.params['v']
        params['ll'] = '%f,%f' % (lat, lng)
        params['intent'] = 'browse'
        params['radius'] = radius
        params['limit'] = 50
        params['categoryId'] = categories

        try:
            alternatives = self.wrapper.query_routine("venues", "search", params, True)
            return alternatives['response']['venues']
        except urllib2.HTTPError, e:
            pass
        except urllib2.URLError, e:
            pass   


if __name__ == "__main__":

    venueid = "4b978a27f964a520f20735e3"
    alt_searcher = VenueSearcher()
    venue_data = alt_searcher.search_for_venue(venueid)
    print venue_data['name']
    alternates = alt_searcher.search_for_alternates(venue_data, 1000)
    for alternate in alternates:
        print alternate['name']



