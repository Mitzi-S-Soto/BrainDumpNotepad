#wxPyExample
'''
SavePerspective(self)
Saves the entire user interface layout into an encoded string, which can then be stored by the application (probably using Config). When a perspective is restored using LoadPerspective, the entire user interface will return to the state it was when the perspective was saved.
'''
import sys
import os
from pathlib import Path
import wx
import wx.stc as stc # StyledTextControl
import wx.lib.agw.aui as aui # Tab notebooks

class Global():
    path = Path.cwd()
    wildcard = "Text (*.txt)|*.txt|"  \
            "Python (*.py)|*py|"  
    openTabs = []
#------
class TabTree(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self,parent=parent, id=wx.ID_ANY)

        self.tree = self.CreateTree()
 
    def CreateTree(self):
        self.Tree = wx.TreeCtrl(self,wx.ID_ANY,wx.DefaultPosition,style = wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS)
        self.root = self.Tree.AddRoot('FileRoot')
        self.UnsortedFiles = self.Tree.AppendItem(self.root,'Unsorted')

        #----
        layout = wx.BoxSizer(wx.HORIZONTAL)
        layout.Add(self.Tree,proportion=1,border=4,flag=wx.ALL|wx.EXPAND)
        self.SetSizer(layout)

class TabPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self,parent=parent, id=wx.ID_ANY)

        self.txt = self.CreateStyledTextCtrl()
 
    def CreateStyledTextCtrl(self):
        self.stTextCtrl = stc.StyledTextCtrl(self)
        self.stTextCtrl.SetWindowStyle(self.stTextCtrl.GetWindowStyle() | wx.DOUBLE_BORDER)
        self.stTextCtrl.StyleSetSpec(stc.STC_STYLE_DEFAULT, "size:12,face:Courier New")
        self.stTextCtrl.SetWrapMode(stc.STC_WRAP_WORD) 
        #----
        layout = wx.BoxSizer(wx.HORIZONTAL)
        layout.Add(self.stTextCtrl, proportion=1,border=0,flag=wx.ALL|wx.EXPAND)
        self.SetSizer(layout)
        #----
        self.stTextCtrl.Bind(stc.EVT_STC_CHANGE, self.OnChangeTxtCtrl)

    def OnChangeTxtCtrl(self, event):
        lines = self.stTextCtrl.GetLineCount()
        width = self.stTextCtrl.TextWidth(stc.STC_STYLE_LINENUMBER, str(lines)+" ")
        self.stTextCtrl.SetMarginWidth(0, width)
        self.flagDirty = True

#------

