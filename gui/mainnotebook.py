# MainNotebook.py
import wx
import wx.richtext as rt
import wx.lib.agw.aui as aui  # Tab notebooks


# ------
class TabPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY,style=wx.BORDER_NONE)
        self.rtc = rt.RichTextCtrl(self, style=wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER)

        self.isSaved = False

        layout = wx.BoxSizer(wx.HORIZONTAL)
        layout.Add(self.rtc, proportion=1, border=0, flag=wx.ALL | wx.EXPAND)
        self.SetSizer(layout)


class MainNotebook(aui.auibook.AuiNotebook):
    def __init__(self, parent):
        super().__init__(
            parent,
            id=wx.ID_ANY,
            agwStyle=aui.AUI_NB_TOP
            | aui.AUI_NB_TAB_SPLIT
            | aui.AUI_NB_TAB_MOVE
            | aui.AUI_NB_SCROLL_BUTTONS
            | aui.AUI_NB_CLOSE_ON_ALL_TABS
            | aui.AUI_NB_MIDDLE_CLICK_CLOSE,
        )
        self.parent = parent
        _AddRTCHandlers(self)

    def __getitem__(self, index):
        """More pythonic way to get a specific page, also useful for iterating
        over all pages, e.g: for page in notebook: ..."""
        if index < self.GetPageCount():
            return self.GetPage(index)
        else:
            raise IndexError

    def NewTabPanel(self, parent):
        newTab = TabPanel(parent)
        return newTab


def _AddRTCHandlers(self):
    # make sure we haven't already added them.
    if rt.RichTextBuffer.FindHandlerByType(rt.RICHTEXT_TYPE_HTML) is not None:
        return

    rt.RichTextBuffer.AddHandler(rt.RichTextHTMLHandler())
    rt.RichTextBuffer.AddHandler(rt.RichTextXMLHandler())
    rt.RichTextBuffer.AddHandler(rt.RichTextPlainTextHandler())

    rt.RichTextBuffer.AddHandler(
        rt.RichTextXMLHandler(name="BrainDump XML", ext="braindump", type=99)
    )
    rt.RichTextBuffer.AddHandler(
        rt.RichTextPlainTextHandler(name="Python", ext="py", type=99)
    )

    # This is needed for the view as HTML option since we tell it
    # to store the images in the memory file system.
    wx.FileSystem.AddHandler(wx.MemoryFSHandler())

    # TODO: Do we have the wildcard behing handled here too?!
    self.WILDCARD = rt.RichTextBuffer.GetExtWildcard()
    self.WILDCARD = list(self.WILDCARD)
