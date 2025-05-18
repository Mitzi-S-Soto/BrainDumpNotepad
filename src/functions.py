# functions.py
""" """

import os
from pathlib import Path
import shelve
import send2trash as trash

import logging

logging.basicConfig(
    level=logging.DEBUG, format=" %(asctime)s -  %(levelname)s -  %(message)s"
)


"""#############
CONSTANTS
These 'constants' will be set when the
assosiated window is first created 
##################"""
HOMEPATH = Path.home()
BDNPATH = str(HOMEPATH/Path('BrainDump'))
UNORGANIZEDTEXTSPATH = str(BDNPATH / Path("UnorganizedTexts"))
SHELFFILE = BDNPATH / Path('shelffile')

MAINWINDOW = ""
MAINNOTEBOOK = ""
MAINTREE = ""

WILDCARD = (
    "txt",
    "xml",
    "ox",
    "py",
)  # TODO: Make this work with the function that needs it

ALTEVENTTAB = []  # Set in Bind Events

########
# NOT QUITE CONSTANTS

fileType = 1
filePath = str(HOMEPATH)
treeDirectory = UNORGANIZEDTEXTSPATH

autosaveTimerLength = 20000

openedFiles = []  # projects open editor
projectFiles = []  # files in project tree; not nessisarly open in editor


def DefaultFileDialogOptions():
    pass


##############
#  FUNCTIONS
##############


def CreateUnorganizedTextsFolder():
    """
    Create needed file directory in user directory
    """
    if not os.path.exists(UNORGANIZEDTEXTSPATH):
        os.makedirs(UNORGANIZEDTEXTSPATH)
        logging.info(f"Folder created.")
    else:
        logging.info(f"Folder already exists.")


def GetFileNameandParentDir(path):
    """
    Returns file's name as:
    'dir/filename.ext'
    Used to make title for tabs
    """
    name = Path(path).name
    parent = Path(path).parent.name
    name = str(parent) + "/" + str(name)
    return name


def LoadPreviousFiles():
    """
    Use Shelve module to open and load
    previous saved files.
    """
    shelfFile = shelve.open(SHELFFILE)
    # Check if there are previous files to open
    # if not, create a new, blank tab
    if "openedFiles" not in shelfFile:
        CreateNewTab()
    elif len(shelfFile["openedFiles"]) <= 0:
        CreateNewTab()
    else:
        for path in shelfFile["openedFiles"]:
            if path and Path(path).is_file():
                CreateOpenTab(path)
            else:
                logging.debug("file doesn't exist")
    if "currentProject" in shelfFile:
        ChangeProjectTreeDirectory(shelfFile["currentProject"])
    if "projectFiles" in shelfFile:
        projectFiles = shelfFile["projectFiles"]
    shelfFile.close()
    ChangeOpenFiles()


def ChangeOpenFiles(tab=False):
    openedFiles.clear()
    for page in MAINNOTEBOOK:
        file = page.rtc.GetFilename()
        if not tab:
            openedFiles.append(file)
        elif tab.rtc.GetFilename() != file:
            openedFiles.append(file)
    UpdateFileTree()


def ShelveCurrentlyOpenFiles():
    ChangeOpenFiles()
    shelfFile = shelve.open(SHELFFILE)
    shelfFile["openedFiles"] = openedFiles
    shelfFile.close()


def ShelveCurrentlyOpenProject():
    shelfFile = shelve.open(SHELFFILE)
    shelfFile["projectFiles"] = projectFiles
    shelfFile["currentProject"] = MAINTREE.projectFolder
    shelfFile.close()


def SaveAllOpenFiles():
    for page in MAINNOTEBOOK:
        page.rtc.SaveFile()


def DeleteTempSave(tab):
    if not tab.isSaved:
        delFile = tab.rtc.GetFilename()
        trash.send2trash(delFile)
    else:
        pass


# ----
# FILE TREE


def UpdateFileTree():
    MAINTREE.DeleteChildren(MAINTREE.UnSaved)
    MAINTREE.DeleteChildren(MAINTREE.UnsortedFiles)
    for file in openedFiles:
        if Path(file).parent == Path(UNORGANIZEDTEXTSPATH):
            name = Path(file).name
            item = MAINTREE.AppendItem(MAINTREE.UnSaved, name, data=[file])
            MAINTREE.setText(item)
            SetTreeItemImg(item, 3, 3)
        elif file not in projectFiles:
            name = Path(file).name
            item = MAINTREE.AppendItem(MAINTREE.UnsortedFiles, name, data=[file])
            MAINTREE.setText(item)
            SetTreeItemImg(item, 3, 3)
    #ChangeProjectTreeDirectory()
    FindOpenProjectItems()


