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

import logging
logging.basicConfig()
logger = logging.getLogger('DJREG_LIB')
logger.setLevel(logging.INFO)

class VerceRegManager:
  '''Interface with the registry, keeping some info on logging in, etc.'''

  token_filename_prefix = 'djvercereg_token_'
  token_file = None
  token = None
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
  
  # JSON property names
  PROP_PEIMPLS='peimpls'
  PROP_FNIMPLS='fnimpls'
  
  # For resolving json object types
  TYPE_PE = 0
  TYPE_FN = 1
  TYPE_PEIMPL = 2
  TYPE_FNIMPL = 3
  TYPE_NOT_RECOGNISED=100
  
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
  
  def _get_auth_header(self):
    '''Return the authentication header as used for requests to the registry.'''
    return {'Authorization':'Token %s'%(self.get_auth_token())}
    
    
  def _valid_login(self, username):
    ''' Return true if the client has already logged in and login is valid. '''
    return self.logged_in and self.logged_in_username == username and (datetime.datetime.now()-self.logged_in_time).total_seconds() < self.PASSWORD_EXPIRATION_PERIOD_HRS * 60 * 60
      
  def _extract_kind_from_json_object(self, j):
    '''
    The kind/type is inferred based on the URL. Assumes this is called for single objects.
    Return one of the TYPE* values defined in VerceRegManager.
    '''
    # logger.info(j)
    rhs = j['url'][len(self.get_base_url())+1:]
    kind = rhs[:rhs.find('/')]

    if kind == 'pes': return VerceRegManager.TYPE_PE
    elif kind == 'functions': return VerceRegManager.TYPE_FN
    else: return VerceRegManager.TYPE_NOT_RECOGNISED
      
  def login(self, username, password):
    '''(Lazily) log into vercereg with the given credentials.'''
    if self._valid_login(username):
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
      self.token = json.loads(r.text)['token']
      f.write(self.token)
      f.close()
    return self.logged_in
  

  def get_auth_token(self):
    '''Return the authorization token.'''
    #TODO Potentially unsafe operation - check this is safe
    if self.logged_in:
      return self.token
    else:
      raise NotLoggedInError()
      return


  def clone(self, orig_workspace_id, name):
    '''Clone the given workspace into a new one with the name `name`. '''
    if not self.logged_in:
      raise NotLoggedInError()
      return

    url = self.get_base_url() + self.URL_WORKSPACES + '?clone_of=' + str(orig_workspace_id)
    r = requests.post(url, data={'name':name}, headers=self._get_auth_header())
    print r.text
  

  def get_pe_implementation_code(self, workspace_id, pckg, name, impl_index=0):
    '''Return the implementation code of the given PE / identified by pckg-name.'''
    if not self.logged_in:
      raise NotLoggedInError()
      return
    
    url = self.get_base_url() + self.URL_WORKSPACES + str(workspace_id) + '/?fqn=' + pckg + '.' + name
    r = requests.get(url, headers=self._get_auth_header())
    
    if r.status_code != requests.codes.ok:
      r.raise_for_status()
      return
      
    if self.PROP_PEIMPLS not in r.json():
      raise NotPEError()
      return 
      
    try:
      impl_url = r.json()[self.PROP_PEIMPLS][impl_index]
    except IndexError:
      raise ImplementationNotFound()
      return
      
    r = requests.get(impl_url, headers=self._get_auth_header())
    return r.json().get('code')


  def get_fn_implementation_code(self, workspace_id, pckg, name, impl_index=0):
    '''Return the implementation code of the given function / identified by pckg-name.'''
    if not self.logged_in:
      raise NotLoggedInError()
      return
    
    url = self.get_base_url() + self.URL_WORKSPACES + str(workspace_id) + '/?fqn=' + pckg + '.' + name
    r = requests.get(url, headers=self._get_auth_header())
    
    if r.status_code != requests.codes.ok:
      r.raise_for_status()
      return
      
    if self.PROP_FNIMPLS not in r.json():
      raise NotFunctionError()
      return 
      
    try:
      impl_url = r.json()[self.PROP_FNIMPLS][impl_index]
    except IndexError:
      raise ImplementationNotFound()
      return
      
    r = requests.get(impl_url, headers=self._get_auth_header())
    return r.json().get('code')


  #TODO Implement
  def get_spec(self, workspace_id, pckg, name): # optional
    pass
  
  
  #TODO Implement
  def get_impl(self, workspace_id, pckg, name): # optional
    pass
    
    
  def get_pe_spec(self, workspace_id, pckg, name):
    '''Return a JSON-coded specification of the PE identified by workspace_id, pckg.name'''
    if not self.logged_in:
      raise NotLoggedInError()
      return
    
    url = self.get_base_url() + self.URL_WORKSPACES + str(workspace_id) + '/?fqn=' + pckg + '.' + name
    r = requests.get(url, headers=self._get_auth_header())
    
    if r.status_code != requests.codes.ok:
      r.raise_for_status()
      return
      
    if self._extract_kind_from_json_object(r.json()) != VerceRegManager.TYPE_PE:
      raise NotPEError()
      return
    
    return r.json()
    
  
  def get_fn_spec(self, workspace_id, pckg, name):
    '''Return a JSON-coded specification of the function identified by workspace_id, pckg.name'''
    if not self.logged_in:
      raise NotLoggedInError()
      return
    
    url = self.get_base_url() + self.URL_WORKSPACES + str(workspace_id) + '/?fqn=' + pckg + '.' + name
    r = requests.get(url, headers=self._get_auth_header())
    
    if r.status_code != requests.codes.ok:
      r.raise_for_status()
      return
      
    if self._extract_kind_from_json_object(r.json()) != VerceRegManager.TYPE_FN:
      raise NotPEError()
      return
    
    return r.json()
    
    
  def set_pe_spec(self, workspace_id, pckg, name):
    pass 

## VERCE Registry library errors: ###########################

class ImplementationNotFound(Exception):
  pass
  
class NotPEError(Exception):
  pass

class NotFunctionError(Exception):
  pass

class VerceRegClientLibError(Exception):
  pass

class NotLoggedInError(VerceRegClientLibError):
  def __init__(self, msg='Log in required; please log in first.'):
    self.msg = msg

