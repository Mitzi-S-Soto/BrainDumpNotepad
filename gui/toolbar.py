import wx

import gui.images as images

def MakeToolBar(self):
    self.tbar_panel = wx.Panel(self)
    tbar = wx.ToolBar(self.tbar_panel)

    self.idOnOpen = tbar.AddTool(-1, '', images._rt_open.GetBitmap(), shortHelp="Open")
    self.idOnOpenProject = tbar.AddTool(-1, '', images.expansion.GetBitmap(), shortHelp="Open Project")
    self.idOnSave = tbar.AddTool(-1, '', images._rt_save.GetBitmap(), shortHelp="Save")

    tbar.AddSeparator()

    self.idOnCut = tbar.AddTool(wx.ID_CUT, '', images._rt_cut.GetBitmap(), shortHelp="Cut")# on.ForwardEvent, on.ForwardEvent)
    self.idOnCopy = tbar.AddTool(wx.ID_COPY, '', images._rt_copy.GetBitmap(), shortHelp="Copy")# on.ForwardEvent, on.ForwardEvent)
    self.idOnPaste = tbar.AddTool(wx.ID_PASTE, '', images._rt_paste.GetBitmap(), shortHelp="Paste")# on.ForwardEvent, on.ForwardEvent)
    
    tbar.AddSeparator()

    self.idOnUndo = tbar.AddTool(wx.ID_UNDO, '', images._rt_undo.GetBitmap(), shortHelp="Undo")# on.ForwardEvent, on.ForwardEvent)
    self.idOnRedo = tbar.AddTool(wx.ID_REDO, '', images._rt_redo.GetBitmap(), shortHelp="Redo")# on.ForwardEvent, on.ForwardEvent)
    
    tbar.AddSeparator()

    self.idOnBold = tbar.AddCheckTool(-1, '', images._rt_bold.GetBitmap(), shortHelp="Bold")# on.OnBold, on.OnUpdateBold)
    self.idOnItalic = tbar.AddCheckTool(-1, '', images._rt_italic.GetBitmap(), shortHelp="Italic")# on.OnItalic, on.OnUpdateItalic)
    self.idOnUnderline = tbar.AddCheckTool(-1, '', images._rt_underline.GetBitmap(), shortHelp="Underline")# on.OnUnderline, on.OnUpdateUnderline)
    
    tbar.AddSeparator()
    
    self.idOnAlignLeft = tbar.AddCheckTool(-1, '', images._rt_alignleft.GetBitmap(), shortHelp="Align Left")# on.OnAlignLeft, on.OnUpdateAlignLeft)
    self.idOnAlignCenter = tbar.AddCheckTool(-1, '', images._rt_centre.GetBitmap(), shortHelp="Center")# on.OnAlignCenter, on.OnUpdateAlignCenter)
    self.idOnAlignRight = tbar.AddCheckTool(-1, '', images._rt_alignright.GetBitmap(), shortHelp="Align Right")# on.OnAlignRight, on.OnUpdateAlignRight)
    
    tbar.AddSeparator()
    
    self.idOnUnindent = tbar.AddTool(-1, '', images._rt_indentless.GetBitmap(), shortHelp="Indent Less")# on.OnIndentLess)
    self.idOnIndent = tbar.AddTool(-1, '', images._rt_indentmore.GetBitmap(), shortHelp="Indent More")# on.OnIndentMore)
    
    tbar.AddSeparator()
    
    self.idOnFont = tbar.AddTool(-1, '', images._rt_font.GetBitmap(), shortHelp="Font")#, on.OnFont)
    self.idOnColor = tbar.AddTool(-1, '', images._rt_colour.GetBitmap(), shortHelp="Font Colour")#, on.OnColour)
    
    tbar.AddSeparator()
    
    self.idNewTab = tbar.AddTool(-1,' ', images.moredialog.GetBitmap(), shortHelp="New Tab")#, on.OnNewTab)
    
    tbar.Realize()
    
