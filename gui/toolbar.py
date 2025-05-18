#toolbar.py
import wx
import gui.images as images
'''
Toolbar GUI
'''

def MakeToolBar(self):
    self.tbar_panel = wx.Panel(self,style=wx.BORDER_NONE)
    tbar = wx.ToolBar(self.tbar_panel,style=wx.BORDER_NONE)
    tbar.SetToolBitmapSize(wx.Size(25,25))
    tbar.SetToolSeparation(5)

    self.idOnOpen = tbar.AddTool(-1, '', images.document.GetBitmap(), shortHelp="Open")
    self.idOnOpenProject = tbar.AddTool(-1, '', images.subfolder.GetBitmap(), shortHelp="Open Project")
    self.idOnSave = tbar.AddTool(-1, '', images.save.GetBitmap(), shortHelp="Save")
    self.idOnRefreshProject = tbar.AddTool(-1, '', images.refresh2.GetBitmap(), shortHelp="Refresh Project")

    tbar.AddSeparator()

    self.idOnCut = tbar.AddTool(wx.ID_CUT, '', images.cut.GetBitmap(),shortHelp="Cut")
    self.idOnCopy = tbar.AddTool(wx.ID_COPY, '', images.copy.GetBitmap(), shortHelp="Copy")
    self.idOnPaste = tbar.AddTool(wx.ID_PASTE, '', images.paste.GetBitmap(), shortHelp="Paste")
    
    tbar.AddSeparator()

    self.idOnUndo = tbar.AddTool(wx.ID_UNDO, '',images.undo.GetBitmap(), shortHelp="Undo")
    self.idOnRedo = tbar.AddTool(wx.ID_REDO, '', images.redo.GetBitmap(), shortHelp="Redo")
    
    tbar.AddSeparator()

    self.idOnBold = tbar.AddCheckTool(-1, '', images.bold.GetBitmap(), shortHelp="Bold")
    self.idOnItalic = tbar.AddCheckTool(-1, '', images.italic.GetBitmap(), shortHelp="Italic")
    self.idOnUnderline = tbar.AddCheckTool(-1, '', images.underline.GetBitmap(), shortHelp="Underline")
    
    tbar.AddSeparator()
    
    self.idOnAlignLeft = tbar.AddCheckTool(-1, '', images.left.GetBitmap(), shortHelp="Align Left")
    self.idOnAlignCenter = tbar.AddCheckTool(-1, '', images.center.GetBitmap(), shortHelp="Center")
    self.idOnAlignRight = tbar.AddCheckTool(-1, '', images.right.GetBitmap(), shortHelp="Align Right")
    
    tbar.AddSeparator()
    
    self.idOnUnindent = tbar.AddTool(-1, '', images.outdent.GetBitmap(), shortHelp="Indent Less")
    self.idOnIndent = tbar.AddTool(-1, '', images.indent.GetBitmap(), shortHelp="Indent More")
    
    tbar.AddSeparator()
    
    self.idOnFont = tbar.AddTool(-1, '', images.text.GetBitmap(), shortHelp="Font")
    self.idOnColor = tbar.AddTool(-1, '', images.color.GetBitmap(), shortHelp="Font Colour")
    
    tbar.AddSeparator()
    
    self.idNewTab = tbar.AddTool(-1,' ', images.plus.GetBitmap(), shortHelp="New Tab")
    
    tbar.Realize()
    
