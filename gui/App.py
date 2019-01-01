from tkinter import *
from utils import *
from configparser import ConfigParser
from Objects import *
from Filters import *
from Console import *
from Buttons import *
from AddPopup import *
import sys
sys.path.insert(0, "../finder/")
import planets

class App(Tk):
    def __init__(self, width, height, *args, **kwargs):
        self.obtained = ""
        self.que = PriorityQue()
        self.width = width
        self.height = height

        #object to be added into objectframe row
        self.row = -1

        super(App, self).__init__(*args, **kwargs)

    def getRow(self):
        self.row += 1
        return self.row


    def _buildRoot(self):
        """
        builds the skeleton which consists of a toolbar
        and master frame (mainFrame) which consists of
        a left and right frame
        """
        self.toolbar = Frame(self, bd=1, relief=RAISED)
        self.toolbar.pack(side=TOP, fill=X)

        self.mainFrame = Frame(self)
        self.mainFrame.pack(fill=BOTH, expand=True, padx=5, pady=5)

        self.leftFrame = Frame(self.mainFrame)
        self.rightFrame = Frame(self.mainFrame)
        self.leftFrame.pack(fill=BOTH, side=LEFT, expand=True)
        self.rightFrame.pack(fill=BOTH, side=RIGHT, expand=True)


    def _buildLeftSubRoot(self):
        """builds the upper and lower left frame subframes"""
        self.filterFrame = Frame(self.leftFrame, bd=1, relief=GROOVE)
        #self.filterFrame = FilterFrame(self.leftFrame, bg=1, relief=GROOVE)
        #self.filterFrame.buildFilters()
        self.filterFrame.pack(fill=BOTH, side=TOP, expand=True, padx=2, pady=2)

        self.buttonFrame = Frame(self.leftFrame, bd=1, relief=GROOVE)
        self.buttonFrame.pack(fill=BOTH, side=BOTTOM, expand=True, padx=5, pady=5)

        self.objectCanvas = Canvas(self.rightFrame, bd=1, relief=GROOVE)
        self.objectCanvas.pack(fill=BOTH, side=TOP, expand=True, padx=5, pady=5) #expand=False


    def _buildRightSubRoot(self):
        """builds the upper and lower right frame subrames"""

        self.consoleFrame = Frame(self.objectCanvas, height=self.width//4)
        self.consoleFrame.pack(fill=BOTH, side=BOTTOM, expand=False)
        self.objectFrame = Frame(self.objectCanvas)

        #configure scrollable canvas
        self.scrollObjects = Scrollbar(self.objectCanvas, orient="vertical", command=self.objectCanvas.yview)
        self.objectCanvas.configure(yscrollcommand=self.scrollObjects.set)
        self.objectCanvas.create_window((4, 4), window=self.objectFrame, anchor="nw")
        self.scrollObjects.pack(side=RIGHT, fill=Y)
        self.objectFrame.bind("<Configure>", lambda event, canvas=self.objectCanvas: self.onFrameConfigure(self.objectCanvas))

        
    def _buildFilters(self):
        buildFilters(self)


    def _buildPopups(self):
        self.addObjectPopup = AddObjectPopup(self)

        #Buttons
    
    def _buildButtons(self):
        """builds the lower left panel"""
        #self.downloadButton = Button(self.buttonFrame, text="Download")
        self.downloadButton = DownloadButton(self, self.buttonFrame, text="Download")
        self.downloadButton.configure(command=self.downloadButton.callback)
        #print(self.downloadButton.app, self.downloadButton.master)
        self.downloadButton.pack()

        self.addButton = AddButton(self, self.buttonFrame, text="Add object")
        self.addButton.configure(command=self.addObjectPopup.run)
        self.addButton.pack()

        #self.addButton = Button(self, text="Add object", command=)

        #self.applyButton = Button(self.buttonFrame, text="Apply filter")# TODO
        #self.applyButton.pack()


    def _buildText(self):
        """builds the lower right panel"""
        self.text = ConsoleText(self.consoleFrame)
        self.text.initialize()
        self.text.pack(side=RIGHT, fill=BOTH, expand=True)
        

    def build(self):
        self._buildRoot()
        self._buildLeftSubRoot()
        self._buildRightSubRoot()

        #Other windows - debug mode
        try:
            self._buildPopups()
        except Exception as e:
            print("_buildPopups failed:", e)

        #Left side stuff
        self._buildFilters()
        self._buildButtons()
        self._buildText()

        #Right side stuff builds right away for proper expansion


    def center(self):
        w = self.width
        h = self.height
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        # calculate position x, y
        x = (ws/2) - (w/2)    
        y = (hs/2) - (h/2)   
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))

        


    @staticmethod
    def onFrameConfigure(canvas):
        """Reset the scroll region to encompass the inner frame"""
        canvas.configure(scrollregion=canvas.bbox("all"))

    
    def loadConfig(self, file="config.ini"):
        cp = ConfigParser()
        cp.read(file)
        self.setupConfig(cp)

    
    def setupConfig(self, cp):
        """cp - config parser or dictionary if manual setup"""
        #[OBS]
        self.obs_code = cp["OBS"]["obs_code"]
        self.continous = cp["OBS"]["continuous"]

        #[FILTER]
        self.min_score = cp["FILTER"]["min_score"]
        self.min_ef_mag = cp["FILTER"]["min_ef_mag"]
        self.min_alt = cp["FILTER"]["min_alt"]
        self.max_scat_xcoo = cp["FILTER"]["max_scat_xcoo"]
        self.max_scat_ycoo = cp["FILTER"]["max_scat_ycoo"]
        self.max_not_seen = cp["FILTER"]["max_not_seen"]
        self.max_sun_alt = cp["FILTER"]["max_sun_alt"]
        self.min_d_from_moon = cp["FILTER"]["min_d_from_moon"]
        self.min_motion_speed = cp["FILTER"]["min_motion_speed"]


    def run(self):
        self.build()
        self.center()
        self.mainloop()


if __name__ == "__main__":
    root = App(800, 600)
    root.loadConfig()
    root.run()
    #manal add object
