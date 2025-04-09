
#import sys
#import os
from pathlib import Path
import wx
import wx.stc as stc # StyledTextControl
import wx.richtext as rt
import wx.lib.agw.aui as aui # Tab notebooks

#------
class TabPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self,parent=parent, id=wx.ID_ANY)
        self.txt = self.CreateRichTextCtrl()
        self.filedir = ''
        self.file = ''
        self.isSaved = False
 
    def CreateRichTextCtrl(self):
        self.rtc = rt.RichTextCtrl(self, style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER)
        #----
        layout = wx.BoxSizer(wx.HORIZONTAL)
        layout.Add(self.rtc, proportion=1,border=0,flag=wx.ALL|wx.EXPAND)
        self.SetSizer(layout)
    
    def SetFontStyle(self, fontColor = None, fontBgColor = None, fontFace = None, fontSize = None,
                     fontBold = None, fontItalic = None, fontUnderline = None):
        if fontColor:
            self.textAttr.SetTextColour(fontColor)
        if fontBgColor:
            self.textAttr.SetBackgroundColour(fontBgColor)
        if fontFace:
            self.textAttr.SetFontFaceName(fontFace)
        if fontSize:
            self.textAttr.SetFontSize(fontSize)
        if fontBold is not None:
            if fontBold:
                self.textAttr.SetFontWeight(wx.FONTWEIGHT_BOLD)
            else:
                self.textAttr.SetFontWeight(wx.FONTWEIGHT_NORMAL)
        if fontItalic is not None:
            if fontItalic:
                self.textAttr.SetFontStyle(wx.FONTSTYLE_ITALIC)
            else:
                self.textAttr.SetFontStyle(wx.FONTSTYLE_NORMAL)
        if fontUnderline is not None:
            if fontUnderline:
                self.textAttr.SetFontUnderlined(True)
            else:
                self.textAttr.SetFontUnderlined(False)
        self.rtc.SetDefaultStyle(self.textAttr)


class MainNotebook(aui.auibook.AuiNotebook):
    def __init__(self,parent):
        self.openTabs = []
        super().__init__(parent, id=wx.ID_ANY, agwStyle=aui.AUI_NB_TOP|aui.AUI_NB_TAB_SPLIT|aui.AUI_NB_TAB_MOVE|aui.AUI_NB_SCROLL_BUTTONS|aui.AUI_NB_CLOSE_ON_ALL_TABS|aui.AUI_NB_MIDDLE_CLICK_CLOSE)
        
        #Add first tab to notebook
        #TODO: Create functions to load last opened docs
        self.CreateNewTab()
        self.CreateNewTab()

        self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.OnPageClose)
        
        #self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        #self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGING, self.OnPageChanging)

    def CreateNewTab(self, name = 'New Tab'):
        '''Create new blank file/tab/page'''
        newTab = TabPanel(self)
        self.AddPage(newTab, name)

        path = Path.cwd()
        path_UnOrgTexts = path/Path('UnorganizedTexts')
        file_exists = True
        i = 1
        while file_exists:
            new_file = str(i)+ '.txt'
            new_file_path = path_UnOrgTexts/Path(new_file)
            if new_file_path.is_file():
                i+=1
            else:
                with open(new_file_path, 'w', encoding='utf-8') as file:
                    file.write('')
                    newTab.filedir = str(path_UnOrgTexts)
                    newTab.file = str(new_file)
                    print(Path(newTab.filedir))
                    print(Path(newTab.file))
                file_exists = False
        self.openTabs.append(newTab)

    def OnPageClose(self, event):
        tab = self.GetCurrentPage()
        text = tab.rtc.GetValue()
        filepath = Path(tab.filedir)/tab.file
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(text)

    def OnPageChanged(self, event):
        pass

    def OnPageChanging(self, event):
        pass


