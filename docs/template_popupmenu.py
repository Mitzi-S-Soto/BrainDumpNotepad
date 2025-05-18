import wx
import logging
import gui.images as images
import src.functions as f

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s -  %(levelname)s -  %(message)s')

def InitPopUpMenu(self):
    # Make IDs
    self.popupID1 = wx.NewIdRef()
    self.popupID2 = wx.NewIdRef()
    self.popupID3 = wx.NewIdRef()
    self.popupID4 = wx.NewIdRef()
    self.popupID5 = wx.NewIdRef()
    self.popupID6 = wx.NewIdRef()
    self.popupID7 = wx.NewIdRef()
    self.popupID8 = wx.NewIdRef()
    self.popupID9 = wx.NewIdRef()

def OnContextMenu(event):
    self = f.MAINWINDOW
    logging.debug("OnContextMenu\n")

    # make a menu
    menu = wx.Menu()
    # Show how to put an icon in the menu
    item = wx.MenuItem(menu, self.popupID1,"One")
    bmp = images.Smiles.GetBitmap()
    item.SetBitmap(bmp)
    menu.Append(item)
    # add some other items
    menu.Append(self.popupID2, "Two")
    menu.Append(self.popupID3, "Three")
    menu.Append(self.popupID4, "Four")
    menu.Append(self.popupID5, "Five")
    menu.Append(self.popupID6, "Six")
    # make a submenu
    sm = wx.Menu()
    sm.Append(self.popupID8, "sub item 1")
    sm.Append(self.popupID9, "sub item 1")
    menu.Append(self.popupID7, "Test Submenu", sm)

    # Popup the menu.  If an item is selected then its handler
    # will be called before PopupMenu returns.
    self.PopupMenu(menu)
    menu.Destroy()


#These Go in Bind Events
def OnPopupOne(event):
    logging.debug("Popup one\n")

def OnPopupTwo(event):
    logging.debug("Popup two\n")

def OnPopupThree(event):
    logging.debug("Popup three\n")

def OnPopupFour(event):
    logging.debug("Popup four\n")

def OnPopupFive(event):
    logging.debug("Popup five\n")

def OnPopupSix(event):
    logging.debug("Popup six\n")

def OnPopupSeven(event):
    logging.debug("Popup seven\n")

def OnPopupEight(event):
    logging.debug("Popup eight\n")

def OnPopupNine(event):
    logging.debug("Popup nine\n")