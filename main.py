# Main

import random, string, threading, math, sys, pathlib, time
from threading import *

path = pathlib.Path(__file__).parent.absolute()
sys.path.insert(0, str(path) + '/modules')

import castWindows, castConnections

def idGenerator(size, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

global secure
secure = False
statusId = "HBB"

authorized = []

class returningThread(threading.Thread):
  def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.result = None

  def run(self):
      if self._target is None:
          return
      try:
          self.result = self._target(*self._args, **self._kwargs)
      except Exception as exc:
          print(f'{type(exc).__name__}: {exc}', file=sys.stderr) 

  def join(self, *args, **kwargs):
      super().join(*args, **kwargs)
      return self.result

castWindows.openInfoWindow(statusId)
castConnections.startScreenCast(statusId)