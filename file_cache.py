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

import os
import time
import json
from datetime import timedelta, datetime


class JSONFileCache(object):

    def __init__(self, refresh_time=timedelta(days=1)):

        cwd_dir = os.getcwd()

        # directory for plots
        self.cache_dir = os.path.join(cwd_dir, 'cache')
        if not os.path.isdir(self.cache_dir):
            os.makedirs(self.cache_dir)

        self.refresh_time = refresh_time

    def file_exists(self, file_id):

        requested = os.path.join(self.cache_dir, file_id)

        if os.path.isfile(requested):

            refresh_time = datetime.now() - self.refresh_time
            time_modified = datetime.fromtimestamp(os.path.getmtime(requested))

            if time_modified < refresh_time:
                return False
            else:
                return True
        else:
            return False


    def get_json(self, file_id):
        assert self.file_exists(file_id)

        with open(os.path.join(self.cache_dir, file_id), 'r') as infile:
            return json.load(infile)


    def put_json(self, json_data, file_id):

        with open(os.path.join(self.cache_dir, file_id), 'w') as outfile:
            json.dump(json_data, outfile)

