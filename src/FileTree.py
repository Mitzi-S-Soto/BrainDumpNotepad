#import sys
#import os
#from pathlib import Path
import wx
import wx.lib.agw.aui as aui # Tab notebooks


class FileTree(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self,parent=parent, id=wx.ID_ANY)
        self.tree = self.CreateTree()
 
    def CreateTree(self):
        self.Tree = wx.TreeCtrl(self,wx.ID_ANY,wx.DefaultPosition,style = wx.TR_HIDE_ROOT|wx.TR_NO_BUTTONS|wx.TR_SINGLE)
        self.root = self.Tree.AddRoot('FileRoot')
        self.UnsortedFiles = self.Tree.AppendItem(self.root,'Unsorted')
        #----
        layout = wx.BoxSizer(wx.HORIZONTAL)
        layout.Add(self.Tree,proportion=1,border=4,flag=wx.ALL|wx.EXPAND)
        self.SetSizer(layout)
#------