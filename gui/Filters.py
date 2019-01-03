from tkinter import Frame, X, Label, Entry, LEFT, RIGHT
import json
class Filter:
    
    def __init__(self, master, text, default):
        self.frame = Frame(master)

        self.textLabel = Label(self.frame, text=text)
        self.textLabel.pack(side=LEFT, fill=X)

        self.entry = Entry(self.frame)
        self.entry.insert(0, default)
        self.entry.pack(side=RIGHT, fill=X)


def buildFilters(master, file="filters.json"):
    with open(file, "r") as f:
        content = json.load(f)

    filters = content.get("FILTERS")
    obs = content.get("OBS")

    for filtr in filters:
        print(filtr)
        text, ent = content["FILTERS"][filtr]
        print(text, ent)
        ftr = Filter(master, text, ent)     
        ftr.frame.pack(fill=X)