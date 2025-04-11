#import sys
#import os
#from pathlib import Path
import wx
import wx.lib.agw.aui as aui # Tab notebooks

class FileTree(wx.TreeCtrl):
    def __init__(self,parent):
        super().__init__(parent,wx.ID_ANY,wx.DefaultPosition,style = wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS|wx.TR_SINGLE)
        self.root = self.AddRoot('FileRoot')
        self.UnsortedFiles = self.AppendItem(self.root,'UnSaved')
        self.UnSaved = self.AppendItem(self.root,'UnSorted')
        self.OpenDir = self.AppendItem(self.root,'Open Directory')
        self.AddTreeItem(self.UnSaved,"Item 1")
        #----

    def AddTreeItem(self, folder, name):
        self.AppendItem(folder, name)
        #TODO:
        #   -Tree Folder
        #   -Tree Name
        #   -Tree File Dir
        #   -Tree File Name
        #   -Tree Associated Tab/Tab Associated Tree
        #   -Tree Individual ID?
        #

    def OnActivate():
        '''
        '''
        #TODO: When Item Double-Clicked, open or switch to file Tab
        pass

  
#------