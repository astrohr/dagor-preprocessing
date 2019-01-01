from tkinter import *



#old
class ObjectRow(Frame):
    def __init__(self, minorPlanet, *args, **kwargs):
        self.minorPlanet = minorPlanet
        self._build()

        super(ObjectRow, self).__init__(*args, **kwargs)



    def _build(self):
        self.rm = Button(self, text="Remove", command=lambda: self.destroy())
        self.rm.pack(side=LEFT)

        self.name = Label(self, text=self.minorPlanet.name)
        self.name.pack(side=RIGHT)

        #self.move = Frame(self)
        #self.move.pack(side=RIGHT)

        #self.moveUp = Button(self.frame, text="Up") #command
        #self.moveUp.pack(side=TOP)

        #self.moveDown = Button(self.frame, text="Down") #command
        #self.moveDown.pack(side=BOTTOM)

