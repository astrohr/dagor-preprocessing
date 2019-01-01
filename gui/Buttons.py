from tkinter import *
from utils import downloadList

class DownloadButton(Button):
    def __init__(self, app, *args, **kwargs):
        self.app = app
        super(DownloadButton, self).__init__(*args, **kwargs)

    def callback(self):
        self.app.obtained = downloadList()
        self.app.text.print(self.app.obtained)


class AddButton(Button):
    def __init__(self, app, *args, **kwargs):
        self.app = app
        super(AddButton, self).__init__(*args, **kwargs)

    def callback(self):
        self.app.AddObjectPopup.mainloop()

