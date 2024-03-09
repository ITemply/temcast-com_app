# Connections

import socketio, threading, sys, pathlib, base64
from PIL import ImageGrab
from io import BytesIO

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

sio = socketio.Client()

@sio.event
def connect():
    print('Connection Established')

@sio.event
def disconnect():
    print('Client Dissconnected')

def captureScreen(sessionId):
  while True:
    screenshot = ImageGrab.grab()
    buffer = BytesIO()
    screenshot.save(buffer, 'png')
    b64 = base64.b64encode(buffer.getvalue())
    sio.emit('screenData', '{"image": "' + b64.decode('utf-8') + '", "id": "' + sessionId + '"}')

def startScreenCast(sessionId):
  startCast = returningThread(target=captureScreen, args=(sessionId,))
  startCast.start()

sio.connect('https://3000-itemply-temcast-r7oav6476dj.ws-us108.gitpod.io', namespaces=['/'])