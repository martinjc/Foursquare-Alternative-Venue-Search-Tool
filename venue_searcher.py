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
from datetime import timedelta
from file_cache import JSONFileCache
from api import APIGateway, APIWrapper


class VenueSearcher:

    def __init__(self):
        
        self.gateway = APIGateway(access_token, 500, [client_id, client_secret], 5000)
        self.wrapper = APIWrapper(self.gateway)

        self.params = {
            'v' : 20140713
        }

        self.cache = JSONFileCache(timedelta(days=1))


    def venue_has_chain_property(self, venue):
        if venue.get('page', None) is not None:
            if venue['page'].get('user', None) is not None:
                if venue['page']['user'].get('type', None) is not None:
                    return venue['page']['user']['type'] == 'chain'
        return False


    def global_search(self, query):

        params = {}
        params['v'] = self.params['v']
        params['intent'] = 'global'
        params['limit'] = 50
        params['query'] = query

        if self.cache.file_exists('%s_global.json' % (query.replace('/', ''))):
            results = self.cache.get_json('%s_global.json' % (query.replace('/', '')))
            return results['response']['venues']
        else:
            try:
                results = self.wrapper.query_routine('venues', 'search', params, True)
                if not results is None:
                    self.cache.put_json(results, '%s_global.json' % (query.replace('/', '')))
                return results['response']['venues']
            except urllib2.HTTPError, e:
                pass
            except urllib2.URLError, e:
                pass


    def local_search(self, venue, query, radius):

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
        params['query'] = query

        if self.cache.file_exists('%s,%s,%s.json' % (query, params['ll'], radius)):
            results = self.cache.get_json('%s,%s,%s.json' % (query, params['ll'], radius))
            return results['response']['venues']
        else:
            try:
                results = self.wrapper.query_routine('venues', 'search', params, True)
                if not results is None:
                    self.cache.put_json(results, '%s,%s,%s.json' % (query, params['ll'], radius))
                return results['response']['venues']
            except urllib2.HTTPError, e:
                pass
            except urllib2.URLError, e:
                pass


    def get_venue_json(self, venue_id):

        if self.cache.file_exists('%s.json' % (venue_id)):
            response = self.cache.get_json('%s.json' % (venue_id))
        else:
            try:
                response = self.wrapper.query_resource('venues', venue_id, get_params=self.params, userless=True)
            except urllib2.HTTPError, e:
                pass
            except urllib2.URLError, e:
                pass
            if not response is None:
                self.cache.put_json(response, '%s.json' % (venue_id))
        
        return response['response']['venue']


    def search_alternates(self, venue, radius=500):

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

        if self.cache.file_exists('%s,%s,%s,alternates.json' % (params['ll'], categories, radius)):
            alternatives = self.cache.get_json('%s,%s,%s,alternates.json' % (params['ll'], categories, radius))
            return alternatives['response']['venues']
        else:
            try:
                alternatives = self.wrapper.query_routine('venues', 'search', params, True)
                if not alternatives is None:
                    self.cache.put_json(alternatives, '%s,%s,%s,alternates.json' % (params['ll'], categories, radius))
                return alternatives['response']['venues']
            except urllib2.HTTPError, e:
                pass
            except urllib2.URLError, e:
                pass   


if __name__ == "__main__":

    starbucks1 = '4b4ef4dbf964a520a4f726e3'
    northcliffe = '5030ef53e4b0beacbee84cef'
    starbucks2 = '5315d2d211d2c227cf2a7037'
    mcdonalds = '4c41df47520fa5933a41caac'
    tesco = '4c14b6aea1010f479fd94c18'

    vs = VenueSearcher()

    venue_data = vs.get_venue_json(mcdonalds)
    alternates = vs.search_alternates(venue_data, 5000)

    print venue_data['name']

    official_chain = vs.venue_has_chain_property(venue_data)

    print official_chain

    global_name = vs.global_search(venue_data['name'])

    print len(global_name)

    for alternate in global_name:
        print alternate['name']

    local_search_10000 = vs.local_search(venue_data, venue_data['name'], 10000)

    print len(local_search_10000)

    for alternate in local_search_10000:
        print alternate['name']

    local_search_100000 = vs.local_search(venue_data, venue_data['name'], 100000)

    print len(local_search_100000)

    for alternate in local_search_100000:
        print alternate['name']

