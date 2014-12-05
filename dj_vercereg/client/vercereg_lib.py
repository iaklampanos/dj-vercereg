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

import os 
import sys
import requests 
from tempfile import NamedTemporaryFile
import json
import datetime

class VerceRegManager:
  '''Interface with the registry, keeping some info on logging in, etc.'''

  token_filename_prefix = 'djvercereg_token_'
  token_file = None
  auth_header='' # TODO: Fill in / Internet connection...
  protocol='http'
  host='localhost'
  port='8000'
  logged_in = False
  logged_in_time = None
  logged_in_username = None
  
  PASSWORD_EXPIRATION_PERIOD_HRS = 3

  # REST service URL suffixes
  URL_AUTH = '/api-token-auth/'
  URL_USERS = '/users/'
  URL_REGISTRYUSERGROUPS = '/registryusergroups/'
  URL_GROUPS = '/groups/'
  URL_WORKSPACES = '/workspaces/'
  URL_PES = '/pes/'
  URL_FNS = '/functions/'
  URL_LITS = '/literals/'
  URL_CONNS = '/connections/'
  URL_PEIMPLS = '/pe_implementations/'
  URL_FNIMPLS = '/fn_implementations/'

  # Default package names depending on the type of the registrable item
  DEF_PKG_PES='pes'
  DEF_PKG_FNS='fns'
  DEF_PKG_LIT='lits'
  DEF_PKG_FNIMPLS='fnimpls'
  DEF_PKG_PEIMPLS='peimpls'
  DEF_PKG_WORKSPACES='workspaces'
  
  # def __init__(self):
  #   pass
  
  def get_base_url(self):
    return self.protocol + '://' + self.host + ':' + self.port
  
  def get_auth_token(self):
    if not self.logged_in:
      raise NotLoggedInError()
      return
    with open(self.token_file, 'r') as f:
      token = f.readline().strip()
    return token
  
  def get_auth_header(self):
    return {'Authorization':'Token %s'%(self.get_auth_token())}
      
  def login(self, username, password):
    '''(Lazily) log into vercereg with the given credentials.'''
    if self.logged_in and self.logged_in_username == username and (datetime.datetime.now()-logged_in_time).total_seconds() < self.PASSWORD_EXPIRATION_PERIOD_HRS * 60 * 60:
      return True
    
    data = {'username':username, 'password':password}
    url = self.get_base_url() + self.URL_AUTH
    r = requests.post(url, data)
    self.logged_in = r.status_code == 200
    if self.logged_in:
      self.logged_in_time = datetime.datetime.now()
      self.logged_in_username = username
      f = NamedTemporaryFile(prefix=self.token_filename_prefix, delete=False)
      self.token_file = f.name
      f.write(json.loads(r.text)['token'])
      f.close()
    return self.logged_in

  def clone(self, orig_workspace_id, name):
    '''Clone the given workspace into a new one with the name `name`. '''
    if not self.logged_in:
      raise NotLoggedInError()
      return

    url = self.get_base_url() + self.URL_WORKSPACES + '?clone_of=' + str(orig_workspace_id)
    r = requests.post(url, data={'name':name}, headers=self.get_auth_header())
    print r.text
  
  def get_implementations(self, workspace_id, pckg, name):
    '''Return a dictionary corresponding to the implementations of the given workspace-item / identified by pckg-name.'''
    if not self.logged_in:
      raise NotLoggedInError()
      return
    
    #TODO implement!
    pass
    

## VERCE Registry library errors: ###########################    
class VerceRegClientLibError(Exception):
  pass

class NotLoggedInError(VerceRegClientLibError):
  def __init__(self, msg='Log in required; please log in first.'):
    self.msg = msg

