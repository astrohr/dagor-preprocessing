from tkinter import Tk, Frame, Label, Entry, Button, LEFT, RIGHT, BOTTOM
from utils import MinorPlanet


def addObject(objectFrame, row, minorPLanet):
    frame = Frame(objectFrame)

    #name, score, ra...
    name = Label(frame, text=minorPLanet.name)
    remove = Button(frame, text="Remove", command=lambda: frame.destroy())

    remove.grid(row=0, column=0)
    name.grid(row=0, column=1)
    frame.grid(row=row)


class AddObjectPopup:
    def __init__(self, app):
        self.app = app
        
    def _build(self):
        self.window = Tk()
        self.label_name = Label(self.window, text="Name")
        self.label_name.pack(side=LEFT)
        self.entry_name = Entry(self.window)
        self.entry_name.pack(side=RIGHT)

        self.submitObject = Button(self.window, text="Confirm", command=lambda: addObject(self.app.objectFrame, self.app.getRow(), MinorPlanet("K-PAC", 10, 10, 20)))
        #self.submitObject.configure(self.submitObject.callback)
        self.submitObject.pack(side=BOTTOM)

    def center(self):
        w = 400
        h = 200
        ws = self.window.winfo_screenwidth()
        hs = self.window.winfo_screenheight()
        # calculate position x, y
        x = (ws/2) - (w/2)    
        y = (hs/2) - (h/2)   
        self.window.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def getMinorPlanet(self):
        #Test
        return MinorPlanet("K-PAC", 30, 20, 21)

    def run(self):
        self._build()
        self.center()
        #self.window.mainloop()

    def shut(self):
        self.window.destroy()
