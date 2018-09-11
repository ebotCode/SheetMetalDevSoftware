from DialogsGui import * 
from TobeTopLevel3Class import * 

class PageTemplate:
    def __init__(self):
        self.nothing = 1
        self.name = ""
       
    def SetInputs(self,value):
        self.values = value

    def ShowResult1(self,dimensiondict,valuedict,othersdict = None):
        self.inputpageobj.ShowResult1(dimensiondict,valuedict,othersdict = othersdict)



    def CreateWindow(self,root):
        self.inputpageobj.CreateWindow(root)
        self.master = self.inputpageobj.GetWindowReference()
        self.count = 0

    def CloseWindow(self):
        self.parent.CloseOption(self.idnumber)
        self.brain.Destroy()
        



    def GetInputs(self):
        self.brain.SetInput(self.values)
    def Close(self):
        self.master.destroy()


    def Calculate(self):
        self.allow = 1

        self.brain.SetErrorDialog(WarningDialog(self.inputpageobj.master))
        self.GetInputs()
        self.brain.Run()

    def SetName(self,name):
        self.name = name
        self.brain.SetName(name)
        


    def Plot(self):
        if self.allow:
            if self.brain.stop:
                pass
            else:
                self.count +=1
                if self.count == 1:
                    self.SetupWindow()
                self.brain.Plot(self.top1)

    def CloseCanvasWindow(self):
        self.count = 0
        self.brain.DestroyGui()

    def SetupWindow(self):
        self.top1 = TobeTopLevel3(self.master,self,funcid = self.CloseCanvasWindow)

    def SetIdnumber(self,idnumber):
        self.idnumber = idnumber

    def GetDataToSave(self,fileobj):
        self.fileobj = fileobj
        self.fileobj['input'] = self.brain.GetDataToSave()
        self.fileobj['category'] = self.category
        self.fileobj['classname'] = self.classname

    def ReceiveDataToOpen(self,fileobj):
        self.fileobj = fileobj
        self.inputpageobj.ReceiveDataToOpen(self.fileobj)
        
        
