#MenuBar.py
import wx
import wx.lib.agw.aui as aui # Tab notebooks


def CreateMenuBar(self):
    menuBar = wx.MenuBar()
    menuFile = wx.Menu()
    menuEdit = wx.Menu()
    menuAbout = wx.Menu()
        
    self.menuFile_Open = menuFile.Append(wx.ID_OPEN, "&Open"+"\t"+"Ctrl+O",
                                             "Open a new file.")
    menuFile.AppendSeparator()

    self.menuFile_Save = menuFile.Append(wx.ID_SAVE,
                                             "&Save"+"\t"+"Ctrl+S",
                                             "Save the current file.")
    self.menuFile_SaveAs = menuFile.Append(wx.ID_SAVEAS,
                                             "&Save As"+"\t"+"Ctrl+Shift+S",
                                             "Save file under different name.")
    menuFile.AppendSeparator()

    self.menuFile_RenameTab = menuFile.Append(wx.ID_ANY,"&Rename Tab","Rename current tab")

    self.menuFile_Close = menuFile.Append(wx.ID_EXIT,'&Exit' + "\t" + "Ctrl+X",
                                              "Exit the program")
    #------------
    self.menuEdit_Cut = menuEdit.Append(wx.ID_CUT,
                                            "&Cut" + "\t" + "Ctrl+X",
                                            "Cut")
    self.menuEdit_Copy = menuEdit.Append(wx.ID_COPY,
                                             "&Copy"+"\t"+"Ctrl+C",
                                             "Copy")
    self.menuEdit_Paste = menuEdit.Append(wx.ID_PASTE,
                                            "&Paste"+"\t"+"Ctrl+V",
                                             "Paste")
    menuEdit.AppendSeparator()
    self.menuEdit_Undo = menuEdit.Append(wx.ID_UNDO,
                                             "&Undo"+"\t"+"Ctrl+Z",
                                             "Undo")
    self.menuEdit_Redo = menuEdit.Append(wx.ID_REDO,
                                             "&Redo"+"\t"+"Ctrl+Shift+Z",
                                             "Redo")

    self.menuAbout_Info = menuAbout.Append(wx.ID_ANY,
                                            "&About"+"\t"+"Ctrl+I",
                                            "Information about this program")
    #-------
    menuBar.Append(menuFile,"File")
    menuBar.Append(menuEdit,"Edit")
    menuBar.Append(menuAbout,"About")

    self.SetMenuBar(menuBar)