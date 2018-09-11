
from Tkinter import* 
from tkMessageBox import*
from tkFileDialog import askopenfilename,asksaveasfilename
import os 

class SaveDialog:
    def __init__(self,parent):
        self.name = None
        b = os.getcwd()
        defaultfilepath = os.path.join(b ,"SheetMetalWork")
        self.initialdir = defaultfilepath
        self.defaultext = ".cd"
        self.parent = parent
        self.filetypes = [('cdn','*.cd')]
        
        

    def SaveFile(self):
        filepath = asksaveasfilename(initialdir = self.initialdir,\
                                     defaultextension = self.defaultext,\
                                     parent = self.parent,filetypes = self.filetypes)
        
        if filepath:
            return str(filepath)
        else:
            return None
    def SetInitialDir(self,dirname):
        self.initialdir = dirname

class OpenDialog:
    def __init__(self,parent):
        self.name = None
        b = os.getcwd()
        defaultfilepath = b + "\\Examples"
        self.initialdir = defaultfilepath
        self.defaultext = ".cd"
        self.parent = parent
        self.filetypes = [('cdn','*.cd')]

    def OpenFile(self):
        filepath = askopenfilename(initialdir = self.initialdir,\
                                     defaultextension = self.defaultext,\
                                   parent = self.parent,filetypes = self.filetypes)
        
        if filepath:
            return str(filepath)
        else:
            return None

class WarningDialog:
    def __init__(self,parent):
        self.name = None
        self.parent = parent
                    
    def ShowErrorMessage(self,messagetitle,message):
        showinfo(messagetitle,message,parent = self.parent)

