# Copyright 2014 The University of Edinburgh
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#from django.http import HttpRequest

# REST_PREFIX = 'rest'
REST_PREFIX = ''


def get_base_rest_uri(request):
    protocol = request.is_secure() and 'https' or 'http'
    host = request.get_host()
    return protocol + '://' + host + REST_PREFIX + '/'


def extract_id_from_url(url):
    parts = url.split('/')
    if parts[-1].isdigit(): return parts[-1]
    else: return parts[-2]


def split_name(fullname):
    """
    Split a pckg.name string into its package and name parts.

    :param fullname: an entity name in the form of <package>.<name>
    """
    parts = fullname.split('.')
    pkg = ".".join(parts[:-1])
    simpleName = parts[-1]
    return pkg, simpleName
