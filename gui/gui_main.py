# gui_main.py
"""
The main GUI. Pulls all the smaller GUI modules
together into the main module that the application
will call to create.
Trying to keep the GUI as 'dumb' as possible.
Keep any code from 'src' out. Handle the GUI
outside the GUI.
"""
import wx
import wx.lib.agw.aui as aui  # Tab notebooks

import gui.aui_mgr as aui_mgr  # our AUI Manager code
import gui.menubar as menubar
import gui.toolbar as toolbar
import gui.treectrls as tree
import gui.mainnotebook as note
import gui.popmenu_tab as tabpop


class MainWindow(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "BrainDump Notepad", size=(850, 500))

        """ --------
            Create GUI
            -------- """
        self.font = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Arial")
        self.SetFont(self.font)

        menubar.CreateMenuBar(self)
        self.toolbar = toolbar.MakeToolBar(self)
        self.Tree = tree.FileTree(self)
        self.notebook = note.MainNotebook(self)

        self.Tree.SetFont(self.font)
        self.notebook.SetFont(self.font)

        self._mgr = aui_mgr.Mgr(self)
        self._mgr.AddPane(
            self.tbar_panel,
            aui.AuiPaneInfo()
            .Top()
            .Dockable(False)
            .Floatable(False)
            .Resizable(False)
            .CaptionVisible(False)
            .CloseButton(False)
            .PaneBorder(False)
        )
        self._mgr.AddPane(
            self.Tree,
            aui.AuiPaneInfo()
            .BestSize((250, 100))
            .Left()
            .CaptionVisible(True)
            .CloseButton(False)
            .TopDockable(False)
            .BottomDockable(False)
            .Floatable(False),
        )
        self._mgr.AddPane(self.notebook, aui.AuiPaneInfo().CenterPane().PaneBorder(False))
        self._mgr.Update()

        self.CreateStatusBar()

        tabpop.InitTabPopMenu(self)
        # --------
