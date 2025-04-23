#FileTree Class
import wx

class FileTree(wx.TreeCtrl):
    def __init__(self,parent):
        super().__init__(parent,wx.ID_ANY,wx.DefaultPosition,style = wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS|wx.TR_SINGLE)
        self.root = self.AddRoot('FileRoot')
        self.UnsortedFiles = self.AppendItem(self.root,'Unsorted')
        self.UnSaved = self.AppendItem(self.root,'UnSaved')
        self.OpenDir = self.AppendItem(self.root,'Open Directory')
        #----

    def OnActivate():
        '''
        '''
        #TODO: When Item Double-Clicked, open or switch to file Tab
        pass

  
#------