from Tkinter import * 

class ShowButton:
    def __init__(self,parent1,linkerobject):
        self.parent1 = parent1
        self.linkerobject = linkerobject
        self.linkerobject.AddTool(self,name = "Show")
        
        self.frame = Frame(self.parent1)
        self.frame.rowconfigure(0, weight = 1)
        self.frame.columnconfigure(0,weight = 1)
        self.frame.columnconfigure(1,weight = 1)
        
        self.button1variable = BooleanVar()
        self.button2variable = BooleanVar()
        self.button1 = Checkbutton(self.frame,text = "ShowLabels",\
                                   variable = self.button1variable,
                                   command = self.ShowLabels)
        self.button2 = Checkbutton(self.frame,text = "ShowPatternLines",\
                                   variable = self.button2variable,
                                   command = self.ShowPatternLines)
        self.button1.grid(sticky = W, row = 0, column = 0)
        self.button2.grid(sticky = W,row = 0, column = 1)

        self.button1.invoke()
        self.button2.invoke()
        
        
    def Grid(self,row= 0, column = 0):
        self.frame.grid(sticky = NW, row = row,column = column)


    def ShowLabels(self):
        if self.button1variable.get():
            self.linkerobject.ShowLabels()
        else:
            self.linkerobject.UnShowLabels()

    def ShowPatternLines(self):
        if self.button2variable.get():
            self.linkerobject.ShowPatternLines()
        else:
            self.linkerobject.UnShowPatternLines()
