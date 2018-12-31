from tkinter import *
from configparser import ConfigParser
from bs4 import BeautifulSoup
import requests
WIDTH = 800
HEIGHT = 600

#Downloads go here
obtained = ""


#Rows (minor planets)
row = 0
isRunning = False

config = ConfigParser()
#Load presets
config.read("config.ini")

#[OBS]
obs_code = config["OBS"]["obs_code"]
continous = config["OBS"]["continuous"]

#[FILTER]
min_score = config["FILTER"]["min_score"]
min_ef_mag = config["FILTER"]["min_ef_mag"]
min_alt = config["FILTER"]["min_alt"]
max_scat_xcoo = config["FILTER"]["max_scat_xcoo"]
max_scat_ycoo = config["FILTER"]["max_scat_ycoo"]
max_not_seen = config["FILTER"]["max_not_seen"]
max_sun_alt = config["FILTER"]["max_sun_alt"]
min_d_from_moon = config["FILTER"]["min_d_from_moon"]
min_motion_speed = config["FILTER"]["min_motion_speed"]

"""Core classes"""
class MinorPlanet:
    def __init__(self, name, ra, de, v):
        self.name = name
        self.ra = ra
        self.de = de
        self.v = v


"""Core functions"""
def center_window(root, w=WIDTH, h=HEIGHT):
    # get screen width and height
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    # calculate position x, y
    x = (ws/2) - (w/2)    
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))


def populate(minorPlanet):
    global objectframe
    global row
    lb = Label(objectframe, text=minorPlanet.name+str(row)) #debug only
    lb.grid(row=row)
    row += 1


def shut(window):
    global isRunning
    isRunning = False
    window.destroy()

def insertText(txt):
    global text
    text.insert("end", "\n<<< {}".format(txt))



"""Button callbacks"""
def downloadNC():
    global obtained
    insertText("downloading...")
    neocp = "https://www.minorplanetcenter.net/iau/NEO/neocp.txt"
    req = requests.get(neocp)
    obtained = req.text
    insertText("obtained:\n"+obtained)



def addObject():
    global isRunning
    #print(isRunning)

    if isRunning:
        pass
    else:
        isRunning = True
        window = Tk()
        window.protocol("WM_DELETE_WINDOW", lambda: shut(window))

        submit = Button(window, text="Submit", command=lambda: populate(mp))
        submit.pack(side=BOTTOM)
        center_window(window, 200, 100)
        window.mainloop()


"""Testing"""
mp = MinorPlanet("ZTF025c", 25, 33, 19)


root = Tk()
root.configure(background="DeepSkyBlue4")

toolbar = Frame(root, bd=1, relief=RAISED)
toolbar.pack(side=TOP, fill=X)
btn1 = Button(toolbar, text="Text", relief=FLAT)
btn1.pack(side=LEFT)

mainframe = Frame(root, bg="DeepSkyBlue3")
mainframe.pack(fill=BOTH, expand=True, padx=5, pady=5)

leftframe = Frame(mainframe, bg="SkyBlue3")
leftframe.pack(fill=BOTH, side=LEFT, expand=True, padx=5, pady=5)

rightframe = Frame(mainframe, bg="DodgerBlue3")
rightframe.pack(fill=BOTH, side=RIGHT, expand=True, padx=5, pady=5)



filterframe = Frame(leftframe, bg="cyan4")
filterframe.pack(fill=BOTH, side=TOP, expand=True, padx=5, pady=5)


buttonframe = Frame(leftframe, bg="SteelBlue3")
buttonframe.pack(fill=BOTH, side=BOTTOM, expand=True, padx=5, pady=5)

objectcanvas = Canvas(rightframe, bg="SteelBlue") # width=500,height=500, scrollregion=(0,0,500,800)


objectframe = Frame(objectcanvas, bg="DeepSkyBlue4")
#objectframe.pack(side=LEFT, expand=False, padx=5, pady=5)


consoleframe = Frame(rightframe, bg="SlateGray2", height=200)
consoleframe.pack(fill=BOTH, side=BOTTOM, expand=False, padx=5, pady=5)


#Frames
frame_obs_code = Frame(filterframe)
frame_obs_code.pack(fill=X)

frame_min_score = Frame(filterframe)
frame_min_score.pack(fill=X)

frame_min_ef_mag = Frame(filterframe)
frame_min_ef_mag.pack(fill=X)

frame_min_alt = Frame(filterframe)
frame_min_alt.pack(fill=X)

frame_max_scat_xcoo = Frame(filterframe)
frame_max_scat_xcoo.pack(fill=X)

frame_max_scat_ycoo = Frame(filterframe)
frame_max_scat_ycoo.pack(fill=X)

frame_not_seen = Frame(filterframe)
frame_not_seen.pack(fill=X)

frame_max_sun_alt = Frame(filterframe)
frame_max_sun_alt.pack(fill=X)

