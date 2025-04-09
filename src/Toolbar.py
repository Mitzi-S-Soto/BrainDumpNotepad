from six import BytesIO

import wx
import wx.richtext as rt
import wx.lib.agw.aui as aui # Tab notebooks

import src.images as images

def MakeToolBar(self):
    def doBind(item, handler, updateUI=None):
        self.Bind(wx.EVT_TOOL, handler, item)
        if updateUI is not None:
            self.Bind(wx.EVT_UPDATE_UI, updateUI, item)
    self.tbar_panel = wx.Panel(self)
    tbar = wx.ToolBar(self.tbar_panel)
    
    #layout = wx.BoxSizer(wx.HORIZONTAL)
    #layout.Add(tbar_panel, proportion=1,border=0,flag=wx.ALL|wx.EXPAND)
    #self.SetSizer(layout)

    doBind( tbar.AddTool(-1, '', images._rt_open.GetBitmap(),
                            shortHelp="Open"), self.OnFileOpen)
    doBind( tbar.AddTool(-1, '', images._rt_save.GetBitmap(),
                            shortHelp="Save"), self.OnFileSave)
    tbar.AddSeparator()
    doBind( tbar.AddTool(wx.ID_CUT, '', images._rt_cut.GetBitmap(),
                            shortHelp="Cut"), self.ForwardEvent, self.ForwardEvent)
    doBind( tbar.AddTool(wx.ID_COPY, '', images._rt_copy.GetBitmap(),
                            shortHelp="Copy"), self.ForwardEvent, self.ForwardEvent)
    doBind( tbar.AddTool(wx.ID_PASTE, '', images._rt_paste.GetBitmap(),
                            shortHelp="Paste"), self.ForwardEvent, self.ForwardEvent)
    tbar.AddSeparator()
    doBind( tbar.AddTool(wx.ID_UNDO, '', images._rt_undo.GetBitmap(),
                            shortHelp="Undo"), self.ForwardEvent, self.ForwardEvent)
    doBind( tbar.AddTool(wx.ID_REDO, '', images._rt_redo.GetBitmap(),
                            shortHelp="Redo"), self.ForwardEvent, self.ForwardEvent)
    tbar.AddSeparator()
    doBind( tbar.AddCheckTool(-1, '', images._rt_bold.GetBitmap(),
                                  shortHelp="Bold"), self.OnBold, self.OnUpdateBold)
    doBind( tbar.AddCheckTool(-1, '', images._rt_italic.GetBitmap(),
                                  shortHelp="Italic"), self.OnItalic, self.OnUpdateItalic)
    doBind( tbar.AddCheckTool(-1, '', images._rt_underline.GetBitmap(),
                                  shortHelp="Underline"), self.OnUnderline, self.OnUpdateUnderline)
    tbar.AddSeparator()
    doBind( tbar.AddCheckTool(-1, '', images._rt_alignleft.GetBitmap(),
                                  shortHelp="Align Left"), self.OnAlignLeft, self.OnUpdateAlignLeft)
    doBind( tbar.AddCheckTool(-1, '', images._rt_centre.GetBitmap(),
                                  shortHelp="Center"), self.OnAlignCenter, self.OnUpdateAlignCenter)
    doBind( tbar.AddCheckTool(-1, '', images._rt_alignright.GetBitmap(),
                                  shortHelp="Align Right"), self.OnAlignRight, self.OnUpdateAlignRight)
    tbar.AddSeparator()
    doBind( tbar.AddTool(-1, '', images._rt_indentless.GetBitmap(),
                            shortHelp="Indent Less"), self.OnIndentLess)
    doBind( tbar.AddTool(-1, '', images._rt_indentmore.GetBitmap(),
                            shortHelp="Indent More"), self.OnIndentMore)
    tbar.AddSeparator()
    doBind( tbar.AddTool(-1, '', images._rt_font.GetBitmap(),
                            shortHelp="Font"), self.OnFont)
    doBind( tbar.AddTool(-1, '', images._rt_colour.GetBitmap(),
                            shortHelp="Font Colour"), self.OnColour)
    tbar.Realize()
    
