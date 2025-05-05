# Bind Events
'''
This script is to preform all the wx Bind events.
It also has all the 'onEvent' type functions related
to the Bind Events
'''
import pathlib as Path
import send2trash as trash

import wx 
import wx.lib.agw.aui as aui
import wx.richtext as rt

import src.functions as f
import src.autosave as autosave

import gui.popmenu_tab as tabpop

import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s -  %(levelname)s -  %(message)s')

def StartBind(self):
    w = f.MAINWINDOW

    f.MAINNOTEBOOK = w.notebook
    f.WILDCARD = f.MAINNOTEBOOK.WILDCARD

    f.MAINTREE = w.Tree

    f.ALTEVENTTAB = [w.idTabPop_Save, w.idTabPop_Close]

    # MAIN MENU EVENTS
    w.Bind(wx.EVT_MENU, OnNewTab, w.menuFile_NewTab)
    w.Bind(wx.EVT_MENU, OnFileOpen, w.menuFile_Open)
    w.Bind(wx.EVT_MENU, OnFileOpenProject, w.menuFile_OpenProject)
    w.Bind(wx.EVT_MENU, OnFileSave, w.menuFile_Save)
    w.Bind(wx.EVT_MENU, OnFileSaveAs, w.menuFile_SaveAs)
    w.Bind(wx.EVT_MENU, OnExit, w.menuFile_Close)
    w.Bind(wx.EVT_MENU, ForwardEvent, w.menuEdit_Cut)
    w.Bind(wx.EVT_MENU, ForwardEvent, w.menuEdit_Copy)
    w.Bind(wx.EVT_MENU, ForwardEvent, w.menuEdit_Paste)
    w.Bind(wx.EVT_MENU, ForwardEvent, w.menuEdit_Undo)
    w.Bind(wx.EVT_MENU, ForwardEvent, w.menuEdit_Redo)
    w.Bind(wx.EVT_MENU, OnBold, w.menuFormat_Bold)
    w.Bind(wx.EVT_MENU, OnItalic, w.menuFormat_Italic)
    w.Bind(wx.EVT_MENU, OnUnderline, w.menuFormat_Underline)
    w.Bind(wx.EVT_MENU, OnAlignLeft, w.menuFormat_AlignLeft)
    w.Bind(wx.EVT_MENU, OnAlignCenter, w.menuFormat_AlignCenter)
    w.Bind(wx.EVT_MENU, OnAlignRight, w.menuFormat_AlignRight)
    w.Bind(wx.EVT_MENU, OnUnindent, w.menuFormat_Unindent)
    w.Bind(wx.EVT_MENU, OnIndent, w.menuFormat_Indent)
    w.Bind(wx.EVT_MENU, OnFont, w.menuFormat_Font)
    w.Bind(wx.EVT_MENU, OnColor, w.menuFormat_Color)

    w.Bind(wx.EVT_MENU, OnAbout, w.menuAbout_Info)

    # MAIN TOOLBAR EVENTS
    w.Bind(wx.EVT_TOOL, OnFileOpen, w.idOnOpen)
    w.Bind(wx.EVT_TOOL, OnFileOpenProject, w.idOnOpenProject)
    w.Bind(wx.EVT_TOOL, OnFileSave, w.idOnSave)

    w.Bind(wx.EVT_TOOL, ForwardEvent, w.idOnCut)
    w.Bind(wx.EVT_TOOL, ForwardEvent, w.idOnCopy)
    w.Bind(wx.EVT_TOOL, ForwardEvent, w.idOnPaste)

    w.Bind(wx.EVT_TOOL, ForwardEvent, w.idOnUndo)
    w.Bind(wx.EVT_TOOL, ForwardEvent, w.idOnRedo)

    w.Bind(wx.EVT_TOOL, OnBold, w.idOnBold)
    w.Bind(wx.EVT_UPDATE_UI, OnUpdateBold, w.idOnBold)

    w.Bind(wx.EVT_TOOL, OnItalic, w.idOnItalic)
    w.Bind(wx.EVT_UPDATE_UI, OnUpdateItalic, w.idOnItalic)
    w.Bind(wx.EVT_TOOL, OnUnderline, w.idOnUnderline)
    w.Bind(wx.EVT_UPDATE_UI, OnUpdateUnderline, w.idOnUnderline)

    w.Bind(wx.EVT_TOOL, OnAlignLeft, w.idOnAlignLeft)
    w.Bind(wx.EVT_UPDATE_UI, OnUpdateAlignLeft, w.idOnAlignLeft)
    w.Bind(wx.EVT_TOOL, OnAlignCenter, w.idOnAlignCenter)
    w.Bind(wx.EVT_UPDATE_UI, OnUpdateAlignCenter, w.idOnAlignCenter)
    w.Bind(wx.EVT_TOOL, OnAlignRight, w.idOnAlignRight)
    w.Bind(wx.EVT_UPDATE_UI, OnUpdateAlignRight, w.idOnAlignRight)

    w.Bind(wx.EVT_TOOL, OnUnindent, w.idOnUnindent)
    w.Bind(wx.EVT_TOOL, OnIndent, w.idOnIndent)

    w.Bind(wx.EVT_TOOL, OnFont, w.idOnFont)
    w.Bind(wx.EVT_TOOL, OnColor, w.idOnColor)

    w.Bind(wx.EVT_TOOL, OnNewTab, w.idNewTab)

    w.Bind(wx.EVT_CLOSE, OnCloseWindow)

    # AUTOSAVE SYSTEM
    autosave.StartAutoSaveTimer(w)
    w.Bind(wx.EVT_TIMER, autosave.OnAutoSaveTimer)

    # NOTEBOOK EVENTS
    f.MAINNOTEBOOK.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSE, OnPageClose)
    f.MAINNOTEBOOK.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSED, OnPageClosed)
    f.MAINNOTEBOOK.Bind(aui.EVT_AUINOTEBOOK_TAB_RIGHT_DOWN, OnPageRightClick)

    #TabPopMenu
    w.Bind(wx.EVT_MENU, OnFileSave, w.idTabPop_Save)
    w.Bind(wx.EVT_MENU, OnCloseTab, w.idTabPop_Close)

    #TREE EVENTS
    f.MAINTREE.Bind(wx.EVT_TREE_ITEM_ACTIVATED, OnTreeItemClicked)

