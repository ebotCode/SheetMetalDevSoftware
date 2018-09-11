from Tkinter import * 

from PanButtonClass import * 
from ZoomButtonClass import * 
from ShowButtonClass import * 
from RotateClass import * 

class ToolBar:
    def __init__(self,linkerobject):


        self.linkerobject = linkerobject
        self.linkerobject.Add(self,name = "ToolBar")

    def SetFrame(self,frame):
        self.parent1 = frame
        self.GridComponent()
    def GridComponent(self):
        self.frame = Frame(self.parent1)
        self.frame.rowconfigure(0,weight = 1)
        


        self.panbutton = PanButton(self.frame,self.linkerobject)
        self.zoombutton = ZoomButton(self.frame,self.linkerobject)
        self.showbutton = ShowButton(self.frame, self.linkerobject)
        self.rotatebutton = RotateButton(self.frame, self.linkerobject)
        self.panbutton.Grid(row = 0, column = 0)
        self.zoombutton.Grid(row = 0, column = 1)
        self.rotatebutton.Grid(row =0, column = 2)
        self.showbutton.Grid(row = 0, column = 3)
        
    def Grid(self,row = 0, column = 0):
        self.frame.grid(sticky = NW, row = row,column = column)
