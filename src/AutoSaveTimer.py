#AutoSaveTimer.py

import wx
import wx.lib.delayedresult as delayedresult

#----

running = False

def OnStart(self):
    self.Timer = wx.Timer(self)
    self.Timer.Start(3000)
    
    print("EVT_TIMER timer started\n")
    

def OnStop(self):
    self.Timer.Stop()
    print("EVT_TIMER timer stopped\n")
    del self.Timer

def OnTimer(Self): #event
    global running
    '''
    This will start the autosave for all open tabs
    #Can use lib.delayedresult to process saves without freezing gui
    delayedresult.startWorker(self._resultConsumer, self._resultProducer,
                                  wargs=(self.jobID,self.abortEvent), jobID=self.jobID)
        '''
    if not running:
        running = True
        delayedresult.startWorker(resultConsumer,resultProducer)
        print( "Starting job in producer thread: GUI remains responsive")
    print("got EVT_TIMER event\n")

def resultProducer():
    global running
    """
        Pretend to be a complex worker function or something that takes
        long time to run due to network access etc. GUI will freeze if this
        method is not called in separate thread.
        """
    print('result produces, sleep now')
    import time
    count = 0
    while count < 50:
        time.sleep(0.1)
        count += 1
    else:
        running = False
        print('sleep end')
    return True

def handleAbort():
    #TODO: Fix This
    """Abort the result computation."""

    print( "Aborting result for job" )

def resultConsumer(delayedResult):
    print('resultConsumer', delayedResult)
    result = delayedResult.get()

    print( "Got result for job %s" % (result) )
