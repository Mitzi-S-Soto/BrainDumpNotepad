#AutoSaveTimer.py
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
    logging.debug("Timer Start")

def AutoSaveTimerStop(self):
    self.Timer.Stop()
    del self.Timer
    
def OnAutoSaveTimer(self):
    if not f.MAINWINDOW.TimerRunning:
        f.MAINWINDOW.TimerRunning = True
        f.MAINWINDOW.StatusBar.SetStatusText("Auto Saving...")
        delayedresult.startWorker(AutoSaveConsumer,AutoSaveProducer, wargs={self})
        logging.debug("started working")
    else:
        logging.debug("Already running")
    logging.debug("got EVT_TIMER event\n")

def AutoSaveProducer(self, *wargs):
    logging.debug('Start Saving')
    f.SaveAllOpenFiles()
    f.MAINWINDOW.TimerRunning = False
    logging.debug('Saving end')
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
        logging.debug("done {result}")
    else:
        logging.debug("No result")

