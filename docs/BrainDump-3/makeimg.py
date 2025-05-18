import wx.tools.img2py as i
import pathlib as path
import os

mypath = os.getcwd() + '/docs/BrainDump-3'

i.img2py( mypath + '/refresh2.png', mypath+'/imgs.py',append=True)
