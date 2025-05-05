#FileTree Class
import wx

class FileTree(wx.TreeCtrl):
    def __init__(self,parent):
        super().__init__(parent,wx.ID_ANY,wx.DefaultPosition,style = wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS|wx.TR_SINGLE)
        
        self.projectFolder = ''

        isz = (24,24)
        il = wx.ImageList(isz[0], isz[1])

        self.file_img = [
        il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER,      wx.ART_OTHER, isz)),
        il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, isz)),
        il.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, isz)),
        ]
        self.SetImageList(il)
        self.il = il

        self.normal = wx.TreeItemIcon_Normal
        self.expanded = wx.TreeItemIcon_Expanded

        self.root = self.AddRoot('FileRoot')
        self.UnsortedFiles = self.AppendItem(self.root,'nonProject')
        self.UnSaved = self.AppendItem(self.root,'unSaved')
        self.Project = self.AppendItem(self.root,'Project')


        self.SetItemImage(self.UnsortedFiles, self.file_img[0], self.normal)
        self.SetItemImage(self.UnsortedFiles, self.file_img[1], self.expanded)

        self.SetItemImage(self.UnSaved, self.file_img[0], self.normal)
        self.SetItemImage(self.UnSaved, self.file_img[1], self.expanded)

        self.SetItemImage(self.Project, self.file_img[0], self.normal)
        self.SetItemImage(self.Project, self.file_img[1], self.expanded)


        #----
   

    def OnActivate():
        '''
        '''
        #TODO: When Item Double-Clicked, open or switch to file Tab
        pass
  
#------