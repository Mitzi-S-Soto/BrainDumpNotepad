#----------------------------------------------------------------------
# agwAUINotebook.py
#
# Created: December 2009
#
# Author: Mike Driscoll - mike@pythonlibrary.org
#
# Note: Some code comes from the wxPython demo
#
#----------------------------------------------------------------------


import wx
import wx.lib.agw.aui as aui 

########################################################################
class TabPanelOne(wx.Panel):
    """
    A simple wx.Panel class
    """
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """"""
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        
        izer = wx.BoxSizer(wx.VERTICAL)
        txtOne = wx.TextCtrl(self, wx.ID_ANY, "")
        txtTwo = wx.TextCtrl(self, wx.ID_ANY, "")
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(txtOne, 0, wx.ALL, 5)
        sizer.Add(txtTwo, 0, wx.ALL, 5)
        
        self.SetSizer(sizer)
        
########################################################################
class DemoFrame(wx.Frame):
    """
    wx.Frame class
    """
    
    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, 
                          "AGW AUI Notebook Tutorial",
                          size=(600,400))
 
        self._mgr = aui.AuiManager()
        
        # tell AuiManager to manage this frame
        self._mgr.SetManagedWindow(self)
                
        notebook = aui.AuiNotebook(self)
        panelOne = TabPanelOne(notebook)
        panelTwo = TabPanelOne(notebook)
        
        notebook.AddPage(panelOne, "PanelOne", False)
        notebook.AddPage(panelTwo, "PanelTwo", False)
        
        self._mgr.AddPane(notebook, 
                          aui.AuiPaneInfo().Name("notebook_content").
                          CenterPane().PaneBorder(False)) 
        self._mgr.Update()
        #notebook.EnableTab(1, False)
        
 #----------------------------------------------------------------------
# Run the program
if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = DemoFrame()
    frame.Show()
    app.MainLoop()
