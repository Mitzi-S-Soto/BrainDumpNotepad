# Bind Events
"""
This script is to preform all the wx Bind events.
It also has all the 'onEvent' type functions related
to the Bind Events
"""
import pathlib as Path

import wx
import wx.lib.agw.aui as aui
import wx.richtext as rt

import src.functions as f
import src.autosave as autosave

import gui.popmenu_tab as tabpop
import gui.abtdialog as about

import logging

logging.basicConfig(
    level=logging.DEBUG, format=" %(asctime)s -  %(levelname)s -  %(message)s"
)

def _SetConstants():

    f.MAINNOTEBOOK = f.MAINWINDOW.notebook
    f.WILDCARD = f.MAINNOTEBOOK.WILDCARD
    f.MAINTREE = f.MAINWINDOW.Tree
    f.ALTEVENTTAB = [f.MAINWINDOW.idTabPop_Save, f.MAINWINDOW.idTabPop_Close]

def StartBind(self):
    
    _SetConstants()

    w = f.MAINWINDOW
    
    # MAIN MENU EVENTS
    w.Bind(wx.EVT_MENU, OnNewTab, w.menuFile_NewTab)
    w.Bind(wx.EVT_MENU, OnFileOpen, w.menuFile_Open)
    w.Bind(wx.EVT_MENU, OnFileOpenProject, w.menuFile_OpenProject)
    w.Bind(wx.EVT_MENU, OnRefreshProject, w.menuFile_RefreshProject)
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
    w.Bind(wx.EVT_TOOL, OnRefreshProject, w.idOnRefreshProject)


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

    # TabPopMenu
    w.Bind(wx.EVT_MENU, OnFileSave, w.idTabPop_Save)
    w.Bind(wx.EVT_MENU, OnCloseTab, w.idTabPop_Close)

    # TREE EVENTS
    f.MAINTREE.Bind(wx.EVT_TREE_ITEM_ACTIVATED, OnTreeItemClicked)
    # TODO: Create Right Click Save


"""##########
    ON FUNCTIONS
##########"""

######## MAIN MENU BAR #########

### FILESAVING ###


def _AskForFilename(style=wx.FD_SAVE, **dialogOptions):
    wildcard, types = rt.RichTextBuffer.GetExtWildcard(save=False)
    message = "Choose a file :"
    defaultDir = f.filePath
    dialog = wx.FileDialog(
        f.MAINWINDOW,
        message=message,
        defaultDir=defaultDir,
        wildcard=wildcard,
        style=style,
    )
    dialog.SetFilterIndex(3)

    if dialog.ShowModal() == wx.ID_OK:
        f.fileType = types[dialog.GetFilterIndex()]
        f.filePath = dialog.GetPath()
        logging.debug('checking')
        logging.debug(Path.Path(f.filePath))
        if Path.Path(f.filePath).parent == Path.Path(f.UNORGANIZEDTEXTSPATH):
            logging.debug('same path')
            wx.MessageBox('The chosen output file is in the temperary files\n Choose another file', 'Error', wx.OK | wx.ICON_WARNING)
            providedFilename = False
            _AskForFilename()
        else:
            providedFilename = True   
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
    """open a directory in the file tree"""
    dlg = wx.DirDialog(
        None, "Choose input directory", " ", wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST
    )
    if dlg.ShowModal() == wx.ID_OK:
        f.ChangeProjectTreeDirectory(dlg.GetPath())
    dlg.Destroy()


def OnFileSave(event):
    id = event.GetId()
    tab = f.GetCurrentTab(True, id)
    if tab.isSaved:
        tab.rtc.SaveFile()
        f.ChangeOpenFiles()
    else:
        OnFileSaveAs(event)


