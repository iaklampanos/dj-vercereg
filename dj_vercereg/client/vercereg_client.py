#!/usr/bin/env python

import sys
import os
import curses
import collections
import argparse
import datetime

from vercereg_lib import VerceRegManager

class VerceRegClient:
  HISTORY_LENGTH = 5000
  history = None
  manager = None

  def __init__(self):
    self.history = collections.deque(maxlen=self.HISTORY_LENGTH)
    self.manager = VerceRegManager()
  

def main():
  # TODO: Define and implement commands for the client
  # parser = argparse.ArgumentParser(description='Client for the VERCE Registry.')
  # parser.add_argument('command', metavar='Command', type=str,
  #                    help='a VERCE Registry command')
                     
  manager = VerceRegManager()
  manager.login('admin', 'admin')
  manager.clone(1, 'cloned_wspc'+'@'.join(str(datetime.datetime.now()).split()))

if __name__ == '__main__':
  main()