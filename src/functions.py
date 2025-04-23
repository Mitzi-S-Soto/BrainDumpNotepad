#functions
from pathlib import Path
import shelve

import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s -  %(levelname)s -  %(message)s')

# These 'constants' will be set when the assosiated window is
# first created 
UNORGANIZEDTEXTSPATH = str(Path.cwd() / Path("UnorganizedTexts"))

PROGRAMNAME = 'BrainDump Notepad'
PROGRAMABOUT = 'A small notepad thing'

MAINWINDOW = ''
MAINNOTEBOOK = ''
MAINTREE = ''

WILDCARD = "Text (*.txt)|*.txt|" "Python (*.py)|*py|" "XML (*.xml)|*xml" "HTML (*.html)|*html"

ALTEVENTTAB = [] #Set in Bind Events

# -----

path = Path.cwd()
dirname = "."
fileType = 1
filePath = UNORGANIZEDTEXTSPATH
filename = ' '

autosaveTimerLength = 10000

openedFiles = []

def DefaultFileDialogOptions():
        """Return a dictionary with file doalog options that
        can be used in bot the save f ile as well as the open file dialog"""
        return dict(
            message = "Choose a file :",
            defaultDir = filePath,
            wildcard = WILDCARD,
        )

#---

def LoadPreviousFiles():
    shelfFile = shelve.open('openedFiles')
    if 'openedFiles' not in shelfFile:
        CreateNewTab()
    elif len(shelfFile['openedFiles']) <= 0:
        CreateNewTab()
    else:
        for file in shelfFile['openedFiles']:
            path = file
            if path and Path(file).is_file():
                name = Path(path).name
                tab = CreateOpenTab(name)
                tab.rtc.LoadFile(path)
                if Path(path).parent == Path(UNORGANIZEDTEXTSPATH):
                    tab.rtc.isSaved = False
                else:
                    tab.rtc.isSaved = True
            else:
                 logging.debug('file no exist')       
    shelfFile.close()
    ChangeOpenFiles()

def ChangeOpenFiles(tab = False):
    openedFiles.clear()
    for page in MAINNOTEBOOK:
        file = page.rtc.GetFilename()
        if not tab:
            openedFiles.append(file)
        elif tab.rtc.GetFilename() != file:
            openedFiles.append(file)
    #TODO: Change FileTreee when Changing Open Files
    UpdateFileTree_nonProjectFiles()
    logging.debug(openedFiles)

def UpdateFileTree_nonProjectFiles():
    MAINTREE.DeleteChildren(MAINTREE.UnSaved)
    MAINTREE.DeleteChildren(MAINTREE.UnsortedFiles)
    for file in openedFiles:
        if Path(file).parent == Path(UNORGANIZEDTEXTSPATH):
            name = Path(file).name
            MAINTREE.AppendItem(MAINTREE.UnSaved, name, data = {'path': file})
        else:
            name = Path(file).name
            MAINTREE.AppendItem(MAINTREE.UnsortedFiles, name, data = {'path': file})
            logging.debug('unsorted file %s', name)

#for page

def ShelveCurrentlyOpenFiles():
    ChangeOpenFiles()
    shelfFile = shelve.open('openedFiles')
    shelfFile['openedFiles'] = openedFiles
    logging.debug(shelfFile['openedFiles'])
    shelfFile.close()

def SaveAllOpenFiles():
    for page in MAINNOTEBOOK:
        page.rtc.SaveFile()
        logging.debug('page')

# ----

def GetFilesTab(info):
    for page in MAINNOTEBOOK:
        file = page.rtc.GetFilename()
        if info == file:
            id = MAINNOTEBOOK.GetPageIndex(page)
            MAINNOTEBOOK.SetSelection(id)
            logging.debug('switch to page done')

def GetCurrentTab():
    tab = MAINNOTEBOOK.GetCurrentPage()
    return tab

def GetEventTab(id):
    if id in ALTEVENTTAB:
        tab = MAINWINDOW.tabPopPage
        tab = MAINNOTEBOOK.GetPage(tab)
    else:
        tab = GetCurrentTab()
    return tab

def CreateOpenTab(name = 'Open Tab'):
        newTab = MAINNOTEBOOK.NewTabPanel(MAINNOTEBOOK)
        MAINNOTEBOOK.AddPage(newTab, name)
        #Change to recently opened
        num = MAINNOTEBOOK.GetPageCount()
        MAINNOTEBOOK.SetSelection(num-1)
        ChangeOpenFiles()
        return newTab

def CreateNewTab(name = 'New Tab'):
    '''Create new blank file/tab/page'''
    newTab = MAINNOTEBOOK.NewTabPanel(MAINNOTEBOOK)
    # CREATE INITIAL SAVE FILE
    path = Path.cwd()
    path_UnOrgTexts = path/Path('UnorganizedTexts')
    file_exists = True
    i = 1
    while file_exists:
        new_file = str(i) + '.txt'
        new_file_path = path_UnOrgTexts/Path(new_file)
        if new_file_path.is_file():
            i+=1
        else: 
            # SAVE FILE WITH AVAILABLE FILENAME
            newTab.rtc.SaveFile(str(new_file_path))
            name = Path(new_file_path).name
            MAINNOTEBOOK.AddPage(newTab, name)
            MAINNOTEBOOK.SetSelection(MAINNOTEBOOK.GetPageIndex(newTab))
            file_exists = False
    ChangeOpenFiles()
    return newTab

#----

def OnExitProgram():
    '''Functions common to all functions that close the program'''
    ShelveCurrentlyOpenFiles()
    MAINWINDOW._mgr.onClose()

# ---


