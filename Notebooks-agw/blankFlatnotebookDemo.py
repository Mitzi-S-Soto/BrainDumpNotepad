#----------------------------------------------------------------------
# flatnotebookDemo.py
#
# Created: 12-04-2009
#
# Author: Mike Driscoll  
#
# Email:  mike@pythonlibrary.org
#----------------------------------------------------------------------

import panelOne, panelTwo, panelThree
import random
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
        
########################################################################
class DemoFrame(wx.Frame):
    """
    Frame that holds all other widgets
    """

    #----------------------------------------------------------------------
    def __init__(self, title="FlatNotebook Add/Remove Page Tutorial"):
        """Constructor"""        
        wx.Frame.__init__(self, None, wx.ID_ANY, 
                          title=title,
                          size=(600,400)
                          )
        self._newPageCounter = 0
        panel = wx.Panel(self)
        self.createRightClickMenu()
        
        # create some widgets
        self.notebook = FlatNotebookDemo(panel)
        addPageBtn = wx.Button(panel, label="Add Page")
        addPageBtn.Bind(wx.EVT_BUTTON, self.onAddPage)
        removePageBtn = wx.Button(panel, label="Remove Page")
        removePageBtn.Bind(wx.EVT_BUTTON, self.onDeletePage)
        self.notebook.SetRightClickMenu(self._rmenu)
        
        # create some sizers
        sizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # layout the widgets
        sizer.Add(self.notebook, 1, wx.ALL|wx.EXPAND, 5)
        btnSizer.Add(addPageBtn, 0, wx.ALL, 5)
        btnSizer.Add(removePageBtn, 0, wx.ALL, 5)
        sizer.Add(btnSizer)
        panel.SetSizer(sizer)
        self.Layout()
        
        self.Show()
        
    #----------------------------------------------------------------------
    def createRightClickMenu(self):
        """
        Based on method from flatnotebook demo
        """
        self._rmenu = wx.Menu()
        item = wx.MenuItem(self._rmenu, wx.ID_ANY, 
                           "Close Tab\tCtrl+F4", 
                           "Close Tab")
        self.Bind(wx.EVT_MENU, self.onDeletePage, item)
        self._rmenu.AppendItem(item)
        
    #----------------------------------------------------------------------
    def onAddPage(self, event):
        """
        This method is based on the flatnotebook demo
        
        It adds a new page to the notebook
        """
        caption = "New Page Added #" + str(self._newPageCounter)
        self.Freeze()

        self.notebook.AddPage(self.createPage(caption), caption, True)
        self.Thaw()
        self._newPageCounter = self._newPageCounter + 1
        
    #----------------------------------------------------------------------
    def createPage(self, caption):
        """
        Creates a notebook page from one of three
        panels at random and returns the new page
        """
        panel_list = [panelOne, panelTwo, panelThree]
        obj = random.choice(panel_list)
        page = obj.TabPanel(self.notebook)
        return page
        
    #----------------------------------------------------------------------
    def onDeletePage(self, event):
        """
        This method is based on the flatnotebook demo
        
        It removes a page from the notebook
        """
        self.notebook.DeletePage(self.notebook.GetSelection())
        
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = DemoFrame()
    app.MainLoop()
