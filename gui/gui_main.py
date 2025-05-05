#gui_main.py
'''
The main GUI. Pulls all the smaller GUI modules
together into the main module that the application
will call to create.
Trying to keep the GUI as 'dumb' as possible.
Keep any code from 'src' out. Handle the GUI
outside the GUI.
'''
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
        wx.Frame.__init__(self, None, wx.ID_ANY, "BrainDump Notepad", size=(720, 480))
        
        ''' --------
            Create GUI
            -------- '''

        menubar.CreateMenuBar(self)
        self.toolbar = toolbar.MakeToolBar(self)
        self.Tree = tree.FileTree(self)
        self.notebook = note.MainNotebook(self)

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
            aui.AuiPaneInfo().BestSize((150,100))
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

        tabpop.InitTabPopMenu(self)
        # --------
