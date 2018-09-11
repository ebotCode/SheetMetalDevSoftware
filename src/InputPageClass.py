from Tkinter import *
from DisplayResultClass import * 
from TobeTopLevelClass import * 

class InputPageClass:
    def __init__(self,parent,displaynames,inputnames,displaynames2 = None):
        self.parent = parent
        self.name = self.parent.name
        self.displayobj = DisplayResultClass(self,row = 0,column = 0,size = (400,300))
        self.SetDisplayNames(displaynames)
        self.SetInputNames(inputnames)
        self.SetDisplayNames2(displaynames2)

    def SetDisplayNames(self,displaynames):

        self.displaynames = displaynames

    def SetDisplayNames2(self,displaynames):
        self.displaynames2 = displaynames


    def SetInputNames(self,inputnames):
        self.inputnames = inputnames

    def SetName(self,name):
        self.name = name
        self.parent.SetName(name)

    def GetWindowRef(self):
        return self.master


    def CreateWindow(self,root):
        self.master = TobeTopLevel(root,self,self.CloseWindow,self.name,maximize = 1)
        self.master.CreateMenuBar2()
        
        self.master.geometry("980x450")
##        self.master.maxsize(width = 989,height = 455)
##        self.master.minsize(width = 979,height = 445)
        
        self.master.title(self.name)
        self.master.rowconfigure(0,weight = 1)
        self.master.columnconfigure(0,weight = 1)

        self.frame = Frame(self.master)
        self.frame.grid(sticky = W+E+N+S, row = 0, column = 0)
        self.frame.columnconfigure(0,weight = 1)
        self.count = 0

##        self.rowconfigure(0,weight = 1)
        self.frame.rowconfigure(1,weight = 1)
##        self.rowconfigure(2,weight = 1)
        self.frame.columnconfigure(1,weight = 1)
##        self.columnconfigure(2,weight = 1)

        self.frame1 = Frame(self.frame)
        self.frame1.grid(sticky = W+E+N+S, row = 1,rowspan = 3,column = 0,padx = 2,pady = 10)
        self.rowcount = 0
        for i in range(len(self.displaynames)):
            self.rowcount +=2
            self.frame1.rowconfigure(2*i,weight = 1)
            self.frame1.columnconfigure(2*(i+1) - 1, weight = 1)
            
        self.frame1.columnconfigure(0,weight = 0)
        self.frame1.columnconfigure(1,weight =0 )


        self.frame2 = Frame(self.frame)
        self.frame2.grid(sticky = W+E, row = 3, column = 0)
        self.frame2.columnconfigure(0,weight = 1)

        self.label = Label(self.frame2,text = "Dr. S. Gbeminiyi   ", font = "Arial 7")
        self.label.grid(sticky = W, row = 0,column = 0)

        self.label12 = Label(self.frame2,text = self.parent.category, font = "Arial 7")
        self.label12.grid(sticky = E, row = 0,column = 1)

        self.CreateDisplayLabels()
        self.CreateButtons()
        self.displayobj.CreateWindow(self.frame4)



        

    def CreateDisplayLabels(self):
        self.labellist  = []
        self.entrylist = []
        for i in range(len(self.displaynames)):
            label = Label(self.frame1,text = self.displaynames[i], font = "Arial 10")
            label.grid(sticky = E, row = 2*i,column = 0)
            entry = Entry(self.frame1)
            entry.grid(sticky = W,row = 2*i, column = 1)
            self.labellist.append(label)
            self.entrylist.append(entry)

    def HasEdited(self,event = None):
        self.master.SetHasEdited()



        
    def CreateButtons(self):
        self.frame3 = Frame(self.frame1)
        self.frame3.grid(sticky = W+E, row = self.rowcount,column = 0, columnspan = 2,pady = 10)
##        self.frame3.rowconfigure(0,weight = 1)
        self.frame3.columnconfigure(0,weight = 1)
        self.frame3.columnconfigure(1,weight = 1)
        self.frame3.columnconfigure(2,weight = 1)
        self.frame3.columnconfigure(3,weight = 1)
        self.frame3.columnconfigure(4,weight = 1)
        self.frame3.columnconfigure(5,weight = 1)
        self.frame3.columnconfigure(6,weight = 1)


        self.calcbutton = Button(self.frame3,text = "Calculate",command = self.Calculate)
        self.calcbutton.grid(sticky = W+E, row = 0,column = 2,columnspan = 2)


        self.plotbutton = Button(self.frame3,text = "Plot",command = self.Plot)
        self.plotbutton.grid(sticky = W+E, row = 0,column = 5,columnspan = 2)
        



        self.frame4 = Frame(self.frame)
        self.frame4.grid(sticky = W+E+N+S, row = 1,rowspan = 3,column = 1)
        self.frame4.rowconfigure(0,weight = 1)
        self.frame4.columnconfigure(0,weight = 1)
        self.count = 0


    def CloseWindow(self):
        self.parent.CloseWindow()

    def SetInputs(self,values):
        self.parent.SetInputs(values)


    def GetInputs(self):
        values = {}
        for i in range(len(self.inputnames)):
            values [self.inputnames[i]] = self.entrylist[i].get()
            
        self.SetInputs(values)
        
    def Close(self):
        self.master.destroy()


    def Calculate(self):
        self.HasEdited()
        self.GetInputs()
        self.parent.Calculate()

    def Plot(self):
        self.parent.Plot()
    def CloseCanvasWindow(self):
        self.parent.CloseCanvasWindow()

    def GetWindowReference(self):
        return self.master

    def ShowResult1(self,dimensiondict,valuedict,othersdict = None):
        self.displayobj.InsertData(dimensiondict,valuedict,othersdict = othersdict)

    def ShowResult2(self,valuedict):
        self.displayobj.InsertValue(valuedict)
    def GetDataToSave(self,fileobj):
        self.fileobj = fileobj
        self.fileobj['text'] = self.displayobj.GetDataToSave()
        self.parent.GetDataToSave(fileobj)

    def ReceiveDataToOpen(self,fileobj):
        self.fileobj = fileobj
        btext = self.fileobj['text']
        name = self.fileobj['name']
        valuedict = self.fileobj['input']
        filepath = self.fileobj['filepath']
        self.master.SetName(name)
        self.master.SetOpenDetails(filepath)
        self.PlaceInputs(valuedict)
        self.displayobj.ReceiveDataToOpen(btext)
       
       
    def PlaceInputs(self,valuedict):
        if valuedict:
            values = {}
            for i in range(len(self.displaynames)):
                self.entrylist[i].insert(INSERT,valuedict[self.displaynames2[i]])


        
