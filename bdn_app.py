
import wx
import gui.gui_main as gui_main

import src.functions as f
import src.bind_events as bind


class MyApp(wx.App):

    def OnInit(self):
        f.CreateUnorganizedTextsFolder()
        
        f.MAINWINDOW = gui_main.MainWindow()

        bind.StartBind(self)
     
        f.LoadPreviousFiles()
     
        f.MAINWINDOW.Show(True)
        return True

##############
class main:
    def __init__(self):
        app = MyApp(False)
        app.MainLoop()

if __name__ == "__main__":
    main()