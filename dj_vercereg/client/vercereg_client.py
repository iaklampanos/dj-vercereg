import os 
import sys
import requests 

TOKEN_FILENAME='_token'
AUTH_HEADER='' # TODO: Fill in / Internet connection...
PROTOCOL='http'
HOST='localhost'
PORT='8000'
BASE_URL=PROTOCOL + '://' + HOST + ':' + PORT

DEF_PKG_PES='pes'
DEF_PKG_FNS='fns'
DEF_PKG_LIT='lits'
DEF_PKG_FNIMPLS='fnimpls'
DEF_PKG_PEIMPLS='peimpls'
DEF_PKG_WORKSPACES='workspaces'

def login(username, password):
  """docstring for login"""
  pass

def main():
  """docstring for main"""
  print BASE_URL


if __name__ == '__main__':
  main()