#tabpopmenu.py
'''
The pop up menu shown when notebook tab
is right clicked
'''
import wx

def InitTabPopMenu(self):
    # Make IDs
    self.idTabPop_Save = wx.NewIdRef()
    self.idTabPop_Close = wx.NewIdRef()
    self.tabPopPage = 0

def OnTabPopMenu(self, event):
    menu = wx.Menu()
    menu.Append(self.idTabPop_Save, "Save")
    menu.Append(self.idTabPop_Close, "Close")

    self.PopupMenu(menu)
    menu.Destroy()

