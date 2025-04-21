# AUIMgr.py
import wx.lib.agw.aui as aui # Tab notebooks

class Mgr(aui.AuiManager):
    """
    AUI Manager class
    """
    _allManagers = []

    def __init__(self, managed_window):
        """Constructor"""
        aui.AuiManager.__init__(self)
        self.SetManagedWindow(managed_window)
        Mgr._allManagers.append(self)
    
    @classmethod
    def onClose(cls):
        for mgr in Mgr._allManagers:
            mgr.UnInit()

