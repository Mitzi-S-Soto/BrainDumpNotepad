#----------------------------------------------------------------------
# flatnotebookDemo.py
#
# Created: 12-03-2009
#
# Author: Mike Driscoll  
#
# Email:  mike@pythonlibrary.org
#----------------------------------------------------------------------

import panelOne, panelTwo, panelThree
import wx
import wx.lib.agw.flatnotebook as fnb

########################################################################
class FlatNotebookDemo(fnb.FlatNotebook):
    """
    Flatnotebook class
    """

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        fnb.FlatNotebook.__init__(self, parent, wx.ID_ANY)
        
        pageOne = panelOne.TabPanel(self)
        pageTwo = panelTwo.TabPanel(self)
        pageThree = panelThree.TabPanel(self)
        
        self.AddPage(pageOne, "PageOne")
        self.AddPage(pageTwo, "PageTwo")
        self.AddPage(pageThree, "PageThree")
    
    

########################################################################
class DemoFrame(wx.Frame):
    """
    Frame that holds all other widgets
    """

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""        
        wx.Frame.__init__(self, None, wx.ID_ANY, 
                          "FlatNotebook Tutorial",
                          size=(600,400)
                          )
        panel = wx.Panel(self)
        
        notebook = FlatNotebookDemo(panel)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.ALL|wx.EXPAND, 5)
        panel.SetSizer(sizer)
        self.Layout()
        
        self.Show()
        
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = DemoFrame()
    app.MainLoop()
