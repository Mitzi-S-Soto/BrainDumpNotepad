# Brain Dump Notepad Application
"""
Developer: Mitzi S. Soto

#TODO: Create functions to load last opened docs
#TODO: Function to delete old temp file when saving and/or

SavePerspective(self)
Saves the entire user interface layout into an encoded string,
which can then be stored by the application (probably using Config).
When a perspective is restored using LoadPerspective, the entire user
interface will return to the state it was when the perspective was saved.

"""
import sys
import os
from pathlib import Path

import wx
import wx.richtext as rt
import wx.lib.agw.aui as aui  # Tab notebooks

import src.constants as c
import src.functions as f
import src.autosave as autosave
import src.bind_events as bind_events

import gui.aui_mgr as aui_mgr  # our AUI Manager code
import gui.menubar as menubar
import gui.toolbar as toolbar
import gui.treectrls as tree
import gui.mainnotebook as note
import logging

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s -  %(levelname)s -  %(message)s')

#---
class MainWindow(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "BrainDump Notepad", size=(640, 480))

        c.MAINWINDOW = self
        self._SetProperties()

        logging.debug(c.MAINWINDOW)
        ''' --------
            Create GUI
            -------- '''

        menubar.CreateMenuBar(self)
        self.toolbar = toolbar.MakeToolBar(self)
        self.Tree = tree.FileTree(self)
        self.notebook = note.MainNotebook(self)
        c.MAINNOTEBOOK = self.notebook
        c.MAINNOTEBOOK.CreateNewTab()
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
        bind_events.StartBind(self)

        # ------------
    
    def _SetProperties(self):
       f.SetFunctionVariables()

#############

class MyApp(wx.App):

    def OnInit(self):
        frame = MainWindow()
        frame.Show(True)
        return True

##############
class main:
    def __init__(self):
        app = MyApp(False)
        app.MainLoop()


if __name__ == "__main__":
    main()
