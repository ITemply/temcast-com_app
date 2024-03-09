# Windows

from tkinter import *
import random, string, threading, math, sys
from threading import *

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

def createInfoWindow(statusId):
  global secure

  root = Tk()
  root.overrideredirect(True)
  root.geometry('200x60+0+0')
  root.title('Info')

  text = Label(root, text='Session Open: ' + statusId)
  text.pack()

  buttonFrame = Frame(root)
  buttonFrame.pack()

  def toggleSecure():
    global secure
    secure = True

  closeButton=Button(buttonFrame, text='Close', width=7, height=1, command=root.destroy)
  closeButton.grid(row=0, column=0, padx=5, pady=5)

  secureButton=Button(buttonFrame, text='Secure Cast', width=7, height=1, command=toggleSecure)
  secureButton.grid(row=0, column=1, padx=5, pady=5)

  root.mainloop()

def createSecureAccept(username):
  global accepting
  accepting = False

  root = Tk()
  root.overrideredirect(True)

  windowHeight = 60
  windowWidth = 200
  screenWidth = root.winfo_screenwidth()
  screenHright = root.winfo_screenheight()
  x = math.floor((screenWidth/2) - (windowWidth/2))
  y = math.floor((screenHright/2) - (windowHeight/2))

  root.geometry(f'{windowWidth}x{windowHeight}+{x}+{y}')
  root.title('Accept User')

  text = Label(root, text='Session Request: ' + username)
  text.pack()

  buttonFrame = Frame(root)
  buttonFrame.pack()

  def acceptRequest():
    global accepting
    accepting = True
    root.destroy()

  def declineRequest():
    root.destroy()

  acceptButton=Button(buttonFrame, text='Accept', width=7, height=1, command=acceptRequest)
  acceptButton.grid(row=0, column=0, padx=5, pady=5)

  declineButton=Button(buttonFrame, text='Decline', width=7, height=1, command=declineRequest)
  declineButton.grid(row=0, column=1, padx=5, pady=5)

  root.mainloop()

  return accepting

def openAcceptWindow(username):
  acceptWindow = returningThread(target=createSecureAccept, args=(username,))
  acceptWindow.start()
  returningAccept = acceptWindow.join()

def openInfoWindow(statusId):
  mainWindow = returningThread(target=createInfoWindow, args=(statusId,))
  mainWindow.start()