import wx
import wx.html
from wx.lib.wordwrap import wordwrap

import webbrowser


class AboutDlg(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, wx.ID_ANY, title="About", size=(400, 400))
        html = wxHTML(self)

        html.SetPage(
            
            "<center><img src='gui/iconBD.png'></img>"
            "<br><br>"
            "<h2>BrainDump Notepad</h2><"
            "<p>A simple text editor by Mitzi S. Soto</p>"
            "<p><b>Software used:</b></p><b>"
            '<p><b><a href="http://www.python.org">Python</a></b></p>'
            '<p><b><a href="http://www.wxpython.org">wxPython</a></b></p>'
            "<br>"
            '<p>Icons by: <a href="https://icons8.com">Icons8</a></p></center>'
        )


class wxHTML(wx.html.HtmlWindow):
    def OnLinkClicked(self, link):
        webbrowser.open(link.GetHref())
