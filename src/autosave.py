#AutoSaveTimer.py
'''
This is the autosave timer featurer of the program
It is kept as a seperate module as to help manage it
seperatly so it doesn't break as easy

Possibly could be improved, but as for now
we aren't going to touch what isn't broken
'''
import wx
import wx.lib.delayedresult as delayedresult

import src.functions as f

import logging

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s -  %(levelname)s -  %(message)s')

#----

def StartAutoSaveTimer(self):
    self.Timer = wx.Timer(self)
    self.Timer.Start(f.autosaveTimerLength)
    self.TimerRunning = False
    logging.info("Timer Start")

def AutoSaveTimerStop(self):
    self.Timer.Stop()
    del self.Timer
    
def OnAutoSaveTimer(self):
    if not f.MAINWINDOW.TimerRunning:
        f.MAINWINDOW.TimerRunning = True
        f.MAINWINDOW.StatusBar.SetStatusText("Auto Saving...")
        delayedresult.startWorker(AutoSaveConsumer,AutoSaveProducer, wargs={self})
        logging.info("started working")
    else:
        logging.debug("Already running")
    logging.info("got EVT_TIMER event")

def AutoSaveProducer(self, *wargs):
    logging.info('Start Saving')
    f.SaveAllOpenFiles()
    f.MAINWINDOW.TimerRunning = False
    logging.info('Saving end')
    f.MAINWINDOW.StatusBar.SetStatusText(" ")
    return True

def AutoSaveHandleAbort(self):
    #TODO: Fix This
    """Abort the result computation."""
    #AutoSaver.workerFn.AbortedException()
    pass

def AutoSaveConsumer(delayedResult):
    result = delayedResult.get()
    if result:
        logging.info("done %s", result)
    else:
        logging.debug("No result")