
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
