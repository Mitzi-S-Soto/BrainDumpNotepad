import wx

import gui.images as images

import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s -  %(levelname)s -  %(message)s')

def InitTabPopMenu(self):
    # Make IDs
    self.idTabPop_Save = wx.NewIdRef()
    self.idTabPop_Close = wx.NewIdRef()

def OnTabPopMenu(self, event):
    logging.debug("On Tab Pop Menu\n")

    # make a menu
    menu = wx.Menu()
    menu.Append(self.idTabPop_Save, "Save")
    menu.Append(self.idTabPop_Close, "Close")

    # Popup the menu.  If an item is selected then its handler
    # will be called before PopupMenu returns.
    self.PopupMenu(menu)
    menu.Destroy()