def OnFileSaveAs(event):
    id = event.GetId()
    tab = f.GetCurrentTab(True, id)
    file = tab.rtc.GetFilename()
    file = Path.Path(file).name
    if _AskForFilename(defaultFile=file, style=wx.FD_SAVE):
        if f.filePath:
            f.DeleteTempSave(tab)
            tab.rtc.SaveFile(f.filePath, f.fileType)
            tab.isSaved = True
            f.ChangeOpenFiles()

def OnRefreshProject(event):
    f.ChangeProjectTreeDirectory()


# ---


def OnAbout(event):
    aboutDlg = about.AboutDlg(f.MAINWINDOW)
    aboutDlg.Show()


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
    """The RichTextCtrl can handle menu and update events for undo,
    redo, cut, copy, paste, delete, and select all, so just
    forward the event to it."""
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


def _SetIndent(unindent=False):
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
    """When tab is closed via menu"""
    tab = f.MAINNOTEBOOK.GetPage(f.MAINWINDOW.tabPopPage)
    file = tab.rtc.GetFilename()
    if Path.Path(file).parent == Path.Path(f.UNORGANIZEDTEXTSPATH):
        answer = _AskToSave(tab)
        if answer == "cancel":
            event.Veto()
    else:
        tab.rtc.SaveFile()
    f.ChangeOpenFiles(tab)
    f.MAINNOTEBOOK.DeletePage(f.MAINWINDOW.tabPopPage)


def OnPageClose(event):
    tab = event.GetSelection()
    tab = f.MAINNOTEBOOK.GetPage(tab)
    file = tab.rtc.GetFilename()
    if Path.Path(file).parent == Path.Path(f.UNORGANIZEDTEXTSPATH):
        answer = _AskToSave(tab)
        if answer == "cancel":
            event.Veto()
    else:
        tab.rtc.SaveFile()
    f.ChangeOpenFiles(tab)


def _AskToSave(tab):
    dlg = wx.MessageDialog(
        f.MAINNOTEBOOK,
        "File not saved",
        "File isn't saved. If you don't save "
        "the temporary save will be lost."
        "\n\nDo you want to Save?",
        wx.YES_NO
        | wx.CANCEL
        | wx.ICON_INFORMATION
        | wx.CANCEL_DEFAULT
        | wx.ICON_WARNING,
    )
    clicked = dlg.ShowModal()

    if clicked == wx.ID_YES:
        # save
        answer = "yes"
        file = tab.rtc.GetFilename()
        file = Path.Path(file).name
        if _AskForFilename(style=wx.FD_SAVE):
            if f.filePath:
                # TODO: if file is in UNSAVED ask to choose another
                if Path.Path(f.filePath).parent == f.UNORGANIZEDTEXTSPATH:
                    # TODO: Ask for different file thing
                    hi = 0
                f.DeleteTempSave(tab)
                tab.rtc.SaveFile(f.filePath, f.fileType)
                tab.isSaved = True
                f.ChangeOpenFiles()

    elif clicked == wx.ID_NO:
        # close w/o save
        f.DeleteTempSave(tab)
        answer = "no"

    elif clicked == wx.ID_CANCEL:
        # dont close window
        answer = "cancel"
    dlg.Destroy()

    return answer


def OnPageClosed(event):
    logging.debug("closed")


# ON TREE CONTROLS


def OnTreeItemClicked(event):
    wildcard = (
        "txt",
        "xml",
        "ox",
        "py",
    )  # TODO: I should be able to have this as a 'global' list somewhere
    item = f.MAINTREE.GetFocusedItem()
    data = f.MAINTREE.GetItemData(item)
    if data:
        path = str(Path.Path(data[0]))

    if f.MAINTREE.ItemHasChildren(item):
        f.MAINTREE.Toggle(item)
    else:
        # OPEN ITEM
        f.ChangeOpenFiles()
        for type in wildcard:
            if path.endswith(type):
                if path not in f.openedFiles:
                    new = f.CreateOpenTab(path)
                    filepath = new.rtc.GetFilename()
                    f.projectFiles.append(filepath)
                else:
                    f.GetTabFromFilename(path)