def FindOpenProjectItems():
    cookie = 0
    root = MAINTREE.projectRoot
    if isinstance(root, str):
        return
    (child, cookie) = MAINTREE.GetFirstChild(root)
    while child.IsOk():
        data = MAINTREE.GetItemData(child)
        if data:
            if data[0] in openedFiles:
                logging.debug("match found")
                MAINTREE.SetItemImage(child, MAINTREE.file_img[3])
            else:
                MAINTREE.SetItemImage(child, MAINTREE.file_img[2])
        else:
            logging.debug("no dat?")
        (child, cookie) = MAINTREE.GetNextChild(root, cookie)


def WalkProjectDirectory():

    tree = [MAINTREE.projectRoot]
    projectFiles.clear()

    for folderName, subfolders, filenames in os.walk(MAINTREE.projectFolder):
        parent = tree[-1]
        for subfolder in subfolders:
            name = Path(subfolder).name
            filepath = os.path.join(folderName, subfolder)
            tree.append(MAINTREE.AppendItem(parent, name, data=[filepath]))
            MAINTREE.SetItemFont(tree[-1], MAINTREE.font)
            SetTreeItemImg(tree[-1])

        for filename in filenames:
            name = Path(filename).name
            filepath = os.path.join(folderName, filename)
            projectFiles.append(filepath)
            item = MAINTREE.AppendItem(parent, name, data=[filepath])
            MAINTREE.setText(item)
            SetTreeItemImg(item, norm=2, exp=2)


def ChangeProjectTreeDirectory(dir=""):
    MAINTREE.DeleteChildren(MAINTREE.Project)
    if not dir == "":
        MAINTREE.projectFolder = dir
    MAINTREE.projectRoot = MAINTREE.AppendItem(
        MAINTREE.Project, Path(MAINTREE.projectFolder).name
    )
    MAINTREE.setText(MAINTREE.projectRoot)
    SetTreeItemImg(MAINTREE.projectRoot)
    WalkProjectDirectory()


def SetTreeItemImg(item, norm=0, exp=1):
    MAINTREE.SetItemImage(item, MAINTREE.file_img[norm], MAINTREE.normal)
    MAINTREE.SetItemImage(item, MAINTREE.file_img[exp], MAINTREE.expanded)


# --


def GetTabFromFilename(path):
    for page in MAINNOTEBOOK:
        file = page.rtc.GetFilename()
        if path == file:
            id = MAINNOTEBOOK.GetPageIndex(page)
            MAINNOTEBOOK.SetSelection(id)


def GetCurrentTab(eventyes=False, id=0):
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
    else:
        newTab.isSaved = True
    # Change to recently opened
    num = MAINNOTEBOOK.GetPageCount()
    MAINNOTEBOOK.SetSelection(num - 1)
    ChangeOpenFiles()
    return newTab


def CreateNewTab(name="New Tab"):
    """Create new blank file/tab/page"""
    newTab = MAINNOTEBOOK.NewTabPanel(MAINNOTEBOOK)
    # CREATE INITIAL SAVE FILE
    file_exists = True
    i = 1
    while file_exists:
        new_file = str(i) + ".txt"
        new_file_path = UNORGANIZEDTEXTSPATH / Path(new_file)
        if new_file_path.is_file():
            i += 1
        else:
            # SAVE FILE WITH AVAILABLE FILENAME
            newTab.rtc.SaveFile(str(new_file_path))
            name = GetFileNameandParentDir(new_file_path)
            MAINNOTEBOOK.AddPage(newTab, name)
            MAINNOTEBOOK.SetSelection(MAINNOTEBOOK.GetPageIndex(newTab))
            file_exists = False
    ChangeOpenFiles()
    return newTab


# ----


def OnExitProgram():
    """Functions common to all functions that close the program"""
    ShelveCurrentlyOpenFiles()
    ShelveCurrentlyOpenProject()
    MAINWINDOW._mgr.onClose()


# ---
