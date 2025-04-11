# Brain Dump Notepad
"""
Developer: Mitzi S. Soto

#TODO: Cut/Paste doesnt copy styles

"""
import sys
import os
from pathlib import Path

import wx
import wx.richtext as rt
import wx.lib.agw.aui as aui  # Tab notebooks

import src.AUIMgr as AUIMgr  # our AUI Manager code
import src.MenuBar as MenuBar
import src.Toolbar as Toolbar
import src.FileTree as tree
import src.MainNotebook as note
import src.AutoSaveTimer as AutoSaveTimer
import src.bindEvents as bindEvents

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


# ----
class MainWindow(wx.Frame):

    def __init__(self, filename="noname.txt"):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Notebook", size=(640, 480))

        self.path = Path.cwd()
        self.filename = filename
        self.dirname = "."
        self.flagDirty = False
        self.fileType = 1
        self.filePath = str(Path.cwd() / Path("UnorganizedTexts"))
        logging.debug(self.filePath)

        # --------

        MenuBar.CreateMenuBar(self)

        self.toolbar = Toolbar.MakeToolBar(self)
        self.Tree = tree.FileTree(self)
        self.notebook = note.MainNotebook(self)

        self._mgr = AUIMgr.Mgr(self)

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
        self.SetProperties()

        AutoSaveTimer.CreateAutoSaver(self)

        bindEvents.Bind(self)
        # ------------

    def SetProperties(self):
        self.SetTitle()

    def SetTitle(self):
        # MyFrame.SetTitle overrides wx.Frame.SetTitle,
        # so we have to call it using super :
        super(MainWindow, self).SetTitle("Editor %s" % self.filename)

    def DefaultFileDialogOptions(self):
        """Return a dictionary with file doalog options that
        can be used in bot the save f ile as well as the open file dialog"""
        return dict(
            message="Choose a file :",
            defaultDir=self.filePath,
            wildcard="Text (*.txt)|*.txt|" "Python (*.py)|*py|",
        )

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

    def GetCurrentTabText(self):
        tab = self.GetCurrentTab()
        txt = tab.rtc.GetValue()
        print(txt)
        return txt

    def onOpen(self, event):
        """Open a File"""
        if self.AskForFilename(style=wx.FD_OPEN, **self.DefaultFileDialogOptions()):
            file = open(
                os.path.join(self.dirname, self.filename), "r", encoding="utf-8"
            )
            self.notebook.CreateNewTab()
            self.notebook.openTabs[-1].stTextCtrl.SetValue(file.read())
            file.close()

    def onSave(self, event):
        text = self.GetCurrentTabText()
        tab = self.GetCurrentTab()
        if tab.isSaved:
            filepath = Path(tab.filedir) / tab.file
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(text)
        else:
            self.onSaveAs(event)

    def ChangeTabName(self, event):
        ask = wx.TextEntryDialog(self, "Rename Tab:")
        if ask.ShowModal() == wx.ID_OK:
            tab = self.notebook.GetSelection()
            txt = ask.GetValue()
            self.notebook.SetPageText(tab, txt)
            print(f"User entered: {txt}")
        else:
            print("Dialog cancelled")
        ask.Destroy()

    def onAbout(self, event):
        abt = wx.MessageDialog(self, "BrainDumpPad", "Shmul nuutpat", wx.OK)
        abt.ShowModal()
        abt.Destroy()

    def onExit(self, event):
        AUIMgr.Mgr.onClose()
        self.Close(True)

    def OnCloseWindow(self, event):
        """
        Quit and destroy application.
        """
        AUIMgr.Mgr.onClose()
        self.Autosaver.handleAbort()
        self.Destroy()

    ###########

    def OnFileOpen(self, event):
        pass

    def OnFileSave(self, event):
        pass

    def OnFileSaveAs2(self, event):
        wildcard, types = rt.RichTextBuffer.GetExtWildcard(save=True)
        tab = self.GetCurrentTab()
        file = tab.file
        if self.AskForFilename(
            defaultFile=file, style=wx.FD_SAVE, **self.DefaultFileDialogOptions()
        ):
            text = self.GetCurrentTabText()
            tab = self.GetCurrentTab()
            tab.file = self.filename
            tab.filedir = self.dirname
            filepath = self.filePath
            if self.filePath:
                fileType = types[self.fileType]
                ext = rt.RichTextBuffer.FindHandlerByType(fileType).GetExtension()
                if not filepath.endswith(ext):
                    filepath += "." + ext
                tab.rtc.SaveFile(filepath, fileType)

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
        pass

    def OnIndentMore(self, event):
        pass

    def OnFont(self, event):
        pass

    def OnColour(self, event):
        pass


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
