#MenuBar.py
import wx

def CreateMenuBar(self):
    menuBar = wx.MenuBar()
    menuFile = wx.Menu()
    menuEdit = wx.Menu()
    menuFormat = wx.Menu()
    menuAbout = wx.Menu()

    self.menuFile_NewTab = menuFile.Append(-1,"&New","Create a new tab.")
        
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
    # ------
    self.menuFormat_Bold = menuFormat.Append(wx.ID_BOLD,
                                             "&Bold"+"\t"+"Ctrl+Shift+B",
                                             "Bold")
    self.menuFormat_Italic = menuFormat.Append(wx.ID_ITALIC,
                                             "&Italic"+"\t"+"Ctrl+Shift+I",
                                             "Italic")
    self.menuFormat_Underline = menuFormat.Append(wx.ID_UNDERLINE,
                                             "&Underline"+"\t"+"Ctrl+Shift+U",
                                             "Underline")
    menuFormat.AppendSeparator()
    self.menuFormat_AlignLeft = menuFormat.Append(-1, "&Align Left"+"\t"+"Ctrl+[",
                                                  "Align Left")
    self.menuFormat_AlignCenter = menuFormat.Append(-1, "&Align Center"+"\t"+"Ctrl+\ ",
                                                  "Align Center")
    self.menuFormat_AlignRight = menuFormat.Append(-1, "&Align Right"+"\t"+"Ctrl+]",
                                                  "Align Right")
    menuFormat.AppendSeparator()
    self.menuFormat_Unindent = menuFormat.Append(-1,"&Unindent",
                                                 "Unindent")
    self.menuFormat_Indent = menuFormat.Append(-1,"&Indent",
                                                 "Indent")
    menuFormat.AppendSeparator()
    self.menuFormat_Font = menuFormat.Append(-1,"&Font Style",
                                                 "Set Font Style")
    self.menuFormat_Color = menuFormat.Append(-1,"&Font Color",
                                                 "Set Font Color")


    # ------
    self.menuAbout_Info = menuAbout.Append(wx.ID_ANY,
                                            "&About"+"\t"+"Ctrl+I",
                                            "Information about this program")
    #-------
    menuBar.Append(menuFile,"File")
    menuBar.Append(menuEdit,"Edit")
    menuBar.Append(menuFormat,"Format")
    menuBar.Append(menuAbout,"About")

    self.SetMenuBar(menuBar)