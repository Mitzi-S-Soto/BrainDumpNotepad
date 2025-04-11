
    def onSaveAs(self, event):
        tab = self.GetCurrentTab()
        self.dirname = tab.filedir
        file = tab.file
        filepath = Path(self.dirname)/file
        print(filepath)
        if self.AskForFilename(defaultFile=file, style=wx.FD_SAVE, **self.DefaultFileDialogOptions()):
            text = self.GetCurrentTabText()
            tab = self.GetCurrentTab()
            tab.file = self.filename
            tab.filedir = self.dirname
            self.fileType
            filepath = Path(self.dirname)/self.filename
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(text)
            if tab.isSaved == False:
                #TODO: Delete Temp File
                pass
            tab.isSaved = True
