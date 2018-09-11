
from Tkinter import* 

class DisplayLabel:
    def __init__(self, linkerobject):
        
        self.linkerobject = linkerobject
        self.linkerobject.Add(self,name = "DisplayLabel")

        
        self.posvariable = StringVar()
        self.posvariable.set('x=0,y =0')

    def SetFrame(self,frame):
        self.parent1 = frame
        self.label = Label(self.parent1,\
                textvariable = self.posvariable)


    def DisplayValue(self,astring):
        
        self.posvariable.set(astring)

    def Grid(self, row = 0, column = 0):
        self.label.grid(sticky = W+E+N+S, row = row,\
                        column = column)
