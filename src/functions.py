#functions

import os
from pathlib import Path
import shelve

import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s -  %(levelname)s -  %(message)s')

# These 'constants' will be set when the assosiated window is first created 
UNORGANIZEDTEXTSPATH = str(Path.cwd() / Path("UnorganizedTexts"))

PROGRAMNAME = 'BrainDump Notepad'
PROGRAMABOUT = 'A small notepad thing'

MAINWINDOW = ''
MAINNOTEBOOK = ''
MAINTREE = ''
DIRTREE = ''

WILDCARD =  []
CHECKWILDCARDS = ['.txt','.py','.xml','.html']

ALTEVENTTAB = [] #Set in Bind Events
# -----
fileType = 1
filePath = UNORGANIZEDTEXTSPATH
treeDirectory = UNORGANIZEDTEXTSPATH

autosaveTimerLength = 10000

openedFiles = []
projectFiles = []

def DefaultFileDialogOptions():
    pass

#- FUNCTIONS

def GetFileNameandParentDir(path):
    '''
    Returns file's name as:
    'dir/filename.ext'
    '''
    name = Path(path).name
    parent = Path(path).parent.name
    name = str(parent) +"/"+ str(name)
    return name

def LoadPreviousFiles():
    '''
    Use Shelve module to open and load
    previous saved files.
    '''
    shelfFile = shelve.open('openedFiles')
    #Check if there are previous files to open
    #if not, create a new, blank tab
    if 'openedFiles' not in shelfFile:
        CreateNewTab()
    elif len(shelfFile['openedFiles']) <= 0:
        CreateNewTab()
    else:
        for path in shelfFile['openedFiles']:
            if path and Path(path).is_file():
                CreateOpenTab(path)
            else:
                logging.debug('file no exist')   
    if 'currentProject' in shelfFile:
        ChangeProjectTreeDirectory(shelfFile['currentProject'])   
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

def ShelveCurrentlyOpenFiles():
    ChangeOpenFiles()
    shelfFile = shelve.open('openedFiles')
    shelfFile['openedFiles'] = openedFiles
    logging.debug(shelfFile['openedFiles'])
    shelfFile.close()

def ShelveCurrentlyOpenProject():
    shelfFile = shelve.open('openedFiles')
    shelfFile['currentProject'] = MAINTREE.projectFolder
    shelfFile.close()

def SaveAllOpenFiles():
    for page in MAINNOTEBOOK:
        page.rtc.SaveFile()

# ----
# FILE TREE

def UpdateFileTree_nonProjectFiles():
    MAINTREE.DeleteChildren(MAINTREE.UnSaved)
    MAINTREE.DeleteChildren(MAINTREE.UnsortedFiles)
    for file in openedFiles:
        if Path(file).parent == Path(UNORGANIZEDTEXTSPATH):
            name = Path(file).name
            item = MAINTREE.AppendItem(MAINTREE.UnSaved, name, data = [file])
            SetTreeItemImg(item,2,2)
        elif Path(file) not in projectFiles:
            name = Path(file).name
            item = MAINTREE.AppendItem(MAINTREE.UnsortedFiles, name, data =[file])
            SetTreeItemImg(item,2,2)

def WalkProjectDirectory():

    tree = [MAINTREE.projectRoot]

    for folderName, subfolders, filenames in os.walk(MAINTREE.projectFolder):
        logging.debug('The current folder is ' + folderName)
        parent = tree[-1]
        for subfolder in subfolders:
            logging.debug('SUBFOLDER OF ' + folderName + ': ' + subfolder)
            name = Path(subfolder).name
            filepath = os.path.join(folderName, subfolder)
            tree.append(MAINTREE.AppendItem(parent, name, data = [filepath]))
            MAINTREE.SetItemBold(tree[-1], bold=True)
            SetTreeItemImg(tree[-1])

        for filename in filenames:
            logging.debug('FILE INSIDE ' + folderName + ': '+ filename)
            name = Path(filename).name
            filepath = os.path.join(folderName, filename)
            item = MAINTREE.AppendItem(parent, name, data = [filepath])
            SetTreeItemImg(item, norm=2, exp=2)

def ChangeProjectTreeDirectory(dir):
    MAINTREE.DeleteChildren(MAINTREE.Project)
    MAINTREE.projectFolder = dir
    MAINTREE.projectRoot = MAINTREE.AppendItem(MAINTREE.Project, Path(MAINTREE.projectFolder).name)
    SetTreeItemImg(MAINTREE.projectRoot)
    WalkProjectDirectory()

def SetTreeItemImg(item, norm=0, exp=1):
    MAINTREE.SetItemImage(item, MAINTREE.file_img[norm], MAINTREE.normal)
    MAINTREE.SetItemImage(item, MAINTREE.file_img[exp], MAINTREE.expanded)

#--

def GetTabFromFilename(path):
    for page in MAINNOTEBOOK:
        file = page.rtc.GetFilename()
        if path == file:
            id = MAINNOTEBOOK.GetPageIndex(page)
            MAINNOTEBOOK.SetSelection(id)
            logging.debug('switch to page done')

def GetCurrentTab(eventyes = False, id = 0):
    if eventyes and id in ALTEVENTTAB:
        tab = MAINNOTEBOOK.GetPage(MAINWINDOW.tabPopPage)
    else:
        tab = MAINNOTEBOOK.GetCurrentPage()
    return tab

def CreateOpenTab(path):
        name = GetFileNameandParentDir(path)
        newTab = MAINNOTEBOOK.NewTabPanel(MAINNOTEBOOK)
        MAINNOTEBOOK.AddPage(newTab, name)
        newTab.rtc.LoadFile(str(path), fileType)

        if Path(path).parent == UNORGANIZEDTEXTSPATH:
            newTab.rtc.isSaved = False
            logging.debug('not saved %s',newTab.isSaved)
        else:
            newTab.isSaved = True
            logging.debug('saved %s',newTab.isSaved)
        #Change to recently opened
        num = MAINNOTEBOOK.GetPageCount()
        MAINNOTEBOOK.SetSelection(num-1)
        ChangeOpenFiles()
        return newTab

def CreateNewTab(name = 'New Tab'):
    '''Create new blank file/tab/page'''
    newTab = MAINNOTEBOOK.NewTabPanel(MAINNOTEBOOK)
    # CREATE INITIAL SAVE FILE
    file_exists = True
    i = 1
    while file_exists:
        new_file = str(i) + '.txt'
        new_file_path = UNORGANIZEDTEXTSPATH/Path(new_file)
        if new_file_path.is_file():
            i+=1
        else: 
            # SAVE FILE WITH AVAILABLE FILENAME
            newTab.rtc.SaveFile(str(new_file_path))
            name = GetFileNameandParentDir(new_file_path)
            MAINNOTEBOOK.AddPage(newTab, name)
            MAINNOTEBOOK.SetSelection(MAINNOTEBOOK.GetPageIndex(newTab))
            file_exists = False
    ChangeOpenFiles()
    return newTab

#----

def OnExitProgram():
    '''Functions common to all functions that close the program'''
    ShelveCurrentlyOpenFiles()
    ShelveCurrentlyOpenProject()
    MAINWINDOW._mgr.onClose()

# ---