'''##########
    ON FUNCTIONS
##########'''

######## MAIN MENU BAR #########

### FILESAVING ###

def _AskForFilename(**dialogOptions):
    wildcard, types = rt.RichTextBuffer.GetExtWildcard(save=False)
    message = "Choose a file :"
    defaultDir = f.filePath
    dialog = wx.FileDialog(f.MAINWINDOW, message = message, defaultDir = defaultDir, wildcard=wildcard)

    if dialog.ShowModal() == wx.ID_OK:
        providedFilename = True
        f.fileType = types[dialog.GetFilterIndex()]
        f.filePath = dialog.GetPath()
    else:
        providedFilename = False
    dialog.Destroy()
    return providedFilename

def OnFileOpen(event):
    """Open a File"""
    if _AskForFilename(style=wx.FD_OPEN):
        if f.filePath not in f.openedFiles:
            f.CreateOpenTab(f.filePath)
        else:
            f.GetTabFromFilename(f.filePath)

def OnFileOpenProject(event):
    '''open a directory in the file tree'''
    dlg = wx.DirDialog (None, "Choose input directory", "",
                    wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
    if dlg.ShowModal() == wx.ID_OK:
        f.ChangeProjectTreeDirectory(dlg.GetPath())
    dlg.Destroy()

def OnFileSave(event):
    id = event.GetId()
    tab = f.GetCurrentTab(True, id)
    if tab.isSaved:
        tab.rtc.SaveFile()
    else:
        OnFileSaveAs(event)

def OnFileSaveAs(event):
    id = event.GetId()
    tab =  f.GetCurrentTab(True, id)
    file = tab.rtc.GetFilename()
    file = Path.Path(file).name
    if _AskForFilename(
        defaultFile=file, style=wx.FD_SAVE
    ):
        if f.filePath:
            if not tab.isSaved:
                delFile = tab.rtc.GetFilename()
                trash.send2trash(delFile)
            tab.rtc.SaveFile(f.filePath, f.fileType)
            tab.isSaved = True

# ---

def OnAbout(event):
    abt = wx.MessageDialog(f.MAINWINDOW, f.PROGRAMABOUT, f.PROGRAMNAME, wx.OK)
    abt.ShowModal()
    abt.Destroy()

def OnExit(event):
    f.OnExitProgram()
    f.MAINWINDOW.Close(True)

def OnCloseWindow(event):
    """
    Quit and destroy application.
    """
    f.OnExitProgram()
    f.MAINWINDOW.Destroy()

###### On Text Stylings/Toolbar #######

def ForwardEvent(event):
    '''The RichTextCtrl can handle menu and update events for undo,
       redo, cut, copy, paste, delete, and select all, so just
       forward the event to it.'''
    tab = f.GetCurrentTab()
    tab.rtc.ProcessEvent(event)

def OnBold(event):
    tab = f.GetCurrentTab()
    tab.rtc.ApplyBoldToSelection()

def OnUpdateBold(event):
    tab = f.GetCurrentTab()
    if tab:
        event.Check(tab.rtc.IsSelectionBold())

def OnItalic(event):
    tab = f.GetCurrentTab()
    if tab:
        tab.rtc.ApplyItalicToSelection()

def OnUpdateItalic(event):
    tab = f.GetCurrentTab()
    if tab:
        event.Check(tab.rtc.IsSelectionItalics())

def OnUnderline(event):
    tab = f.GetCurrentTab()
    if tab:
        tab.rtc.ApplyUnderlineToSelection()

def OnUpdateUnderline(event):
    tab = f.GetCurrentTab()
    if tab:
        event.Check(tab.rtc.IsSelectionUnderlined())

def OnAlignLeft(event):
    tab = f.GetCurrentTab()
    if tab:
        tab.rtc.ApplyAlignmentToSelection(wx.TEXT_ALIGNMENT_LEFT)

def OnUpdateAlignLeft(event):
    tab = f.GetCurrentTab()
    if tab:
        event.Check(tab.rtc.IsSelectionAligned(wx.TEXT_ALIGNMENT_LEFT))

def OnAlignCenter(event):
    tab = f.GetCurrentTab()
    if tab:
        tab.rtc.ApplyAlignmentToSelection(wx.TEXT_ALIGNMENT_CENTRE)

def OnUpdateAlignCenter(event):
    tab = f.GetCurrentTab()
    if tab:
        event.Check(tab.rtc.IsSelectionAligned(wx.TEXT_ALIGNMENT_CENTRE))

def OnAlignRight(event):
    tab = f.GetCurrentTab()
    if tab:
        tab.rtc.ApplyAlignmentToSelection(wx.TEXT_ALIGNMENT_RIGHT)

def OnUpdateAlignRight(event):
    tab = f.GetCurrentTab()
    if tab:
        event.Check(tab.rtc.IsSelectionAligned(wx.TEXT_ALIGNMENT_RIGHT))

def _SetIndent(unindent = False):
    tab = f.GetCurrentTab()
    attr = wx.TextAttr()
    attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
    ip = tab.rtc.GetInsertionPoint()

    if tab.rtc.GetStyle(ip, attr):
        r = rt.RichTextRange(ip, ip)
        if tab.rtc.HasSelection():
            r = tab.rtc.GetSelectionRange()
        if unindent:
            if attr.GetLeftIndent() >= 100:
                indentAmount = attr.GetLeftIndent() - 100
        elif not unindent:
            indentAmount = attr.GetLeftIndent() + 100
        attr.SetLeftIndent(indentAmount)
        attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
        tab.rtc.SetStyle(r, attr)

def OnUnindent(event):
    _SetIndent(True)

def OnIndent(event):
    _SetIndent()

def OnFont(event):
    tab = f.GetCurrentTab()
    if not tab.rtc.HasSelection():
        return

    r = tab.rtc.GetSelectionRange()
    fontData = wx.FontData()
    fontData.EnableEffects(False)
    attr = wx.TextAttr()
    attr.SetFlags(wx.TEXT_ATTR_FONT)
    if tab.rtc.GetStyle(tab.rtc.GetInsertionPoint(), attr):
        fontData.SetInitialFont(attr.GetFont())

    dlg = wx.FontDialog(f.MAINWINDOW, fontData)
    if dlg.ShowModal() == wx.ID_OK:
        fontData = dlg.GetFontData()
        font = fontData.GetChosenFont()
        if font:
            attr.SetFlags(wx.TEXT_ATTR_FONT)
            attr.SetFont(font)
            tab.rtc.SetStyle(r, attr)
    dlg.Destroy()

def OnColor(event):
    tab = f.GetCurrentTab()
    colourData = wx.ColourData()
    attr = wx.TextAttr()
    attr.SetFlags(wx.TEXT_ATTR_TEXT_COLOUR)
    if tab.rtc.GetStyle(tab.rtc.GetInsertionPoint(), attr):
        colourData.SetColour(attr.GetTextColour())

    dlg = wx.ColourDialog(f.MAINWINDOW, colourData)
    if dlg.ShowModal() == wx.ID_OK:
        colourData = dlg.GetColourData()
        colour = colourData.GetColour()
        if colour:
            if not tab.rtc.HasSelection():
                tab.rtc.BeginTextColour(colour)
            else:
                r = tab.rtc.GetSelectionRange()
                attr.SetFlags(wx.TEXT_ATTR_TEXT_COLOUR)
                attr.SetTextColour(colour)
                tab.rtc.SetStyle(r, attr)
    dlg.Destroy()

def OnNewTab(event):
    f.CreateNewTab()

### NOTEBOOK & TABS

def OnPageRightClick(event):
    f.MAINWINDOW.tabPopPage = event.GetSelection()
    tabpop.OnTabPopMenu(f.MAINWINDOW, event)

def OnCloseTab(event):
    '''When tab is closed via menu'''
    f.MAINNOTEBOOK.DeletePage(f.MAINWINDOW.tabPopPage)

def OnPageClose(event):
    tab = event.GetSelection()
    tab = f.MAINNOTEBOOK.GetPage(tab)
    tab.rtc.SaveFile()
    f.ChangeOpenFiles(tab)

def OnPageClosed(event):
    logging.debug('closed')

#ON TREE CONTROLS

def OnTreeItemClicked(event):
    wildcard, types = rt.RichTextBuffer.GetExtWildcard(save=True)
    item = f.MAINTREE.GetFocusedItem()
    data = f.MAINTREE.GetItemData(item)
    if data:
        path = str(Path.Path(data[0]))

    if f.MAINTREE.ItemHasChildren(item):
        f.MAINTREE.Toggle(item)
    else:
        #OPEN ITEM
        f.ChangeOpenFiles()
        for ext in wildcard:
            if path.endswith(ext):
                if path not in f.openedFiles:
                    new = f.CreateOpenTab(path)
                    filepath = new.rtc.GetFilename()
                    f.projectFiles.append(filepath)
                else:
                    f.GetTabFromFilename(path)
        
    