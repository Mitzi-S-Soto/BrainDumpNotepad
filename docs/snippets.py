
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



    def SetFontStyle(self, fontColor = None, fontBgColor = None, fontFace = None, fontSize = None,
                     fontBold = None, fontItalic = None, fontUnderline = None):
        if fontColor:
            self.textAttr.SetTextColour(fontColor)
        if fontBgColor:
            self.textAttr.SetBackgroundColour(fontBgColor)
        if fontFace:
            self.textAttr.SetFontFaceName(fontFace)
        if fontSize:
            self.textAttr.SetFontSize(fontSize)
        if fontBold is not None:
            if fontBold:
                self.textAttr.SetFontWeight(wx.FONTWEIGHT_BOLD)
            else:
                self.textAttr.SetFontWeight(wx.FONTWEIGHT_NORMAL)
        if fontItalic is not None:
            if fontItalic:
                self.textAttr.SetFontStyle(wx.FONTSTYLE_ITALIC)
            else:
                self.textAttr.SetFontStyle(wx.FONTSTYLE_NORMAL)
        if fontUnderline is not None:
            if fontUnderline:
                self.textAttr.SetFontUnderlined(True)
            else:
                self.textAttr.SetFontUnderlined(False)
        self.rtc.SetDefaultStyle(self.textAttr)




    def OnFileViewHTML(self, evt):
        # Get an instance of the html file handler, use it to save the
        # document to a StringIO stream, and then display the
        # resulting html text in a dialog with a HtmlWindow.
        handler = rt.RichTextHTMLHandler()
        handler.SetFlags(rt.RICHTEXT_HANDLER_SAVE_IMAGES_TO_MEMORY)
        handler.SetFontSizeMapping([7,9,11,12,14,22,100])

        stream = BytesIO()
        if not handler.SaveStream(self.rtc.GetBuffer(), stream):
            return

        import wx.html
        dlg = wx.Dialog(self, title="HTML", style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        html = wx.html.HtmlWindow(dlg, size=(500,400), style=wx.BORDER_SUNKEN)
        html.SetPage(stream.getvalue())
        btn = wx.Button(dlg, wx.ID_CANCEL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(html, 1, wx.ALL|wx.EXPAND, 5)
        sizer.Add(btn, 0, wx.ALL|wx.CENTER, 10)
        dlg.SetSizer(sizer)
        sizer.Fit(dlg)

        dlg.ShowModal()

        handler.DeleteTemporaryImages()


    def AddRTCHandlers(self):
        # make sure we haven't already added them.
        if rt.RichTextBuffer.FindHandlerByType(rt.RICHTEXT_TYPE_HTML) is not None:
            return

        # This would normally go in your app's OnInit method.  I'm
        # not sure why these file handlers are not loaded by
        # default by the C++ richtext code, I guess it's so you
        # can change the name or extension if you wanted...
        rt.RichTextBuffer.AddHandler(rt.RichTextHTMLHandler())
        rt.RichTextBuffer.AddHandler(rt.RichTextXMLHandler())

        # ...like this
        rt.RichTextBuffer.AddHandler(rt.RichTextXMLHandler(name="Other XML",
                                                           ext="ox",
                                                           type=99))

        # This is needed for the view as HTML option since we tell it
        # to store the images in the memory file system.
        wx.FileSystem.AddHandler(wx.MemoryFSHandler())


