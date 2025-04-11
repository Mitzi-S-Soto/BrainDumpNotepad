#AutoSaveTimer.py

import wx
import wx.lib.delayedresult as delayedresult

#----

running = False

def CreateAutoSaver(self):
    self.Autosaver = AutoSaver(self)
    pass

class AutoSaver():
    def __init__(self, parent):
        self.parent = parent
        self.Timer = wx.Timer(parent)
        self.Timer.Start(10000)
        self.running = False
        print("EVT_TIMER timer started\n")

    def OnStop(self):
        self.Timer.Stop()
        print("EVT_TIMER timer stopped\n")
        del self.Timer
    
    def OnTimer(self, event):
        if not self.running:
            self.running = True
            self.parent.StatusBar.SetStatusText("Producer Saving")
            delayedresult.startWorker(self.resultConsumer,self.resultProducer,cargs={self.parent},wargs={self.parent})
            print( "Starting job in producer thread: GUI remains responsive")
        else:
            print("self is working")
        print("got EVT_TIMER event\n")

    def resultProducer(self, *wargs):
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
            self.running = False
            wargs[0].StatusBar.PushStatusText(" ")
            print('sleep end')
        return True

    def handleAbort(self):
        #TODO: Fix This
        """Abort the result computation."""
        #delayedresult.AbortedException()
        print( "Not Working: Aborting result for job" )


    def resultConsumer(self, delayedResult,*cargs):
        print('resultConsumer', delayedResult)
        
        result = delayedResult.get()

        print( "Got result for job %s" % (result) )
