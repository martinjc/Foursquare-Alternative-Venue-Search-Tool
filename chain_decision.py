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

from Levenshtein import ratio
from venue_searcher import VenueSearcher


def is_chain(venue_id):

    vs = VenueSearcher()

    venue_data = vs.get_venue_json(venue_id)

    if vs.venue_has_chain_property(venue_data):
        return True

    global_venues = vs.global_search(venue_data['name'])

    global_similar_name_count = len(filter(lambda x: ratio(x, venue_data['name']) > 0.95, [venue['name'] for venue in global_venues]))

    if len(global_venues) > 1 and global_similar_name_count > 0:
        global_proportion = float(len(global_venues))/global_similar_name_count
    else:
        global_proportion = 0

    local_venues = vs.local_search(venue_data, venue_data['name'], 5000)
    local_similar_name_count = len(filter(lambda x: ratio(x, venue_data['name']) > 0.95, [venue['name'] for venue in local_venues]))

    if len(local_venues) > 1 and local_similar_name_count > 0:
        local_proportion = float(len(local_venues))/local_similar_name_count
    else: 
        local_proportion = 0

    if global_proportion > 0.9 or local_proportion > 0.9:
        return True
    else:
        return False



if __name__ == "__main__":

    starbucks1 = '4b4ef4dbf964a520a4f726e3'
    northcliffe = '5030ef53e4b0beacbee84cef'
    starbucks2 = '5315d2d211d2c227cf2a7037'
    mcdonalds = '4c41df47520fa5933a41caac'
    tesco = '4c14b6aea1010f479fd94c18'

    print is_chain(mcdonalds)



