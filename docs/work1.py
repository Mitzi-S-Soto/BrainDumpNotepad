# Brain Dump Notepad
"""
Developer: Mitzi S. Soto

#TODO: Cut/Paste doesnt copy styles?

#TODO: Create functions to load last opened docs
#TODO: Function to delete old temp file when saving and/or
"""
import sys
import os
from pathlib import Path

import wx
import wx.richtext as rt
import wx.lib.agw.aui as aui  # Tab notebooks

import src.constants as c
import gui.aui_mgr as aui_mgr  # our AUI Manager code
import src.MenuBar as MenuBar
import src.Toolbar as Toolbar
import src.FileTree as tree
import src.MainNotebook as note
import src.autosave as autosave
import src.bind_events as bind_events

import logging

logging.basicConfig(
    level=logging.DEBUG, format=" %(asctime)s -  %(levelname) s -  %(message)s"
)

"""
SavePerspective(self)
Saves the entire user interface layout into an encoded string,
which can then be stored by the application (probably using Config).
When a perspective is restored using LoadPerspective, the entire user
interface will return to the state it was when the perspective was saved.
"""
#---
class MainWindow(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Notebook", size=(640, 480))

        self.path = Path.cwd()
        self.dirname = "."
        self.flagDirty = False
        self.fileType = 1
        self.filePath = str(Path.cwd() / Path("UnorganizedTexts"))

        logging.debug(self.filePath)

        self.SetProperties()

        ''' --------
            Create GUI
            --------'''

        MenuBar.CreateMenuBar(self)

        self.toolbar = Toolbar.MakeToolBar(self)
        self.Tree = tree.FileTree(self)
        self.notebook = note.MainNotebook(self)
        self.notebook.CreateNewTab()

        self._mgr = aui_mgr.Mgr(self)

        self._mgr.AddPane(
            self.tbar_panel,
            aui.AuiPaneInfo()
            .Top()
            .Dockable(False)
            .Floatable(False)
            .Resizable(False)
            .CaptionVisible(False)
            .CloseButton(False),
        )
        self._mgr.AddPane(
            self.Tree,
            aui.AuiPaneInfo()
            .Left()
            .Caption("File Tree")
            .CloseButton(False)
            .TopDockable(False)
            .BottomDockable(False)
            .Floatable(False),
        )
        self._mgr.AddPane(self.notebook, aui.AuiPaneInfo().CenterPane())

        self._mgr.Update()

        self.CreateStatusBar()
        # --------

        autosave.CreateAutoSaver(self)

        bind_events.Bind(self)

        # ------------
    
    def SetProperties(self):
        self.SetTitle()

    def SetTitle(self):
        # MyFrame.SetTitle overrides wx.Frame.SetTitle,
        # so we have to call it using super :
        super(MainWindow, self).SetTitle("BrainDump Notepad")

    def AskForFilename(self, **dialogOptions):

        dialog = wx.FileDialog(self, **dialogOptions)

        if dialog.ShowModal() == wx.ID_OK:
            providedFilename = True
            self.fileType = dialog.GetFilterIndex()
            self.filename = dialog.GetFilename()
            self.dirname = dialog.GetDirectory()
            self.filePath = dialog.GetPath()
            # Update the window title with the new filename
            self.SetTitle()
        else:
            providedFilename = False
        dialog.Destroy()
        return providedFilename

    def GetCurrentTab(self):
        tab = self.notebook.GetCurrentPage()
        return tab

    #--filesaving

    def OnFileOpen(self, event):
        """Open a File"""
        if self.AskForFilename(style=wx.FD_OPEN, **c.DefaultFileDialogOptions(self)):
            path = self.filePath
            if path:
                #TODO: This needs to open a tab only related to old tab
                name = Path(path).name
                tab = self.notebook.CreateOpenTab(name)
                fileType = self.fileType
                tab.rtc.LoadFile(path, fileType)

    def OnFileSave(self, event):
        tab = self.GetCurrentTab()
        if tab.isSaved:
            if not tab.rtc.GetFilename():
                self.OnFileSaveAs(event)
                return
            tab.rtc.SaveFile()
        else:
            self.OnFileSaveAs(event)

    def OnFileSaveAs(self, event):
        types = rt.RichTextBuffer.GetExtWildcard(save=True)
        tab = self.GetCurrentTab()
        file = tab.file
        if self.AskForFilename(
            defaultFile=file, style=wx.FD_SAVE, **c.DefaultFileDialogOptions(self)
        ):
            tab = self.GetCurrentTab()
            filepath = self.filePath
            if self.filePath:
                fileType = types[self.fileType]
                ext = rt.RichTextBuffer.FindHandlerByType(fileType).GetExtension()
                if not filepath.endswith(ext):
                    filepath += "." + ext
                tab.isSaved = True
                tab.rtc.SaveFile(filepath, fileType)

    def onAbout(self, event):
        abt = wx.MessageDialog(self, "BrainDumpPad", "Shmul nuutpat", wx.OK)
        abt.ShowModal()
        abt.Destroy()

    def onExit(self, event):
        aui_mgr.Mgr.onClose()
        self.Close(True)

    def OnCloseWindow(self, event):
        """
        Quit and destroy application.
        """
        aui_mgr.Mgr.onClose()
        #self.Autosaver.handleAbort()
        self.Destroy()

#############

    def ForwardEvent(self, event):
        # The RichTextCtrl can handle menu and update events for undo,
        # redo, cut, copy, paste, delete, and select all, so just
        # forward the event to it.
        tab = self.GetCurrentTab()
        tab.rtc.ProcessEvent(event)

    def OnBold(self, event):
        tab = self.GetCurrentTab()
        tab.rtc.ApplyBoldToSelection()

    def OnUpdateBold(self, event):
        tab = self.GetCurrentTab()
        event.Check(tab.rtc.IsSelectionBold())

    def OnItalic(self, event):
        tab = self.GetCurrentTab()
        tab.rtc.ApplyItalicToSelection()

    def OnUpdateItalic(self, event):
        tab = self.GetCurrentTab()
        event.Check(tab.rtc.IsSelectionItalics())

    def OnUnderline(self, event):
        tab = self.GetCurrentTab()
        tab.rtc.ApplyUnderlineToSelection()

    def OnUpdateUnderline(self, event):
        tab = self.GetCurrentTab()
        event.Check(tab.rtc.IsSelectionUnderlined())

    def OnAlignLeft(self, event):
        tab = self.GetCurrentTab()
        tab.rtc.ApplyAlignmentToSelection(wx.TEXT_ALIGNMENT_LEFT)

    def OnUpdateAlignLeft(self, event):
        tab = self.GetCurrentTab()
        event.Check(tab.rtc.IsSelectionAligned(wx.TEXT_ALIGNMENT_LEFT))

    def OnAlignCenter(self, event):
        tab = self.GetCurrentTab()
        tab.rtc.ApplyAlignmentToSelection(wx.TEXT_ALIGNMENT_CENTRE)

    def OnUpdateAlignCenter(self, event):
        tab = self.GetCurrentTab()
        event.Check(tab.rtc.IsSelectionAligned(wx.TEXT_ALIGNMENT_CENTRE))

    def OnAlignRight(self, event):
        tab = self.GetCurrentTab()
        tab.rtc.ApplyAlignmentToSelection(wx.TEXT_ALIGNMENT_RIGHT)

    def OnUpdateAlignRight(self, event):
        tab = self.GetCurrentTab()
        event.Check(tab.rtc.IsSelectionAligned(wx.TEXT_ALIGNMENT_RIGHT))

    def OnIndentLess(self, event):
        tab = self.GetCurrentTab()
        attr = wx.TextAttr()
        attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
        ip = tab.rtc.GetInsertionPoint()
        if tab.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if tab.rtc.HasSelection():
                r = tab.rtc.GetSelectionRange()

        if attr.GetLeftIndent() >= 100:
            attr.SetLeftIndent(attr.GetLeftIndent() - 100)
            attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
            self.rtc.SetStyle(r, attr)

    def OnIndentMore(self, event):
        tab = self.GetCurrentTab()
        attr = wx.TextAttr()
        attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
        ip = tab.rtc.GetInsertionPoint()
        if tab.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if tab.rtc.HasSelection():
                r = tab.rtc.GetSelectionRange()

            attr.SetLeftIndent(attr.GetLeftIndent() + 100)
            attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
            tab.rtc.SetStyle(r, attr)

    def OnFont(self, event):
        tab = self.GetCurrentTab()
        if not tab.rtc.HasSelection():
            return

        r = tab.rtc.GetSelectionRange()
        fontData = wx.FontData()
        fontData.EnableEffects(False)
        attr = wx.TextAttr()
        attr.SetFlags(wx.TEXT_ATTR_FONT)
        if tab.rtc.GetStyle(tab.rtc.GetInsertionPoint(), attr):
            fontData.SetInitialFont(attr.GetFont())

        dlg = wx.FontDialog(self, fontData)
        if dlg.ShowModal() == wx.ID_OK:
            fontData = dlg.GetFontData()
            font = fontData.GetChosenFont()
            if font:
                attr.SetFlags(wx.TEXT_ATTR_FONT)
                attr.SetFont(font)
                tab.rtc.SetStyle(r, attr)
        dlg.Destroy()

    def OnColour(self, event):
        tab = self.GetCurrentTab()
        colourData = wx.ColourData()
        attr = wx.TextAttr()
        attr.SetFlags(wx.TEXT_ATTR_TEXT_COLOUR)
        if tab.rtc.GetStyle(tab.rtc.GetInsertionPoint(), attr):
            colourData.SetColour(attr.GetTextColour())

        dlg = wx.ColourDialog(self, colourData)
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


# ----

class MyApp(wx.App):

    def OnInit(self):
        frame = MainWindow()
        frame.Show(True)
        return True


#################################
class main:
    def __init__(self):
        app = MyApp(False)
        app.MainLoop()


if __name__ == "__main__":
    main()
