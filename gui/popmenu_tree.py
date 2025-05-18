# tabpopmenu.py
"""
The pop up menu shown when notebook tab
is right clicked
"""
import wx


def InitTreePopMenu(self):
    # Make IDs
    self.idTreePop_Save = wx.NewIdRef()
    self.idTreePop_Close = wx.NewIdRef()
    self.treePopPage = 0


def OnTreePopMenu(self, event):
    menu = wx.Menu()
    menu.Append(self.idTreePop_Save, "Save")
    menu.Append(self.idTreePop_Close, "Close")

    self.PopupMenu(menu)
    menu.Destroy()
