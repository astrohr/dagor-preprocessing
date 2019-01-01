from tkinter import *

class ConsoleText(Text):

    def initialize(self):
        self.insert("end", "<<< INITIALIZED")

    def print(self, content):
        self.insert("end", "\n<<< "+str(content))
