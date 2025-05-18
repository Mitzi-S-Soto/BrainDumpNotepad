# FileTree Class
import wx
import gui.images as images


class FileTree(wx.TreeCtrl):
    def __init__(self, parent):
        super().__init__(
            parent,
            wx.ID_ANY,
            wx.DefaultPosition,
            style=wx.TR_HIDE_ROOT | wx.TR_HAS_BUTTONS | wx.TR_SINGLE | wx.BORDER_NONE,
        )

        self.projectFolder = ""
        self.projectRoot = ""
        self.font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Arial")
        self.openColour = wx.Colour(100, 100, 100)

        isz = (24, 24)
        il = wx.ImageList(isz[0], isz[1])

        self.file_img = [
            il.Add(images.folder.GetBitmap()),
            il.Add(images.openfolder.GetBitmap()),
            il.Add(images.file.GetBitmap()),
            il.Add(images.document.GetBitmap()),
            il.Add(images.subfolder.GetBitmap()),
        ]
        self.SetImageList(il)
        self.il = il

        self.normal = wx.TreeItemIcon_Normal
        self.expanded = wx.TreeItemIcon_Expanded

        self.root = self.AddRoot("FileRoot")
        self.UnsortedFiles = self.AppendItem(self.root, "nonProject")
        self.UnSaved = self.AppendItem(self.root, "unSaved")
        self.Project = self.AppendItem(self.root, "Project")
        self.setText(self.UnsortedFiles)
        self.setText(self.UnSaved)
        self.setText(self.Project)

        self.SetItemImage(self.UnsortedFiles, self.file_img[0], self.normal)
        self.SetItemImage(self.UnsortedFiles, self.file_img[1], self.expanded)

        self.SetItemImage(self.UnSaved, self.file_img[0], self.normal)
        self.SetItemImage(self.UnSaved, self.file_img[1], self.expanded)

        self.SetItemImage(self.Project, self.file_img[4], self.normal)
        self.SetItemImage(self.Project, self.file_img[4], self.expanded)

    def setText(self, item):
        self.SetItemFont(item, self.font)

        # ----


# ------