frame_min_d_from_moon = Frame(filterframe)
frame_min_d_from_moon.pack(fill=X)

frame_min_motion_speed = Frame(filterframe)
frame_min_motion_speed.pack(fill=X)




#Frame fillers:
#Obs code
label_obs_code = Label(frame_obs_code, text="Obs. code?")
label_obs_code.pack(side=LEFT)

entry_obs_code = Entry(frame_obs_code)
entry_obs_code.insert(0, obs_code)
entry_obs_code.pack(side=RIGHT)


#Min score
label_min_score = Label(frame_min_score, text="Min. score?")
label_min_score.pack(side=LEFT)

entry_min_score = Entry(frame_min_score)
entry_min_score.insert(0, min_score)
entry_min_score.pack(side=RIGHT)


#Min ef mag
label_min_ef_mag = Label(frame_min_ef_mag, text="Min. ef. magnitude?")
label_min_ef_mag.pack(side=LEFT)

entry_min_ef_mag = Entry(frame_min_ef_mag, text=min_ef_mag)
entry_min_ef_mag.insert(0, min_ef_mag)
entry_min_ef_mag.pack(side=RIGHT)


#Min altitude
label_min_alt = Label(frame_min_alt, text="Min. altitude?")
label_min_alt.pack(side=LEFT)

entry_min_alt = Entry(frame_min_alt)
entry_min_alt.insert(0, min_alt)
entry_min_alt.pack(side=RIGHT)


#Max x scat
label_max_scat_xcoo = Label(frame_max_scat_xcoo, text="Max. scat. in x coordinates?")
label_max_scat_xcoo.pack(side=LEFT)

entry_max_scat_xcoo = Entry(frame_max_scat_xcoo)
entry_max_scat_xcoo.insert(0, max_scat_xcoo)
entry_max_scat_xcoo.pack(side=RIGHT)


#Max y scat
label_max_scat_ycoo = Label(frame_max_scat_ycoo, text="Max. scat. in y coordinates?")
label_max_scat_ycoo.pack(side=LEFT)

entry_max_scat_ycoo = Entry(frame_max_scat_ycoo)
entry_max_scat_ycoo.insert(0, max_scat_ycoo)
entry_max_scat_ycoo.pack(side=RIGHT)




#Max sun alt
label_max_sun_alt = Label(frame_max_sun_alt, text="Max. sun altitude?")
label_max_sun_alt.pack(side=LEFT)

entry_max_sun_alt = Entry(frame_max_sun_alt)
entry_max_sun_alt.insert(0, max_sun_alt)
entry_max_sun_alt.pack(side=RIGHT)

#Min d from moon (on sky)
label_min_d_from_moon = Label(frame_min_d_from_moon, text="Min. distance from moon?")
label_min_d_from_moon.pack(side=LEFT)

entry_min_d_from_moon = Entry(frame_min_d_from_moon)
entry_min_d_from_moon.insert(0, min_d_from_moon)
entry_min_d_from_moon.pack(side=RIGHT)


#Min motion speed (on sky)
label_min_motion_speed = Label(frame_min_motion_speed, text="Min. motion speed?")
label_min_motion_speed.pack(side=LEFT)

entry_min_motion_speed = Entry(frame_min_motion_speed, text="Min. motion speed?")
entry_min_motion_speed.insert(0, min_motion_speed)
entry_min_motion_speed.pack(side=RIGHT)

check = Checkbutton(filterframe, text="Continous observation?")
if continous != "0":
    check.select()
check.pack(side=LEFT)





#Buttons (not including the toolbar)
download = Button(buttonframe, text="Download", command=downloadNC)
download.grid(row=0, column=0, padx=2, pady=2)

apply = Button(buttonframe, text="Apply filter")
apply.grid(row=0, column=1, padx=2, pady=2)

remove = Button(buttonframe, text="Manual removal")
remove.grid(row=0, column=2, padx=2, pady=2)

add = Button(buttonframe, text="Manual add", command=addObject)
add.grid(row=0, column=3, padx=2, pady=2)


#console scrollbar - NOT WORKING, TODO
#scroll = Scrollbar(consoleframe, orient="vertical")
#scroll.pack(side=RIGHT, fill=Y)

#objectcanvas scrollbar
vsb = Scrollbar(objectcanvas, orient="vertical", command=objectcanvas.yview)
objectcanvas.configure(yscrollcommand=vsb.set)
objectcanvas.pack(fill=BOTH, side=TOP, expand=True, padx=5, pady=5) #expand=False?
objectcanvas.create_window((4, 4), window=objectframe, anchor="nw")
vsb.pack(side=RIGHT, fill=Y)


objectframe.bind("<Configure>", lambda event, canvas=objectcanvas: onFrameConfigure(objectcanvas))

text = Text(consoleframe)
text.insert("end", "<<< INITIALIZED!")
text.pack(side=RIGHT, fill=BOTH, expand=True)


#objects






center_window(root)
root.mainloop()
