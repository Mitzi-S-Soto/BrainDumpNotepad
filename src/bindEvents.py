
import sys
import os
from pathlib import Path
import wx

def Bind(self):

    self.Bind(wx.EVT_MENU, self.onOpen, self.menuFile_Open)
    self.Bind(wx.EVT_MENU, self.onSave, self.menuFile_Save)
    self.Bind(wx.EVT_MENU, self.OnFileSaveAs2, self.menuFile_SaveAs)
    self.Bind(wx.EVT_MENU, self.ChangeTabName, self.menuFile_RenameTab)
    self.Bind(wx.EVT_MENU, self.onExit, self.menuFile_Close)
    self.Bind(wx.EVT_MENU, self.ForwardEvent, self.menuEdit_Cut)
    self.Bind(wx.EVT_MENU, self.ForwardEvent, self.menuEdit_Copy)
    self.Bind(wx.EVT_MENU, self.ForwardEvent, self.menuEdit_Paste)
    self.Bind(wx.EVT_MENU, self.ForwardEvent, self.menuEdit_Undo)
    self.Bind(wx.EVT_MENU, self.ForwardEvent, self.menuEdit_Redo)
    self.Bind(wx.EVT_MENU, self.onAbout, self.menuAbout_Info)

    self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    self.Bind(wx.EVT_TIMER, self.Autosaver.OnTimer)