class MainNotebook(aui.auibook.AuiNotebook):
    def __init__(self,parent):
        super().__init__(parent, id=wx.ID_ANY, agwStyle=aui.AUI_NB_TOP|aui.AUI_NB_TAB_SPLIT|aui.AUI_NB_TAB_MOVE|aui.AUI_NB_SCROLL_BUTTONS|aui.AUI_NB_CLOSE_ON_ALL_TABS|aui.AUI_NB_MIDDLE_CLICK_CLOSE|aui.AUI_NB_DRAW_DND_TAB)
        #Add first tab to notebook
        self.TreeTab = self.CreateNewTab('tree','Files')
        self.CreateNewTab()
        self.SetCloseButton(0, False)
        self.Split( 0, wx.LEFT)
        self.CalculateNewSplitSize()
        

        self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGING, self.OnPageChanging)

    def CreateNewTab(self,tab = 'txt', name = 'New Tab'):
        if tab == 'txt':
            newTab = TabPanel(self)
        elif tab == 'tree':
            newTab = TabTree(self)
        self.AddPage(newTab, name)
        Global.openTabs.append(newTab)

    def OnPageChanged(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        print('OnPageCHnaged, old:%d, new:%d, sel:%d\n' % (old, new, sel))
        event.Skip()
    def OnPageChanging(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        print('OnPageCHnaged, old:%d, new:%d, sel:%d\n' % (old, new, sel))
        event.Skip()

class MainWindow(wx.Frame):

    def __init__(self, filename="noname.txt"):
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "Notebook Tutorial",
                          size=(600,400)
                          )
        #--------
        self.filename = filename
        self.dirname = "."
        self.flagDirty = False
        #--------

        self.notebook = MainNotebook(self)

        self.SetProperties()
        self.CreateMenuBar()
        self.CreateStatusBar()
        self.BindEvents()
           
          #------------

        layout = wx.BoxSizer(wx.HORIZONTAL)
        layout.Add(self.notebook, proportion=1,border=1,flag=wx.ALL|wx.EXPAND)
        self.SetSizer(layout)
        self.Layout()
        self.Show()

    def SetProperties(self):
        self.SetTitle()

    def SetTitle(self):
        # MyFrame.SetTitle overrides wx.Frame.SetTitle,  
        # so we have to call it using super :
        super(MainWindow, self).SetTitle("Editor %s" % self.filename)

    def CreateMenuBar(self):
        menuBar = wx.MenuBar()
        menuFile = wx.Menu()
        menuEdit = wx.Menu()
        menuAbout = wx.Menu()
        
        self.menuFile_Open = menuFile.Append(wx.ID_OPEN,
                                             "&Open"+"\t"+"Ctrl+O",
                                             "Open a new file.")
        menuFile.AppendSeparator()

        self.menuFile_Save = menuFile.Append(wx.ID_SAVE,
                                             "&Save"+"\t"+"Ctrl+S",
                                             "Save the current file.")
        self.menuFile_SaveAs = menuFile.Append(wx.ID_SAVE,
                                             "&Save As"+"\t"+"Ctrl+Shift+S",
                                             "Save file under different name.")
        menuFile.AppendSeparator()

        self.menuFile_RenameTab = menuFile.Append(wx.ID_ANY,"&Rename Tab","Rename current tab")

        self.menuFile_Close = menuFile.Append(wx.ID_EXIT,'&Exit' + "\t" + "Ctrl+X",
                                              "Exit the program")
        #------------
        self.menuEdit_Cut = menuEdit.Append(wx.ID_CUT,
                                            "&Cut" + "\t" + "Ctrl+X",
                                            "Cut")
        self.menuEdit_Copy = menuEdit.Append(wx.ID_COPY,
                                             "&Copy"+"\t"+"Ctrl+C",
                                             "Copy")
        self.menuEdit_Paste = menuEdit.Append(wx.ID_PASTE,
                                             "&Paste"+"\t"+"Ctrl+V",
                                             "Paste")
        menuEdit.AppendSeparator()
        self.menuEdit_Undo = menuEdit.Append(wx.ID_UNDO,
                                             "&Undo"+"\t"+"Ctrl+Z",
                                             "Undo")
        self.menuEdit_Redo = menuEdit.Append(wx.ID_REDO,
                                             "&Redo"+"\t"+"Ctrl+Shift+Z",
                                             "Redo")

        self.menuAbout_Info = menuAbout.Append(wx.ID_ABOUT,"&About"+"\t"+"Ctrl+I","Information about this program")

        #-------

        menuBar.Append(menuFile,"File")
        menuBar.Append(menuEdit,"Edit")
        menuBar.Append(menuAbout,"About")

        self.SetMenuBar(menuBar)

    def BindEvents(self):
        """
        ...
        """
        self.Bind(wx.EVT_MENU, self.onOpen, self.menuFile_Open)
        self.Bind(wx.EVT_MENU, self.onSave, self.menuFile_Save)
        self.Bind(wx.EVT_MENU, self.onSaveAs, self.menuFile_SaveAs)
        self.Bind(wx.EVT_MENU, self.ChangeTabName, self.menuFile_RenameTab)
        self.Bind(wx.EVT_MENU, self.onExit, self.menuFile_Close)
        self.Bind(wx.EVT_MENU, self.OnCut, self.menuEdit_Cut)
        self.Bind(wx.EVT_MENU, self.OnCopy, self.menuEdit_Copy)
        self.Bind(wx.EVT_MENU, self.OnPaste, self.menuEdit_Paste)
        self.Bind(wx.EVT_MENU, self.OnUndo, self.menuEdit_Undo)
        self.Bind(wx.EVT_MENU, self.OnRedo, self.menuEdit_Redo)
        self.Bind(wx.EVT_MENU, self.onAbout, self.menuAbout_Info)

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def DefaultFileDialogOptions(self):
        '''Return a dictionary with file doalog options that
        can be used in bot the save f ile as well as the open file dialog'''
        return dict(message='Choose a file :',
                    defaultDir=self.dirname,
                    wildcard=Global.wildcard)

    def AskForFilename(self, **dialogOptions):
        dialog = wx.FileDialog(self, **dialogOptions)

        if dialog.ShowModal() == wx.ID_OK:
            providedFilename = True
            self.filename  = dialog.GetFilename()
            self.dirname = dialog.GetDirectory()
            #Update the window title with the new filename
            self.SetTitle()
        else:
            providedFilename = False
        dialog.Destroy()
        return providedFilename
 
    def GetCurrentTabText(self):
        tab = self.notebook.GetActiveTabCtrl()
        txt = tab.stTextCtrl.GetValue()
        print(txt)
        return txt

    def onOpen(self, event):
        '''Open a File'''
        if self.AskForFilename(style=wx.FD_OPEN,
                                   **self.DefaultFileDialogOptions()):
            file = open(os.path.join(self.dirname, self.filename), 'r', encoding='utf-8')
            self.stTextCtrl.SetValue(file.read())
            file.close()

    def onSave(self, event):
        text = self.GetCurrentTabText()
        with open(os.path.join(self.dirname, self.filename), 'w', encoding='utf-8') as file:
           file.write(text)

    def onSaveAs(self, event):
        if self.AskForFilename(defaultFile=self.filename, style=wx.FD_SAVE, **self.DefaultFileDialogOptions()):
            self.onSave(event)

    
    def ChangeTabName(self, event):
        ask = wx.TextEntryDialog(self,'Rename Tab:')
        if ask.ShowModal() == wx.ID_OK:
            tab = self.notebook.GetSelection()
            #tab = self.notebook.FindPage(gettab)
            txt = ask.GetValue()
            self.notebook.SetPageText(tab,txt)
            print(f"User entered: {txt}")
        else:
            print("Dialog cancelled")
        ask.Destroy()

    def OnCut(self, event):
        """
        ...
        """
        self.stTextCtrl.Cut()


    def OnCopy(self, event):
        """
        ...
        """
        self.stTextCtrl.Copy()


    def OnPaste(self, event):
        """
        ...
        """
        self.stTextCtrl.Paste()


    def OnUndo(self, event):
        """
        ...
        """
        self.stTextCtrl.Undo()


    def OnRedo(self, event):
        """
        ...
        """
        self.stTextCtrl.Redo()

    def onAbout(self, event):
            abt = wx.MessageDialog(self, "A small text editor", "About Editor", wx.OK)
            abt.ShowModal()
            abt.Destroy()

    def onExit(self, event):
        self.Close(True)  

    def OnCloseWindow(self, event):
        """
        Quit and destroy application.
        """
        self.Destroy()
#----
class MyApp(wx.App):

    def OnInit(self):
        self.installDir = os.path.split(os.path.abspath(sys.argv[0]))[0]

        frame = MainWindow()
        self.SetTopWindow(frame)
        frame.Show(True)
        return True


    def GetInstallDir(self):

        return self.installDir
    
#################################
def main():
    app = MyApp(False)

    
    app.MainLoop()
    #app.GetCurrentTabText()
    

if __name__ == "__main__":
    main()
